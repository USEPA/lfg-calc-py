# __init__.py (lfg_calc_py)
# !/usr/bin/env python3
# coding=utf-8

import pandas as pd

from lfg_calc_py.lfg_calc_py import LFG
from lfg_calc_py.settings import DEFAULT_DOWNLOAD_IF_MISSING


def getLFGCalculations(
        methodname,
        # external_config_path=None,
        # download_df_if_missing=DEFAULT_DOWNLOAD_IF_MISSING,
        **kwargs
        ) -> pd.DataFrame:
    """
    Loads stored lfg_calc_py output or generates it if it doesn't exist,
    then loads
    :param methodname: str, name of an available method
    :param configpath: str, path to the method file if loading a file
        from outside the repository
    :param download_df_if_missing: bool, if True will attempt to load from
        remote server prior to generating if file not found locally
    :return: dataframe in flow by sector format
    """
    df = LFG.return_LFG_calculations(
        method=methodname,
        # external_config_path=external_config_path,
        # download_df_ok= download_df_if_missing,
        **kwargs
    )

    return df
