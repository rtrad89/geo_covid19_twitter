# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 18:21:56 2020

@author: trad
"""

import pandas as pd
from root_logger import logger
from typing import Final
from data_tools import DataTools as dtls


class ConspiracyDetector:
    """
    A controller class for specific conspiracy topics detection
    """
    G5: Final = 'g'
    CHIP: Final = 'c'

    @classmethod
    def label_tweets(cls,
                     texts: pd.Series, mode: str
                     ) -> pd.Series:
        # This routine would label a tweet as discussing 5G or not
        if mode == cls.G5:
            label = texts.str.contains(pat=r"\b5g\b",
                                       case=False, regex=True)
        elif mode == cls.CHIP:
            label = texts.str.contains(pat=r"chip", case=False, regex=True)
        else:
            logger.error("Specified mode of conspiracy labeller unrecognised")
            raise ValueError("Mode is not valid.")

        return pd.Series(data=label, index=texts.index)

    @classmethod
    def annotate_tweets_ds(cls,
                           dict_ds: dict,
                           store: bool = False,
                           dirpath: str = (r"..\..\Datasets\twitter-sars-cov-2"
                                           "\\annotated\\")
                           ) -> dict:
        # TODO: find a way to check store once not twice without recoding
        # If we want to store the results and the provided directory is invalid
        # then exit
        if store:
            if not dtls.isready_dirpath(dirpath):
                raise IOError(
                    f"Provided storage destination '{dirpath}' is not valid")
        # Either we don't want to store, or the storage destination is valid
        for k, ds in dict_ds.items():
            ds["five_g"] = cls.label_tweets(ds.text, mode=cls.G5)
            logger.info(f"Dataset {k} annotated with 5G labels")
            if store:
                fpath = f"{dirpath}\\annotated_{k}"
                ds.to_csv(path_or_buf=fpath, sep=",",
                          index=False, encoding="utf-8")
                logger.info(f"Annotated dataset {k} saved to disk")

        return dict_ds
