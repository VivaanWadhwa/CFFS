import pandas as pd
import os
import xml.etree.ElementTree as et
import labeller
import numpy as np
from typing import Tuple

class Calculator:
    new_items = None
    nonstdpreps = None
    nonstditems = None
    liquid_unit = None
    solid_unit = None

    def __init__(self, labeller_instance) -> None:
        self.labeller = labeller_instance

    ## Data Cleaning

    def assign_multiplier(self,df: pd.DataFrame) -> None:
        """Assigns a multiplier to each conversion in dataframe"""
        for ind, row in df.iterrows():
            if row["ConvertFromQty"] == 0 or row["ConvertToQty"] == 0:
                df.loc[ind, "Multiplier"] = 1
            else:
                df.loc[ind, "Multiplier"] = row["ConvertFromQty"] / row["ConvertToQty"]

    def preprocessing(self) -> None:
        """Preprocesses the data"""
        self.update_conversions()
        self.labeller.preps = self.clean_preps()
        self.new_items = self.find_new_items()
        self.nonstditems = self.find_non_std_items()


    def update_conversions(self) -> None:
        """Updates the existing conversions dataframe with the new one just read in"""
        conversions = self.labeller.conversions
        update_conv = pd.read_csv(os.path.join(os.getcwd(), "data", "cleaning", 
                                               "update", "Conv_UpdateConv.csv"))
        self.assign_multiplier(update_conv)
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
    def special_converter(self, ingre: str , qty: float, uom: str) -> Tuple[float, str]:
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
    
    def findNonStdItems(self) -> pd.DataFrame:
        Ingredients = self.labeller.Ingredients
        Conversions = self.labeller.Conversions
        Items = self.labeller.Items
        col_names = list(Ingredients.columns.values)
        # Create a Items_Nonstd list
        Items_Nonstd = []
        # If the unit of measurement is not grams or ml and ingredient id starts with I and the ingredient is not in ConversionId column of Conversions 
        # then we add it to Items_Nonstd list
        for index, row in Ingredients.iterrows():
            Ingre = Ingredients.loc[index,'IngredientId']
            Uom = Ingredients.loc[index,'Uom']
            if Uom not in ['g', 'ml'] and Uom not in self.liquid_unit + self.solid_unit and Ingre.startswith('I') and Ingre not in Conversions["ConversionId"].tolist():
                Dict = {}
                Dict.update(dict(row))
                Items_Nonstd.append(Dict)
        # Create a DataFrame from Items_Nonstd list
        Items_Nonstd = pd.DataFrame(Items_Nonstd, columns = col_names)
        # Remove duplicate ingredients of the same properties so that Items_Nonstd has only unique rows. 
        Items_Nonstd.drop_duplicates(subset=['IngredientId'], inplace=True,)
        for index, row in Items_Nonstd.iterrows():
            idx = row['IngredientId']
            filtered_items = Items.loc[Items['ItemId'] == idx, 'Description']
            if not filtered_items.empty:
                descrp = filtered_items.values[0]
                Items_Nonstd.loc[index, 'Description'] = descrp
            else:
                pass
        path = os.path.join(os.getcwd(), "data", "cleaning", "Items_Nonstd.csv")
        Items_Nonstd.to_csv(path, index = False, header = True)
        return Items_Nonstd
    
    def cleanPreps(self) -> pd.DataFrame:
        Preps = self.labeller.Preps
        Preps['StdQty'] = np.nan
        Preps['StdUom'] = np.nan
        for index in Preps.index:
            PrepId = Preps.loc[index,'PrepId']
            Qty = Preps.loc[index,'PakQty']
            Uom = Preps.loc[index,'PakUOM']
            Preps.loc[index,'StdQty'] = self.SpecialConverter(PrepId, Qty, Uom)[0]
            Preps.loc[index,'StdUom'] = self.SpecialConverter(PrepId, Qty, Uom)[1]
        self.NonStdPreps = self.findNonStdPreps(Preps)
        return Preps

    def findNonStdPreps(self, Preps) -> pd.DataFrame:
        col_names = list(Preps.columns.values)
        Preps_Nonstd = []
        for index, row in Preps.iterrows():
            StdUom = Preps.loc[index,'StdUom']
            if StdUom not in ['g', 'ml']:
                Dict = {}
                Dict.update(dict(row))
                Preps_Nonstd.append(Dict)
        Preps_Nonstd = pd.DataFrame(Preps_Nonstd, columns = col_names)
        Manual_PrepU = pd.read_csv(os.path.join(os.getcwd(), "data", "cleaning", "update", "Preps_UpdateUom.csv"))
        col_names = list(Preps_Nonstd.columns.values)
        Preps_Nonstd_na = []
        for index, row in Preps_Nonstd.iterrows():
            PrepId = Preps_Nonstd.loc[index,'PrepId']
            if PrepId not in Manual_PrepU['PrepId'].values:
                Dict = {}
                Dict.update(dict(row))
                Preps_Nonstd_na.append(Dict)
        Preps_Nonstd = pd.DataFrame(Preps_Nonstd_na, columns = col_names)
        path = os.path.join(os.getcwd(), "data", "cleaning", "Preps_NonstdUom.csv")
        Preps_Nonstd.to_csv(path, index = False, header = True)
        return Preps_Nonstd

    def findNewItems(self) -> pd.DataFrame:
        Items_Assigned = pd.read_csv(os.path.join(os.getcwd(), "data", "mapping", "Items_List_Assigned.csv"))
        # Filter new items by itemID that are not in the database and output them in a dataframe
        Items = self.labeller.Items
        col_names = list(Items.columns.values)
        New_Items_List = []
        for index, row in Items.iterrows():
            ItemId = Items.loc[index,'ItemId']
            if ItemId not in Items_Assigned['ItemId'].values:
                Dict = {}
                Dict.update(dict(row))
                New_Items_List.append(Dict)
        New_Items = pd.DataFrame(New_Items_List, columns = col_names)
        New_Items.insert(1, "CategoryID", '')
        if not New_Items.empty:
            return New_Items
        else:
            return None
    
    
    ## Mapping and updating data
    


