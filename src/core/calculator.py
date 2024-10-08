import pandas as pd
import os
import xml.etree.ElementTree as et
import labeller
import numpy as np
from typing import Tuple

class Calculator:
    New_Items = None
    NonStdPreps = None
    NonStdItems = None

    def __init__(self, labeller) -> None:
        self.labeller = labeller

    ## Data Cleaning

    def assign_multiplier(df):
        for ind, row in df.iterrows():
            if row["ConvertFromQty"] == 0 or row["ConvertToQty"] == 0:
                df.loc[ind, "Multiplier"] = 1
            else:
                df.loc[ind, "Multiplier"] = row["ConvertFromQty"] / row["ConvertToQty"]

    def preprocessing(self) -> None:
        self.updateConversions()
        self.labeller.Preps = self.cleanPreps()
        self.New_Items = self.findNewItems()
        self.NonStdItems = self.findNonStdItems()


    def updateConversions(self) -> None:
        Conversions = self.labeller.Conversions
        Update_Conv = pd.read_csv(os.path.join(os.getcwd(), "data", "cleaning", "update", "Conv_UpdateConv.csv"))
        self.assign_multiplier(Update_Conv)
        for index, row in Update_Conv.iterrows():
            Id = row['ConversionId'] 
            if Id in Conversions['ConversionId'].values:
                Conversions.drop(Conversions[Conversions['ConversionId'] == Id].index, inplace=True)
            else:
                print(f"Warning: 'ConversionId' {Id} not found in Conversions DataFrame. Skipping drop operation.")
        frames = [Conversions, Update_Conv]
        Conversions = pd.concat(frames).reset_index(drop=True, inplace=False).drop_duplicates()
        Update_Conv.to_csv(os.path.join(os.getcwd(), "data", "cleaning", "update", "Conv_UpdateConv.csv"), index=False)

    def SpecialConverter(self, ingre , qty, uom) -> Tuple[float, str]:
        Std_Unit = pd.read_csv(os.path.join(os.getcwd(), "data", "external", "standard_conversions.csv"))
        self.liquid_unit = Std_Unit.loc[Std_Unit['ConvertToUom'] == 'ml', 'ConvertFromUom'].tolist()
        self.solid_unit = Std_Unit.loc[Std_Unit['ConvertToUom'] == 'g', 'ConvertFromUom'].tolist()
        Conversions = self.labeller.Conversions

        def std_converter(qty, uom):
            if uom in Std_Unit['ConvertFromUom'].tolist():
                multiplier = Std_Unit.loc[Std_Unit['ConvertFromUom'] == uom, 'Multiplier']
                Qty = float(qty)*float(multiplier)
                Uom = Std_Unit.loc[Std_Unit['ConvertFromUom'] == uom, 'ConvertToUom'].values[0]
            else:
                Qty = qty
                Uom = uom
            return (Qty, Uom)
        
        spc_cov = list(filter(None, Conversions['ConversionId'].tolist()))
        if uom in self.liquid_unit + self.solid_unit:
            return std_converter(qty, uom)
        elif ingre in spc_cov:
            conversion = Conversions.loc[(Conversions['ConversionId'] == ingre) & (Conversions['ConvertFromUom'] == uom)
                                        & (Conversions['ConvertToUom'] == 'g')]
            multiplier = conversion['Multiplier']
            if multiplier.empty:
                return std_converter(qty, uom)
            else: 
                Qty = float(qty)/float(multiplier)
                Uom = conversion['ConvertToUom'].values[0]
                return (Qty, Uom)
        else:
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
    


