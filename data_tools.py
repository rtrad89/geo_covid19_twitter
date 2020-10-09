# -*- coding: utf-8 -*-
"""
Data loader and transformer for GeoCov analyses

"""
import os
from shutil import rmtree
import pandas as pd
from datetime import datetime as dt
from root_logger import logger
import gc
import preprocessor as pptweet


class DataTools:
    """
    A static class to take care of data operations and transformations
    """
    # Define the list of csv data, so that we save them to disk for subsequent
    # visualisation and statistical learning
    list_of_output_dfs = []

    def __init__(self):
        pass

    @classmethod
    def prune_retweets_clean_to_csv(cls,
                                    csv_files: dict,
                                    dirpath: str,
                                    clean: bool = True):
        # Make sure it is a directory path
        if not cls.is_path_dir(dirpath):
            logger.error("You inputted a file path, not a directory")
        # Make the directory if it's not there
        elif not cls.path_exists(dirpath):
            cls.initialise_directories(dirpath)
        # If the directory is not empty, user must investigate this
        # so that no time/data are lost
        elif not cls.is_dir_empty(dirpath):
            logger.error("You inputted an unempty directory. "
                         "if you still want to use it, make sure to "
                         "backup or delete the files therein manually")
        else:
            for k, v in csv_files.items():
                df = cls.load_tweets_ds(v, remove_retweets=True)
                df = df.drop(columns="reweet_id")
                df.text = cls.prerocess_tweets_texts(df.text)
                # Save the pruned csv under the directory
                filepath = f"{dirpath}\\original_{k}.csv"
                df.to_csv(path_or_buf=filepath, sep=",",
                          index=False, encoding="utf-8")
                logger.info(f"File {cls.get_filename(v)} pruned and saved")
                cls.clean_memory()

    @staticmethod
    def prerocess_tweets_texts(texts: pd.Series) -> pd.Series:
        ret = []
        # clean only URLs and Emojis from tweets
        pptweet.set_options(pptweet.OPT.URL, pptweet.OPT.EMOJI)
        for text in texts:
            ret.append(pptweet.clean(text))

        return pd.Series(data=ret)

    @staticmethod
    def load_tweets_ds(csv_fpath: str,
                       remove_retweets: bool = True) -> pd.DataFrame:
        if DataTools.path_exists(csv_fpath):
            ret = pd.read_csv(
                filepath_or_buffer=csv_fpath,
                encoding="utf-8", sep=",",
                usecols=["id", "created_at", "hashtags", "reweet_id",
                         "user_screen_name", "user_followers_count",
                         "user_friends_count", "user_verified",
                         "text"],
                parse_dates=["created_at"],
                infer_datetime_format=True
                )
            if remove_retweets:
                ret = ret[ret.reweet_id.isna()]
            return ret
        else:
            logger.error(msg=f"CSV file \"{csv_fpath}\" was not found")
            return None

    @staticmethod
    def initialise_directory(dir_path):
        """
        Ensure an empty directory is created in `dir_path`.
        Parameters
        ----------
        dir_path : str
            The path of the desired directory.
        Raises
        ------
        PermissionError
            If `dir_path` is not accessible by the current user.
        """

        try:
            if os.path.exists(dir_path):
                rmtree(dir_path)
            os.mkdir(dir_path)
        except PermissionError:
            logger.error("Please make sure the folders required by the program"
                         "are not already opened")

    @staticmethod
    def remove_directory(dir_path):
        if os.path.exists(dir_path):
            rmtree(dir_path)

    @staticmethod
    def initialise_directories(dir_path):
        """
        Ensure an empty directory is created in `dir_path`, guaranteeing that
        all the needed directories on the path are also created
        Parameters
        ----------
        dir_path : str
            The path of the desired directory.
        Raises
        ------
        PermissionError
            If `dir_path` is not accessible by the current user.
        """

        try:
            if os.path.exists(dir_path):
                rmtree(dir_path)
            os.makedirs(dir_path)
        except PermissionError:
            logger.error("Please make sure the folders required by the program"
                         "are not already opened")

    @staticmethod
    def get_filename(path) -> str:
        return os.path.basename(path)

    @staticmethod
    def scan_directory(path):
        return os.scandir(path)

    @staticmethod
    def path_exists(path):
        return os.path.exists(path)

    @staticmethod
    def is_path_dir(path):
        return os.path.isdir(path)

    @classmethod
    def is_dir_empty(cls, path):
        return len(os.listdir(path=path)) == 0

    @staticmethod
    def save_list_to_text(mylist: list, filepath: str,
                          header: str = None):
        with open(file=filepath, mode='w', encoding="utf8") as file_handler:
            if header:
                file_handler.write(f"{header}\n{'-'*12}\n")
            for item in mylist:
                file_handler.write(f"{item}\n")

    @classmethod
    def add_output_df(cls,
                      odf: pd.DataFrame) -> int:
        if(odf is not None and len(odf) > 0):
            cls.list_of_output_dfs.append(odf)
            logger.info("Output dataframe added successfully")
        else:
            logger.warning("Cannot add empty dataframes to outputs")
        return len(cls.list_of_output_dfs)

    @staticmethod
    def clean_memory():
        logger.info(f"{gc.collect()} memory objects purged")


def main():
    print("Data loader main() here")
    logger.shutdown()


if __name__ == "__main__":
    main()
