# -*- coding: utf-8 -*-
from data_tools import DataTools
from root_logger import logger

# Control variable:
prune_tweets = False
resave_5g_tagged_tweets = True
# The paths to the datasets
datasets_folder = r"..\..\Datasets\twitter-sars-cov-2"


# def main():
logger.info("Main Module Start")
# Location where the original tweets are
master_folder = f"{datasets_folder}\\pruned"

if prune_tweets:
    # If the tweet csvs still contain retweets, clean them
    dpaths = {}
    dpaths["2002"] = (f"{datasets_folder}\\ids_all_langs__2020-02-01\\"
                      "ids_2020-02-01.csv")
    dpaths["2003"] = (f"{datasets_folder}\\ids_2020-03-01\\"
                      "tweets_2020-03-01.csv")
    dpaths["2004"] = (f"{datasets_folder}\\ids_2020-04-01\\"
                      "covid19_tweets_20200401.csv")
    dpaths["2005"] = (f"{datasets_folder}\\ids_2020-05-01\\"
                      "tweets_20200501.csv")
    DataTools.prune_retweets_clean_to_csv(csv_files=dpaths,
                                          dirpath=master_folder)

# append pruned to the master path and proceed:
dfs = {}
# Load the four datasets for pruning and saving
with DataTools.scan_directory(master_folder) as docs:
    for doc in docs:
        dfs[doc.name] = DataTools.load_tweets_ds(doc.path)
        logger.info(f"File {doc.name} loaded into a dataframe")


logger.shutdown()
logger.info("Main Module End.")


# if __name__ == "__main__":
#     main()
