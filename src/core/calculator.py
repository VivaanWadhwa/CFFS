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
    def preprocessing(self) -> None:
        """Preprocesses the data"""
        self.__update_conversions()
        self.labeller.preps = self.__clean_preps()
        self.new_items = self.__find_new_items()
        self.nonstditems = self.__find_non_std_items()
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
    ## Mapping and updating data
    
