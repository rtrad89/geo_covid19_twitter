"""
Data loader and transformer for GeoCov analyses

"""
import os
from shutil import rmtree
import pandas as pd
from sys import exit
from root_logger import logger


class DataTools:
    """
    """

    def __init__(self):
        pass

    @staticmethod
    def load_tweets_ds(csv_fpath: str) -> pd.DataFrame:
        if DataTools.path_exists(csv_fpath):
            pd.read_csv(filepath_or_buffer=csv_fpath,
                        encoding="utf-8", sep=",", header=True,
                        usecols=["id", "created_at", "hashtags", "reweet_id",
                                 "user_screen_name", "user_followers_count",
                                 "user_friends_count", "user_verified",
                                 "text"]
                        )
        else:
            logger.error(msg=f"CSV file \"{csv_fpath}\" was not found.")
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
            print("ERROR: Please make sure the folders required by the program"
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
            print("ERROR: Please make sure the folders required by the program"
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

    @staticmethod
    def save_list_to_text(mylist: list, filepath: str,
                          header: str = None):
        with open(file=filepath, mode='w', encoding="utf8") as file_handler:
            if header:
                file_handler.write(f"{header}\n{'-'*12}\n")
            for item in mylist:
                file_handler.write(f"{item}\n")


def main():
    print("Data loader main..")
    print("Exiting with code 0")
    logger.shutdown()
    exit(0)


if __name__ == "__main__":
    main()
