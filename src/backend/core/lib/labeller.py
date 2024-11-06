""""""
import glob
import os
import xml.etree.ElementTree as et
from typing import List, Optional
import pandas as pd
import logging

logging.basicConfig(level = logging.INFO, format = "%(asctime)s -- %(levelname)s - %(message)s")

class Labeller:
    """This class is designed for representing the preprocessed dataset"""
    filepaths = None
    items = None
    ingredients = None
    preps = None
    products = None
    conversions = None
    restaurant_name = None
    def __init__(self, filepath: List[str], restaurant) -> None:
        """Constructor for the Labeller class"""
        self.filepaths = self._validate_filepath(filepath)
        self.restaurant_name = restaurant
        self.items = pd.DataFrame()
        self.ingredients = pd.DataFrame()
        self.preps = pd.DataFrame()
        self.products = pd.DataFrame()
        self.conversions = pd.DataFrame()
        self.read_recipes()

    def __repr__(self) -> str:
        return (f"Labeller FOR {self.restaurant_name}\n"
                f"Items: {self.items.shape[0]}\n"
                f"Ingredients: {self.ingredients.shape[0]}\n"
                f"Preps: {self.preps.shape[0]}\n"
                f"Products: {self.products.shape[0]}\n"
                f"Conversions: {self.conversions.shape[0]}")

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def _validate_filepath(filepath: str) -> List[str]:
        """Function for validating the filepath"""
        if not isinstance(filepath, str):
            raise ValueError("Filepath should be a string.")
        if not os.path.isdir(filepath):
            raise FileNotFoundError("Filepath does not exist.")
        filepaths = glob.glob(os.path.join(filepath, "*.oc"))
        if not filepaths:
            raise FileNotFoundError("No OC files found in the directory.")
        return filepaths

    # def _read_xml_file(self, filename: str, tag: str) -> Optional[et.ElementTree]:
    #     """Function for parsing the XML File"""
    #     for filepath in self.filepaths:
    #         full_path = os.path.join(filepath, filename)
    #         if os.path.isfile(full_path):
    #             try:
    #                 return et.parse(full_path)
    #             except et.ParseError as e:
    #                 logging.error(f"Error parsing {filename}: {e}")
    #                 return None
    #     return None

    def read_items(self) -> None:
        """Function for reading in all items required for recipes"""
        # Read items.xml files in the filepath_list and construct a dataframe
        itemid = []
        description = []
        caseqty = []
        caseuom = []
        pakqty = []
        pakuom = []
        inventorygroup = []
        # from the items xml file, findtext of CaseQty, CaseUOM, PakQty, PakUOM, and InventoryGroup
        # then append it on the lists above
        for filepath in self.filepaths:
            path = filepath + '/Items.xml'
            if os.path.isfile(path):
                try:
                    xtree = et.parse(path)
                except et.ParseError as e:
                    logging.error("Error parsing Items.xml: %s", e)
                    raise e
                for item in xtree.iterfind('Item'):
                    itemid.append(item.attrib['id'])
                    description.append(item.findtext('Description'))
                    caseqty.append(item.findtext('CaseQty'))
                    caseuom.append(item.findtext('CaseUOM'))
                    pakqty.append(item.findtext('PakQty'))
                    pakuom.append(item.findtext('PakUOM'))
                    inventorygroup.append(item.findtext('InventoryGroup'))
        # Create a dataframe from the lists created above.
        self.items = pd.DataFrame({'ItemId': itemid,
                                   'Description': description,
                                   'CaseQty': caseqty,
                                   'CaseUOM': caseuom,
                                   'PakQty': pakqty,
                                   'PakUOM': pakuom,'InventoryGroup': inventorygroup})
        self._clean_dataframe(self.items, subset=["ItemId"])
    def read_ingredients(self) -> None:
        """Function for reading in all ingredients required for recipes"""
        # Read ingredients.xml files in the filepath_list and construct a dataframe
        ingredientid = []
        conversion = []
        invfactor = []
        qty = []
        recipe = []
        uom = []
        # Using the Ingredients XML file, we extract attributes containing ingredients,
        # conversion, invFactor, qty, recipe, and uom.
        # Then we append it onto the IngredientId, Coversion, InvFactor, Qty, Recipe, and Uom lists
        # Then we create a dataframe using the lists created.
        for filepath in self.filepaths:
            path = filepath + '/Ingredients.xml'
            if os.path.isfile(path):
                xtree = et.parse(path)
                for x in xtree.iterfind('Ingredient'):
                    ingredientid.append(x.attrib['ingredient'])
                    conversion.append(x.attrib['conversion'])
                    invfactor.append(x.attrib['invFactor'])
                    qty.append(x.attrib['qty'])
                    recipe.append(x.attrib['recipe'])
                    uom.append(x.attrib['uom'])
        self.ingredients = pd.DataFrame({'IngredientId': ingredientid,
                                         'Qty': qty,
                                         'Uom': uom,
                                         'Conversion': conversion,
                                         'InvFactor': invfactor,
                                         'Recipe': recipe}).drop_duplicates()
        self._clean_dataframe(self.ingredients, subset=["IngredientId", "Recipe"])
    def read_preps(self) -> None:
        """Function for reading in all preparations required for recipes"""
        prepid = []
        description = []
        pakqty = []
        pakuom = []
        inventorygroup = []
        for filepath in self.filepaths:
            path = filepath + '/Preps.xml'
            if os.path.isfile(path):
                xtree = et.parse(path)
                for x in xtree.iterfind('Prep'):
                    prepid.append(x.attrib['id'])
                    description.append(x.findtext('Description'))
                    pakqty.append(x.findtext('PakQty'))
                    pakuom.append(x.findtext('PakUOM'))
                    inventorygroup.append(x.findtext('InventoryGroup'))
        self.preps = pd.DataFrame({'PrepId': prepid,
                                   'Description': description,
                                   'PakQty': pakqty,
                                   'PakUOM':pakuom,
                                   'InventoryGroup': inventorygroup}).drop_duplicates()
        self._clean_dataframe(self.preps, subset=["PrepId"])
    def read_products(self) -> None:
        """Function for reading in all recipes Names"""
        prodid = []
        description = []
        salesgroup = []
        for filepath in self.filepaths:
            path = filepath + '/Products.xml'
            if os.path.isfile(path):
                xtree = et.parse(path)
                for x in xtree.iterfind('Prod'):
                    prodid.append(x.attrib['id'])
                    description.append(x.findtext('Description'))
                    salesgroup.append(x.findtext('SalesGroup'))
        self.products = pd.DataFrame({'ProdId': prodid,
                                      'Description': description,
                                      'SalesGroup': salesgroup})
        self._clean_dataframe(self.products, subset=["ProdId"])
    def read_conversions(self) -> None:
        """Function for reading in all conversions required for recipes"""
        conversionid = []
        multiplier = []
        convertfromqty = []
        convertfromuom = []
        converttoqty = []
        converttouom = []
        for filepath in self.filepaths:
            path = filepath + '/Conversions.xml'
            if os.path.isfile(path):
                xtree = et.parse(path)
                for x in xtree.iterfind('Conversion'):
                    conversionid.append(x.attrib['id'])
                    multiplier.append(x.attrib['multiplier'])
                    convertfromqty.append(x.find('ConvertFrom').attrib['qty'])
                    convertfromuom.append(x.find('ConvertFrom').attrib['uom'])
                    converttoqty.append(x.find('ConvertTo').attrib['qty'])
                    converttouom.append(x.find('ConvertTo').attrib['uom'])
        self.conversions = pd.DataFrame({'ConversionId': conversionid, 'Multiplier': multiplier,
                                        'ConvertFromQty': convertfromqty,
                                        'ConvertFromUom': convertfromuom,
                                        'ConvertToQty': converttoqty,
                                        'ConvertToUom': converttouom}
                                ).drop_duplicates()
        self._clean_dataframe(self.conversions)
  
    def _clean_dataframe(self, df: pd.DataFrame, subset: Optional[List[str]] = None) -> None:
        """Function for cleaning the dataframe"""
        df.drop_duplicates(subset=subset, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.dropna(inplace=True)
    def read_recipes(self):
        """Function for reading in all recipes"""
        self.read_items()
        self.read_ingredients()
        self.read_preps()
        self.read_products()
        self.read_conversions()
