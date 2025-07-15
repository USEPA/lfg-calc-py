# metadata.py (flowsa)
# !/usr/bin/env python3
# coding=utf-8
"""
Functions for creating and loading metadata files for
FlowByActivity (FBA) and FlowBySector (FBS) datasets
"""

import pandas as pd
from esupy.processed_data_mgmt import FileMeta, write_metadata_to_file, \
    read_source_metadata
from lfg_calc_py.lfg_log import log
from lfg_calc_py.settings import paths, PKG, PKG_VERSION_NUMBER, WRITE_FORMAT, \
    GIT_HASH, GIT_HASH_LONG


def set_meta(name_data, category=None):
    """
    Create meta data for a parquet
    :param name_data: string, name of df
    :param category: string, 'FlowBySector' or 'FlowByActivity'
    :return: object, metadata for parquet
    """
    df_meta = FileMeta()
    df_meta.tool = PKG
    df_meta.category = ""
    df_meta.name_data = name_data
    df_meta.tool_version = PKG_VERSION_NUMBER
    df_meta.git_hash = GIT_HASH
    df_meta.ext = "csv"
    df_meta.date_created = \
        pd.to_datetime('today').strftime('%Y-%m-%d %H:%M:%S')
    return df_meta


def write_metadata(source_name, config, df_meta, **kwargs):
    """
    Write the metadata and output as a JSON in a local directory
    :param source_name: string, source name for either a FBA or FBS dataset
    :param config: dictionary, configuration file
    :param df_meta: object, metadata
    :param category: string, 'FlowBySector' or 'FlowByActivity'
    :param kwargs: additional parameters, if running for FBA, define
        "year" of data
    :return: object, metadata that includes methodology for FBAs
    """
    # create empty dictionary
    df_dict = {}
    # add url of method at time of commit
    df_dict['method_url'] = \
        f'https://github.com/USEPA/lfg-calc-py/blob/{GIT_HASH_LONG}/lfg_calc_py/' \
        f'methods/{source_name}.yaml'

    df_dict.update(df_meta)

    write_metadata_to_file(paths, df_dict)

    return df_dict






