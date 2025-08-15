"""
Download GHGRP tables via StEWI
https://enviro.epa.gov/query-builder/ghg/SUBPART%20HH%20-%20MUNICIPAL%20SOLID%20WASTE%20LANDFILLS/

"""
# import pandas as pd
# from stewi.GHGRP import import_or_download_table, OUTPUT_PATH, MetaGHGRP, ghgrp_cols
#
# # TODO: check table requirements for landgem
# tables = ['HH_SUBPART_LEVEL_INFORMATION',
#           'HH_GAS_COLLECTION_SYSTEM_DETLS',
#           # 'HH_ACTIVE_AERATION_SYS_DETLS', # Not working
#           ]
# # year = '2022'
#
# # TODO: import start/end years from yaml?
# # example function imputs
# year_start = 1960
# year_end = 2024
# GHGRP_ID = "1000216"
#
# def return_ghgrp_data(GHGRP_ID, year_start, year_end):
#
#     # empty df
#     ghgrp_data = pd.DataFrame()
#
#     for year in range(year_start, year_end):
#         print(year)
#         # Each table is saved in the specific GHGRP output path by year
#         tables_dir = OUTPUT_PATH.joinpath('tables', year)
#         tables_dir.mkdir(exist_ok=True, parents=True)
#
#         df = pd.DataFrame()
#         for table in tables:
#             filepath = tables_dir.joinpath(f"{table}.csv")
#             t = import_or_download_table(filepath, table, year, m=MetaGHGRP())
#             t['table'] = table
#             df = pd.concat([df, t], ignore_index=True)
#             # ^^ number of columns can get quite large as they are often unique
#             # to each table.
#
#             # TODO: Check if indents correct for following lines
#             # TODO: subset by id number
#
#             # append to ghgrp_data pandas dataframe
#             # TODO: need to append to empty dataframe for function to work
#
#
#     return ghgrp_data