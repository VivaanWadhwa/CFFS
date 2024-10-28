import os
from typing import Tuple
import numpy as np
import pandas as pd
import logging

logging.basicConfig(level = logging.INFO, format = "%(asctime)s -- %(levelname)s - %(message)s")

class Calculator:
    """This class is designed for representing the calculation workflow"""
    new_items = None
    nonstdpreps = None
    nonstditems = None
    liquid_unit = None
    solid_unit = None
    ghge_factors = None
    nitro_factors = None
    water_factors = None
    land_factors = None
    items_assigned = None
    manual_prepu = None
    manual_factor = None
    mapping = None
    def __init__(self, labeller_instance) -> None:
        self.labeller = labeller_instance
    ## Data Cleaning
    def __assign_multiplier(self,df: pd.DataFrame) -> None:
        """Assigns a multiplier to each conversion in dataframe"""
        for ind, row in df.iterrows():
            if row["ConvertFromQty"] == 0 or row["ConvertToQty"] == 0:
                df.loc[ind, "Multiplier"] = 1
            else:
                df.loc[ind, "Multiplier"] = row["ConvertFromQty"] / row["ConvertToQty"]
    def __update_conversions(self) -> None:
        """Updates the existing conversions dataframe with the new one just read in"""
        conversions = self.labeller.conversions
        update_conv = pd.read_csv(os.path.join(os.getcwd(), "data", "cleaning",
                                               "update", "Conv_UpdateConv.csv"))
        self.__assign_multiplier(update_conv)
        for _, row in update_conv.iterrows():
            idx = row['ConversionId']
            if idx in conversions['ConversionId'].values:
                conversions.drop(conversions[conversions['ConversionId'] == idx].index,
                                  inplace=True)
            else:
                print(f"Warning: 'ConversionId' {idx} not found in" +
                      "Conversions DataFrame. Skipping drop operation.")
        frames = [conversions, update_conv]
        conversions = pd.concat(frames).reset_index(drop=True, inplace=False).drop_duplicates()
        conversions.to_csv(os.path.join(os.getcwd(), "data", "cleaning",
                                        "update", "Conv_UpdateConv.csv"), index=False)
    def __special_converter(self, ingre: str , qty: float, uom: str) -> Tuple[float, str]:
        """Converts a quantity and unit of measurement to standard units if possible"""
        std_unit = pd.read_csv(os.path.join(os.getcwd(), "data", "external",
                                            "standard_conversions.csv"))
        self.liquid_unit = std_unit.loc[std_unit['ConvertToUom'] == 'ml', 'ConvertFromUom'].tolist()
        self.solid_unit = std_unit.loc[std_unit['ConvertToUom'] == 'g', 'ConvertFromUom'].tolist()
        def std_converter(qty, uom):
            if uom in std_unit['ConvertFromUom'].tolist():
                multiplier = std_unit.loc[std_unit['ConvertFromUom'] == uom, 'Multiplier']
                ret_qty = float(qty)*float(multiplier)
                ret_uom = std_unit.loc[std_unit['ConvertFromUom'] == uom, 'ConvertToUom'].values[0]
            else:
                ret_qty = qty
                ret_uom = uom
            return (ret_qty, ret_uom)
        conversions = self.labeller.conversions
        spc_cov = list(filter(None, conversions['ConversionId'].tolist()))
        if uom in self.liquid_unit + self.solid_unit:
            return std_converter(qty, uom)
        if ingre in spc_cov:
            conversion = conversions.loc[(conversions['ConversionId'] == ingre) &
                                         (conversions['ConvertFromUom'] == uom)
                                        & (conversions['ConvertToUom'] == 'g')]
            multiplier = conversion['Multiplier']
            if multiplier.empty:
                return std_converter(qty, uom)
            ret_qty = float(qty)/float(multiplier)
            ret_uom = conversion['ConvertToUom'].values[0]
            return (ret_qty, ret_uom)
        return std_converter(qty, uom)
    def __find_non_std_items(self) -> pd.DataFrame:
        """Finds non-standard items in the ingredients dataframe"""
        ingredients = self.labeller.ingredients
        conversions = self.labeller.conversions
        items = self.labeller.items
        col_names = list(ingredients.columns.values)
        # Create a Items_Nonstd list
        items_nonstd = []
        # If the unit of measurement is not grams or ml and ingredient id starts with I
        # and the ingredient is not in ConversionId column of Conversions
        # then we add it to Items_Nonstd list
        for index, row in ingredients.iterrows():
            ingre = ingredients.loc[index,'IngredientId']
            uom = ingredients.loc[index,'Uom']
            if (uom not in ['g', 'ml'] and uom not in self.liquid_unit + self.solid_unit
                and ingre.startswith('I') and ingre not in conversions["ConversionId"].tolist()):
                temp_dict = {}
                temp_dict.update(dict(row))
                items_nonstd.append(temp_dict)
        # Create a DataFrame from Items_Nonstd list
        items_nonstd = pd.DataFrame(items_nonstd, columns = col_names)
        # Remove duplicate ingredients of the same properties so that Items_Nonstd has unique rows.
        items_nonstd.drop_duplicates(subset=['IngredientId'], inplace=True,)
        for index, row in items_nonstd.iterrows():
            idx = row['IngredientId']
            filtered_items = items.loc[items['ItemId'] == idx, 'Description']
            if not filtered_items.empty:
                descrp = filtered_items.values[0]
                items_nonstd.loc[index, 'Description'] = descrp
            else:
                pass
        path = os.path.join(os.getcwd(), "data", "cleaning", "Items_Nonstd.csv")
        items_nonstd.to_csv(path, index = False, header = True)
        return items_nonstd
    def __clean_preps(self) -> pd.DataFrame:
        """Updates the Preps Datafram with standard quantity and unit of measurement"""
        ##TODO: Update this function to update prep weight using ingredients DF
        preps = self.labeller.preps
        preps['StdQty'] = np.nan
        preps['StdUom'] = np.nan
        for index in preps.index:
            prepid = preps.loc[index,'PrepId']
            qty = preps.loc[index,'PakQty']
            uom = preps.loc[index,'PakUOM']
            standard_qty, standard_uom = self.__special_converter(prepid,qty,uom)
            preps.loc[index,'StdQty'] = standard_qty
            preps.loc[index,'StdUom'] = standard_uom
        self.nonstdpreps = self.__find_non_std_preps(preps)
        return preps

    def __find_non_std_preps(self, preps: pd.DataFrame) -> pd.DataFrame:
        """Finds non-standard preps in the preps dataframe"""
        col_names = list(preps.columns.values)
        preps_nonstd = []
        for index, row in preps.iterrows():
            stduom = preps.loc[index,'StdUom']
            if stduom not in ['g', 'ml']:
                temp_dict = {}
                temp_dict.update(dict(row))
                preps_nonstd.append(temp_dict)
        preps_nonstd = pd.DataFrame(preps_nonstd, columns = col_names)
        manual_prepu = pd.read_csv(os.path.join(os.getcwd(), "data", "cleaning",
                                                "update", "Preps_UpdateUom.csv"))
        col_names = list(preps_nonstd.columns.values)
        preps_nonstd_na = []
        for index, row in preps_nonstd.iterrows():
            prepid = preps_nonstd.loc[index,'PrepId']
            if prepid not in manual_prepu['PrepId'].values:
                temp_dict = {}
                temp_dict.update(dict(row))
                preps_nonstd_na.append(temp_dict)
        preps_nonstd = pd.DataFrame(preps_nonstd_na, columns = col_names)
        path = os.path.join(os.getcwd(), "data", "cleaning", "Preps_NonstdUom.csv")
        preps_nonstd.to_csv(path, index = False, header = True)
        return preps_nonstd
    def __find_new_items(self) -> pd.DataFrame:
        """
        Finds items in the items dataframe that have not
        been assigned a category
        """
        items_assigned = pd.read_csv(os.path.join(os.getcwd(), "data", "mapping",
                                                  "Items_List_Assigned.csv"))
        # Filter new items by itemID that are not in the database and output them in a dataframe
        items = self.labeller.items
        col_names = list(items.columns.values)
        new_items_list = []
        for index, row in items.iterrows():
            itemid = items.loc[index,'ItemId']
            if itemid not in items_assigned['ItemId'].values:
                temp_dict = {}
                temp_dict.update(dict(row))
                new_items_list.append(temp_dict)
        new_items = pd.DataFrame(new_items_list, columns = col_names)
        new_items.insert(1, "CategoryID", '')
        if not new_items.empty:
            return new_items
        return None

    def preprocessing(self) -> None:
        """Preprocesses the data"""
        self.__update_conversions()
        self.labeller.preps = self.__clean_preps()
        self.new_items = self.__find_new_items()
        self.nonstditems = self.__find_non_std_items()
    ## Mapping and updating data
    def __read_emissions_data(self) -> dict:
        """Read in constant emission data"""
        #Reading in GHGE data
        self.ghge_factors = pd.read_csv(os.path.join(os.getcwd(), "data",
                                                     "external", "ghge_factors.csv"))
        #Reading in Nitrogen lost data
        self.nitro_factors = pd.read_csv(os.path.join(os.getcwd(), "data",
                                                      "external", "nitrogen_factors.csv"))
        #Reading in Water use data
        self.water_factors = pd.read_csv(os.path.join(os.getcwd(), "data",
                                                      "external", "water_factors.csv"))
        #Read in Land use data and convert to m^2
        self.land_factors = pd.read_csv(os.path.join(os.getcwd(), "data",
                                                     "external", "land_factors.csv"))
        self.land_factors.rename(columns={'km^2 land use/kg product': 'Land Use (m^2)'},
                                 inplace=True)
        self.land_factors['Land Use (m^2)'] *= 1000
    def __read_update_data(self):
        """Read in updated data"""
        self.items_assigned = pd.read_csv(os.path.join(os.getcwd(), "data", "mapping",
                                                      "Items_List_Assigned.csv"))
        self.manual_prepu = pd.read_csv(os.path.join(os.getcwd(), "data", "cleaning",
                                                     "update", "Preps_UpdateUom.csv"))
        self.manual_factor = pd.read_csv(os.path.join(os.getcwd(), "data", "mapping",
                                                       "Manual_Adjust_Factors.csv"))
    def __update_preps(self) -> None:
        """Update the preps dataframe with new data"""
        for index, row in self.manual_prepu.iterrows():
            PrepId = self.manual_prepu.loc[index, 'PrepId']
            qty = self.manual_prepu.loc[index, 'StdQty']
            uom = self.manual_prepu.loc[index, 'StdUom']
            self.labeller.preps.loc[self.labeller.preps['PrepId'] == PrepId, 'StdQty'] = qty
            self.labeller.preps.loc[self.labeller.preps['PrepId'] == PrepId, 'StdUom'] = uom
        self.labeller.preps.drop_duplicates(subset=['PrepId'], inplace=True)
    def __update_items_assigned(self) -> None:
        """Update Items_Assigned with new items"""
        new_items_added = pd.read_csv(os.path.join(os.getcwd(), "data", "mapping", "new items added"
                                            ,"New_Items_2024", "New_Items_Added_2024-08-30.csv"))
        frames = [self.items_assigned, new_items_added]
        items_assigned_updated = pd.concat(frames).reset_index(
                                                    drop=True, inplace=False).drop_duplicates()
        items_assigned_updated[['CategoryID']] = items_assigned_updated[
                                                    ['CategoryID']].apply(pd.to_numeric)
        path = os.path.join(os.getcwd(), "data", "mapping", "Items_List_Assigned.csv")
        items_assigned_updated.to_csv(path, index=False, header=True)
        self.items_assigned = items_assigned_updated
    def __create_mapping(self) -> None:
        """Create a mapping between item and category"""
        items = self.labeller.items
        items_assigned = self.items_assigned
        items = items.merge(items_assigned, on='ItemId', how='left')
        items.drop_duplicates(subset=['ItemId'], inplace=True)
        
        mapping = pd.merge(items, self.ghge_factors[:,['Category ID','Food Category','Active Total Supply Chain Emissions (kg CO2 / kg food)']],
                           how = 'left',
                           left_on = 'CategoryID',
                           right_on = 'Category ID')
        
        mapping = mapping.drop(columns = ['Category ID', 'Food Category_x'])

        mapping = pd.merge(mapping, self.nitro_factors[:,['Category ID','Food Category','Nitrogen lost (kg N / kg food)']],
                            how = 'left',
                            left_on = 'CategoryID',
                            right_on = 'Category ID')
                
        mapping = mapping.drop(columns = ['Category ID', 'Food Category_y'])

        mapping = pd.merge(mapping, self.water_factors[:,['Category ID','Food Category','Water use (L / kg food)']],
                            how = 'left',
                            left_on = 'CategoryID',
                            right_on = 'Category ID')
                
        mapping = mapping.drop(columns = ['Category ID', 'Food Category'])

        mapping = pd.merge(mapping, self.land_factors[:,['Category ID','Food Category','Land Use (m^2)']],
                            how = 'left',
                            left_on = 'CategoryID',
                            right_on = 'Category ID')
                
        mapping = mapping.drop(columns = ['Category ID', 'Food Category'])

        for index in mapping.index:
            if np.isnan(mapping.loc[index, 'Category ID']):
                mapping.loc[index, 'Land Use (m^2)'] = 0
                mapping.loc[index, 'Water use (L / kg food)'] = 0
                mapping.loc[index, 'Nitrogen lost (kg N / kg food)'] = 0
                mapping.loc[index, 'Active Total Supply Chain Emissions (kg CO2 / kg food)'] = 0

        return mapping
    def identify_manual_adjustments(self) -> None:
        """Identify manual adjustments"""
        self.__read_emissions_data()
        self.__read_update_data()
        self.__update_preps()
        self.__update_items_assigned()
        self.mapping = self.__create_mapping()
        ## TODO
        ## Prompt user to input manual adjustments
    def check_ingredients_and_mapping(self) -> None:
        """Check if ingredients are in mapping"""
        map_list = self.mapping['ItemId'].unqiue()
        ingre_list = self.labeller.ingredients['IngredientId'].unique()
        absent_list = []

        for item in ingre_list:
            if item not in map_list and item.startswith('I'):
                absent_list.append(item)
        
        return len(absent_list) == 0
    ##Data Analysis
    

    
