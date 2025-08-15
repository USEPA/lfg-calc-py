import logging as log
from os import path
import re
import pandas as pd

from lfg_calc_py.settings import methodpath, datapath
import lfg_calc_py.lfg_yaml
from lfg_calc_py.lfg_log import log


def load_yaml_dict(filename, filepath=None, **kwargs):
    """
    Load the information in a yaml file

    :return: dictionary containing all information in yaml
    """
    # check if the version and githash are included in the filename, if so,
    # drop, but return warning that we might be loading a revised version of
    # the config file. The pattern looks for a "_v" followed by a number
    # between [0-9] followed by a decimal
    pattern = '_v[0-9].*'
    if re.search(pattern, filename):
        log.warning('Filename includes a github version and githash. Dropping '
                 'the version and hash to load most up-to-date yaml config '
                 'file. The yaml config file might not reflect the yaml used '
                 'to generate the dataframe')
        filename = re.sub(pattern,'', filename)

    if filepath is None:
        folder = methodpath
    else:
        # todo: test code in else statement
        # first check if a filepath for the yaml is specified, as is the
        # case with method files located outside the lfg-cal-py repo
        # if filepath is not None:
        if path.exists(path.join(str(filepath), f'{filename}.yaml')):
                log.info(f'Loading {filename} from {filepath}')
                folder = filepath
        else:
            raise KeyError(f'{filename} not found in {filepath}.')

    yaml_path = f'{folder}/{filename}.yaml'

    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = lfg_calc_py.lfg_yaml.load(f, filepath)
    except FileNotFoundError:
        raise KeyError(f"{filename} not found in {folder}")

    return config


def load_data_csv(filename):
    """
    Loads csv data from lfg_calc_py/data
    :param filename:
    :return:
    """
    path = datapath/f'{filename}.csv'
    with open(path) as file:
        df = pd.read_csv(file, encoding='utf-16')
    # replace Byte Order Mark
    df.columns = df.columns.str.replace('ï»¿', '')
    return df

