"""
LFG data are attributed to a class, allowing the configuration
file and other attributes to be attached to the FBS object. The functions
defined in this file are specific to LFG data.
"""
# necessary so 'LFG' can be used in fxn
# annotations without importing the class to the py script which would lead
# to circular reasoning
from __future__ import annotations

import pandas as pd
import numpy as np
from copy import deepcopy
from functools import partial, reduce
from sympy import exp, symbols

import esupy.processed_data_mgmt

from lfg_calc_py import settings, common, metadata
from lfg_calc_py.settings import DEFAULT_DOWNLOAD_IF_MISSING, datapath
from lfg_calc_py.lfg_log import reset_log_file, log
import lfg_calc_py.lfg_yaml as lfg_yaml
# from lfg_calc_py.validation import check_if_landfill_is_full

with open(settings.datapath / 'lfg_config.yaml') as f:
    lfg_config = lfg_yaml.load(f)


class LFG:
    _metadata = ['full_name', 'config']

    full_name: str
    config: dict

    def __init__(
        self,
        data: pd.DataFrame = None,
        *args,
        add_missing_columns: bool = True,
        fields: dict = None,
        column_order: List[str] = None,
        string_null: 'np.nan' or None = np.nan,
        **kwargs
    ) -> None:

        # Initialize metadata attributes
        for attribute in self._metadata:
            if not hasattr(self, attribute):
                setattr(
                    self,
                    attribute,
                    kwargs.pop(attribute, getattr(data, attribute, None))
                )

        if isinstance(data, pd.DataFrame) and fields is not None:
            if add_missing_columns:
                data = data.assign(**{field: None
                                      for field in fields
                                      if field not in data.columns})
            else:
                fields = {k: v for k, v in fields.items() if k in data.columns}

            fill_na_dict = {
                field: 0 if dtype in ['int', 'float'] else string_null
                for field, dtype in fields.items()
            }
            null_string_dict = {
                field: {null: string_null
                        for null in ['nan', '<NA>', 'None', '',
                                     np.nan, pd.NA, None]}
                for field, dtype in fields.items() if dtype == 'object'
            }

            data = (data
                    .fillna(fill_na_dict)
                    .replace(null_string_dict)
                    .astype(fields))

        if isinstance(data, pd.DataFrame) and column_order is not None:
            data = data[[c for c in column_order if c in data.columns]
                        + [c for c in data.columns if c not in column_order]]

        self.data = data


    @property
    def _constructor(self) -> 'LFG':
        return LFG


    @classmethod
    def get_lfg_df(
        cls,
        file_metadata: esupy.processed_data_mgmt.FileMeta,
        download_ok: bool,
        lfg_generator: partial,
        output_path: str,
        *,
        full_name: str = None,
        config: dict = None,
        external_data_path: str = None
    ) -> 'LFG':
        paths = deepcopy(settings.paths)
        paths.local_path = external_data_path or paths.local_path

        # todo: add option to download from data commons when directory is set up
        # attempt_list = (['import local', 'download', 'generate']
        #                 if download_ok else ['import local', 'generate'])
        attempt_list = ['import local', 'generate']

        for attempt in attempt_list:
            log.info(f'Attempting to {attempt} {file_metadata.name_data} '
                     f'{file_metadata.category}')
            if attempt == 'download':
                esupy.processed_data_mgmt.download_from_remote(
                    file_metadata,
                    paths
                )
            if attempt == 'generate':
                lfg_generator()
            df = esupy.processed_data_mgmt.load_preprocessed_output(
                file_metadata,
                paths
            )
            if df is None:
                log.info(f'{file_metadata.name_data} {file_metadata.category} '
                         f'not found in {paths.local_path}')
            else:
                log.info(f'Successfully loaded {file_metadata.name_data} '
                         f'{file_metadata.category} from {output_path}')
                break
        else:
            log.error(f'{file_metadata.name_data} {file_metadata.category} '
                      f'could not be found locally, downloaded, or generated')
        lfg = cls(df, full_name=full_name or '', config=config or {})
        return lfg

    @classmethod
    def return_LFG_calculations(
        cls,
        method: str,
        config: dict = None,
        # external_config_path: str = None,
        download_df_ok: bool = DEFAULT_DOWNLOAD_IF_MISSING,
        **kwargs
    ) -> 'pd.DataFrame':
        """
        Loads stored LFG output. If it is not
        available, tries to download it from EPA's remote server (if
        download_ok is True), or generate it.
        :param method: string, name of the FBS attribution method file to use
        :param external_config_path: str, path to the FBS method file if
            loading a file from outside the flowsa repository
        :param config: dict, method dictionary loaded from method yaml
        :param download_df_ok: bool, if True will attempt to load df
            from EPA's remote server rather than generating (if not found locally)
        :kwargs: keyword arguments - possible kwargs include full_name and config.
        :return: LFG dataframe
        """
        file_metadata = metadata.set_meta(method)

        # todo: add option for externally defined method yaml and to download from Data Commons
        lfg_generator = (
            lambda x=method: cls.generateLFG(x, config=config)
            )
        # lfg_generator = (
        #     lambda x=method, y=external_config_path: z=download_df_ok:
        #         cls.generateLFG(x, y, z, config=config)
        #     )

        lfg = LFG.get_lfg_df(
            file_metadata=file_metadata,
            download_ok=download_df_ok,
            lfg_generator=lfg_generator,
            output_path=settings.lfgoutputpath,
            full_name=method,
            config=config,
            **kwargs
        )

        return pd.DataFrame(lfg.data)

    @classmethod
    def generateLFG(
            cls,
            method: str,
            external_config_path: str = None,
            **kwargs
    ) -> 'LFG':
        '''
        Generates a FlowBySector dataset.
        :param method: str, name of FlowBySector method .yaml file to use.
        :param external_config_path: str, optional. If given, tells flowsa
            where to look for the method yaml specified above.
        :param download_fba_ok: bool, optional. Whether to attempt to download
            source data FlowByActivity files from EPA server rather than
            generating them.
        :kwargs: keyword arguments to pass to load_yaml_dict(). Possible kwargs
            include config.
        '''
        log.info('Beginning generation for %s', method)
        method_config = common.load_yaml_dict(method,
                                              filepath=external_config_path,
                                              **kwargs)
        # create instance of LFG
        lfg_instance = LFG(
            full_name=method,
            config=method_config,
            # external_config_path=external_config_path,
            # download_df_ok=download_sources_ok,
            # external_data_path=external_data_path
        )

        # generate lfg df
        lfg = lfg_instance.calculate_lfg_emissions()

        # Save df and metadata
        log.info(f'LFG generation complete, saving {method} to file')
        meta = metadata.set_meta(method, 'LFG')
        # save the emissions data to csv
        esupy.processed_data_mgmt.write_df_to_file(lfg.data, settings.paths, meta)
        reset_log_file(method, meta)
        metadata.write_metadata(source_name=method,
                                config=common.load_yaml_dict(
                                    method, filepath=external_config_path, **kwargs),
                                df_meta=meta
                                )

        return lfg


    # todo: modify to account for "false"/no default data/all user input data
    def load_default_decay_rates(
            self: 'LFG',
    ):
        source = self.config.get("default_decay_rates")
        if source == "Barlaz":
            path = datapath/'WARM_Barlaz_Material_Decay_Rates.csv'
        # elif source == "IPCC":
        #     path = datapath/'IPCC_Waste_specific_k-values.csv'
        with open(path) as file:
            decay_rates = pd.read_csv(file)
        return decay_rates


    def return_waste_acceptance(
            self: 'LFG',
            waste_rate_df,
            year
    ):
        """
        Return the waste acceptance for a year, return 0 value if no waste managed that year
        :param year:
        :return:
        """

        try:
            return float(waste_rate_df.loc[
                             waste_rate_df['Year'] == year,
                             'WasteAcceptanceRate'].values[0])
        except IndexError:
            return 0

    def return_material_decay_rates(
            self: 'LFG',
            material
    ):
        """
        Return the methane generation rate for a material type
        :return:
        """

        if "material_decay_rates" in self.config:
            material_decay_rates_df = pd.DataFrame(self.config.get("material_decay_rates").items(),
                                                   columns=['Material', 'Decay_Rate'])
        else:
            material_decay_rates_df = (
                self.load_default_decay_rates()[
                    ["Material", "Landfill_Moisture_Conditions", "Decay_Rate"]]
                .query(f"Landfill_Moisture_Conditions=='{self.config.get('moisture_conditions')}'")
            )
        return float(material_decay_rates_df.loc[
                         material_decay_rates_df['Material'] == material, 'Decay_Rate'].values[0])

    def return_material_ratio(
            self: 'LFG',
            material_ratio_df,
            material
    ):
        """
        Return the fraction of a material in a waste
        :return:
        """
        return float(material_ratio_df.loc[
                material_ratio_df['Waste Type'] == material, 'Waste Fraction'].values[0])


    # def return_gas_collection_efficiency(
    #         self: 'LFG',
    #         material_lfg_collection_efficiencies,
    #         material
    # ):
    #     """
    #     Return gas collection efficiency by material; return 0 value if LFG is not captured
    #     :return:
    #     """
    #     try:
    #         return float(material_lfg_collection_efficiencies.loc[
    #             material_lfg_collection_efficiencies['Material'] == material,
    #             self.config.get("moisture_conditions")].values[0])
    #     except IndexError:
    #         return 0


    def return_annual_lfg_collection_efficiency(
            self: 'LFG',
            annual_lfg_collection_efficiencies,
            y
    ):
        """
        Return gas collection efficiency by year; return 0 value if LFG is not captured
        :param year:
        :return:
        """
        # try:
        #     return float(annual_lfg_collection_efficiencies.loc[
        #                  annual_lfg_collection_efficiencies['Year'] == year, 'Efficiency'].values[0])
        # except IndexError:
        #     return 0

        if y<=15:
            return float(annual_lfg_collection_efficiencies.loc[
                             annual_lfg_collection_efficiencies['Year'] == y, 'Efficiency'].values[0])
        elif y>15:
            return float(annual_lfg_collection_efficiencies.loc[
                             annual_lfg_collection_efficiencies['Year'] == 15, 'Efficiency'].values[0])
        else: return 0


    def calculate_lfg_emissions(
            self: 'LFG',
    ):
        # Variable names and units are derived from USEPA's LandGEM tool.

        # WARM LFG collection efficiencies by year
        annual_lfg_collection_efficiencies = common.load_data_csv('LFG_collection_scenario_values')

        # WARM material-specific LFG collection efficiencies
        material_lfg_collection_efficiencies = common.load_data_csv('WARM_GasCollectionEfficiencies_v1')

        # empty dictionary
        waste_rate_split = {}
        material_ratio_split = {}

        for key, value in self.config.get("waste_acceptance_rate").items():
            # if data is provided as a range, split the range and add waste acceptance for each year to new dictionary
            if "-" in str(key):
                y1, y2 = map(int, key.split("-"))
                for year in range(y1, y2 + 1):
                    waste_rate_split[str(year)] = value
            # else if entry is a single value, append to new dictionary as-is
            else:
                waste_rate_split[str(key)] = value

        for key, value in self.config.get("material_ratios").items():
            # if data is provided as a range, split the range and add waste acceptance for each year to new dictionary
            if "-" in key:
                y1, y2 = map(int, key.split("-"))
                for year in range(y1, y2 + 1):
                    material_ratio_split[str(year)] = value
            # else if entry is a single value, append to new dictionary as-is
            else:
                material_ratio_split[str(key)] = value

        # convert expanded dictionary into df
        waste_rate_df = pd.DataFrame(waste_rate_split.items(), columns = ['Year', 'WasteAcceptanceRate'])
        material_ratio_df = pd.DataFrame(self.config.get("material_ratios").items(),
                                         columns = ['Waste Type', 'Waste Fraction'])

        # set datatypes
        waste_rate_df['Year'] = waste_rate_df['Year'].astype(int)
        waste_rate_df['WasteAcceptanceRate'] = waste_rate_df['WasteAcceptanceRate'].astype(float)

        # define first year of waste acceptance
        year_init = waste_rate_df['Year'][0]

        # Defining calc_year
        if "calc_year" in self.config:
            calc_year = self.config.get("calc_year")
        elif "landfill_close" in self.config:
            calc_year = self.config.get("landfill_close")
        # default warm calculation
        else:
            calc_year = year_init + self.config.get("landfill_lifespan")

        # Defining T as the range of calculation
        T = calc_year - year_init

        # subset waste acceptance rate df to include years up-to and including calc year
        waste_rate_df_subset = waste_rate_df[waste_rate_df['Year'] <= calc_year-1]

        # add material ratios
        material_type_list = list(self.config.get("material_ratios").keys())

        # # Remove excess moisture scenarios
        # material_lfg_collection_efficiencies = (
        #     material_lfg_collection_efficiencies[
        #         ["Material", "Proxy", "Scenario", self.config.get("moisture_conditions")]]
        #     .query(f"Scenario=='{self.config.get('LFG_collection_scenario')}'")
        # )
        # Remove excess moisture scenarios

        annual_lfg_collection_efficiencies = (
            annual_lfg_collection_efficiencies[
                ["Scenario", "Year", "Efficiency"]]
            .query(f"Scenario=='{self.config.get('LFG_collection_scenario')}'")
        )
        annual_lfg_collection_efficiencies['Year'] = annual_lfg_collection_efficiencies['Year'].astype(int)

        added_years = pd.DataFrame({
            'Scenario': self.config.get('LFG_collection_scenario'),
            'Year': range(16, self.config.get("landfill_lifespan") + 1),
            'Efficiency': annual_lfg_collection_efficiencies.loc[
                annual_lfg_collection_efficiencies['Year'] == 15,
                'Efficiency'].values[0]
        })

        annual_lfg_collection_efficiencies = pd.concat([
            annual_lfg_collection_efficiencies, added_years], ignore_index=True)
        annual_lfg_collection_efficiencies = annual_lfg_collection_efficiencies.rename(columns={
            'Scenario': 'Scenario', 'Year': 'landfillOperationYear', 'Efficiency': 'Efficiency'})

        # Methane calculation

        # initial df to calc emissions
        df = pd.DataFrame({
            'Year': [year_init + i for i in range(T)],
            'landfillOperationYear': range(T),
        })

        # add input years then explode
        df['inputYears'] = df['landfillOperationYear'].apply(lambda x: list(range(x)))
        df2 = df.explode('inputYears').copy()
        df2.rename(columns={'inputYears': 'inputYearIndex'}, inplace=True)
        df2['inputYear'] = df2['inputYearIndex'] + year_init
        # diff between landfill operation year and year of waste input, used to calc emission gen,
        # ignore Downcasting object warning
        with pd.option_context("future.no_silent_downcasting", True):
            df2['yearDiff'] = (df2['landfillOperationYear'] - df2['inputYearIndex']).fillna(0).astype(int)

        # Store all material emission summaries
        emissions_data = []

        # loop through materials to calc emissions
        for material in material_type_list:

            # copy parent df
            df_material = df2.copy()

            # add waste acceptance by input year
            df_material['waste_acceptance'] = df_material['inputYear'].apply(
                lambda y: self.return_waste_acceptance(waste_rate_df_subset, y)
            )

            # Compute methane generated with first order decay eqn
            df_material['methane_generated'] = (
                self.return_material_ratio(material_ratio_df, material)
                * df_material['waste_acceptance']
                * self.config.get("methane_fraction")
                * self.config.get("degradable_organic_carbon")
                * self.config.get("degradable_organic_carbon_fraction")
                * self.config.get("methane_content")
                * 16/12
                * (np.exp(-self.return_material_decay_rates(material) * (df_material['yearDiff'] - 1)
                          ) - np.exp(-self.return_material_decay_rates(material) * df_material['yearDiff'])
                   )
            )

            df_material2 = pd.merge(df_material, annual_lfg_collection_efficiencies,
                                    on='landfillOperationYear', how='inner')

            df_material2['methane_captured'] = (
                    df_material2['methane_generated']
                    * df_material2['Efficiency']
            )

            # Summarize methane metrics by landfill operation year
            df_agg = df_material2.groupby(['Year', 'landfillOperationYear', 'Scenario'])[['methane_generated',
                                                                                          'methane_captured']].sum().reset_index()

            df_agg['methane_emitted'] = ((df_agg['methane_generated'] - df_agg['methane_captured'])
                                         * (1 - self.config.get("methane_oxidation_fraction")))

            # Rename columns to include material name
            df_agg.rename(columns={
                'methane_generated': f'{material} Methane Generation',
                'methane_captured': f'{material} Methane Capture',
                'methane_emitted': f'{material} Methane Emitted',
            }, inplace=True)

            # Store for final merging
            emissions_data.append(df_agg)

        # Merge all material summaries into final result
        df_merge = reduce(lambda left, right: pd.merge(left, right, on=['Year', 'landfillOperationYear'], how='outer'), emissions_data)
        df_merge['Unit'] = self.config.get("unit")
        df_merge.sort_values(by='Year', inplace=True)


        # todo: reincorporate cumulative emissions and other col values

        #         log.info(f"{material} emissions generated by waste landfilled in year {x}, during landfill "
        #               f"operation year {landfill_year}: {methane_by_input_waste_year}")
        #
        #         # update the annual landfill emissions by summing the methane generated by each year of waste input
        #         methane_annual += methane_by_input_waste_year
        #
        #     methane_annual_captured = (
        #         methane_annual
        #         * self.return_gas_collection_efficiency(material_lfg_collection_efficiencies, material)
        #         * self.return_annual_lfg_collection_efficiency(annual_lfg_collection_efficiencies, x)
        #     )
        #
        #     methane_total_gen[material] += methane_annual  # cumulative total for material
        #     methane_total_capture[material] += methane_annual_captured  # cumulative total for material
        #
        #     row[f"{material} Annual Methane Generation, Tonnes CH4"] = methane_annual  # annual value
        #     row[f"{material} Annual Methane Capture, Tonnes CH4"] = methane_annual_captured  # annual value
        #     row[f"{material} Annual Methane Emitted, Tonnes CH4"] = methane_annual - methane_annual_captured  # annual value
        #     row[f"{material} Total Methane Generation, Tonnes CH4"] = methane_total_gen[material]  # cumulative
        #     row[f"{material} Total Methane Capture, Tonnes CH4"] = methane_total_capture[material]  # cumulative
        #     row[f"{material} Total Methane Emitted, Tonnes CH4"] = methane_total_emit[material]  # cumulative
        #


        # store emissions data within self
        self.data = df_merge

        return self
