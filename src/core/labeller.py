"""Modules for reading xml files and creating dataframes from them"""
import os
import xml.etree.ElementTree as et
from typing import List
import pandas as pd


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
        for path in filepath:
            if not os.path.isdir(path):
                raise FileNotFoundError(f"The path provided does not exist: {path}")
        self.filepaths = filepath
        self.restaurant_name = restaurant
        self.read_recipes()
    def __repr__(self) -> str:
        string = f"Labeller FOR {self.restaurant_name}\nItems: {self.items.shape[0]}\nIngredients: {self.ingredients.shape[0]}\nPreps: {self.preps.shape[0]}\nProducts: {self.products.shape[0]}\nConversions: {self.conversions.shape[0]}"
        return string
    def __str__(self) -> str:
        string = f"""
        Labeller FOR {self.restaurant_name}
        Items: {self.items.shape[0]}
        Ingredients: {self.ingredients.shape[0]}
        Preps: {self.preps.shape[0]}
        Products: {self.products.shape[0]}
        Conversions: {self.conversions.shape[0]}
        """
        return string

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
                xtree = et.parse(path)
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
        self.items.drop_duplicates(inplace=True)
        self.items.reset_index(drop=True, inplace=True)
        self.items.dropna(inplace=True)
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
        self.ingredients.drop_duplicates(subset=["IngredientId", "Recipe"], inplace=True)
        self.ingredients.reset_index(drop=True, inplace=True)
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
        self.preps.drop_duplicates(subset=["PrepId"], inplace=True)
        self.preps.reset_index(drop=True, inplace=True)
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
        self.products.drop_duplicates(inplace=True)
        self.products.reset_index(drop=True, inplace=True)
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
        self.conversions.reset_index(drop=True, inplace=True)
    def read_recipes(self):
        """Function for reading in all recipes"""
        self.read_items()
        self.read_ingredients()
        self.read_preps()
        self.read_products()
        self.read_conversions()
