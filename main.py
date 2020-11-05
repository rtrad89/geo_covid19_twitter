# -*- coding: utf-8 -*-
from data_tools import DataTools
from root_logger import logger
from conspiracy_detection import ConspiracyDetector


# Control variable:
prune_tweets = True
resave_5g_tagged_tweets = True
# The paths to the datasets
datasets_folder = r"..\..\Datasets\twitter-sars-cov-2"


def main():
    logger.info("Main Module Start")
    # Location where the original tweets are
    master_folder = f"{datasets_folder}\\pruned"

    if prune_tweets:
        # If the tweet csvs still contain retweets, clean them
        logger.info("You've chosen to prune the files. Pruning..")
        # Make a dictionary of <filepaths, whether it's hydrator schema>
        dpaths = {}
        dpaths["200201"] = ((f"{datasets_folder}\\ids_2020-02-01\\"
                             "Rehydrate_tweets_2020-02-01.csv"), True)
        dpaths["200215"] = ((f"{datasets_folder}\\ids_2020-02-15\\"
                             "tweets_2020-02-15.csv"), True)
        dpaths["200301"] = ((f"{datasets_folder}\\ids_2020-03-01\\"
                             "rehydrated_tweets_20200301.csv"), False)
        dpaths["200401"] = ((f"{datasets_folder}\\ids_2020-04-01\\"
                             "rehydrated_tweets_20200401.csv"), True)
        dpaths["200501"] = ((f"{datasets_folder}\\ids_2020-05-01\\"
                            "tweets_20200501.csv"), True)
        dpaths["200315"] = ((f"{datasets_folder}\\ids_2020-03-15\\"
                             "tweets_2020-03-15.csv"), True)
        dpaths["200415"] = ((f"{datasets_folder}\\ids_2020-04-15\\"
                             "tweets_2020-04-15.csv"), True)
        try:
            DataTools.prune_retweets_clean_to_csv(csv_files=dpaths,
                                                  dirpath=master_folder,
                                                  only_eng=True)
        except Exception:
            logger.exception("exception raised")

    logger.info("Pruning phase ended.")

    if not resave_5g_tagged_tweets:
        exit(0)

    # append pruned to the master path and proceed:
    dfs = {}
    # Load the four datasets for pruning and saving
    with DataTools.scan_directory(master_folder) as docs:
        for doc in docs:
            dfs[doc.name] = DataTools.load_tweets_ds(csv_fpath=doc.path,
                                                     already_pruned=True,
                                                     hydrator_file=True,
                                                     remove_retweets=False)
            logger.info(f"File {doc.name} loaded into a dataframe")

    # Annotate tweets with 5G labels in five_g columns
    logger.info("Annotating tweets with 5G labels")
    dfs = ConspiracyDetector.annotate_tweets_ds(dict_ds=dfs,
                                                store=resave_5g_tagged_tweets)

    logger.info("Annotation of 5G finished")

    logger.shutdown()
    logger.info("Main Module End.")


if __name__ == "__main__":
    main()
