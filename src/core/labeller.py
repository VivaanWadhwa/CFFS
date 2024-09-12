import pandas as pd
import os
import xml.etree.ElementTree as et

class Labeller:
    filepath = None
    Items = None
    Ingredients = None
    Preps = None
    Products = None
    Conversions = None

    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.readRecipes()
    
    def readItems(self) -> None:
        # Read items.xml files in the filepath_list and construct a dataframe
        ItemId = []
        Description = []
        CaseQty = []
        CaseUOM = []
        PakQty = []
        PakUOM = []
        InventoryGroup = []
        # from the items xml file, findtext of CaseQty, CaseUOM, PakQty, PakUOM, and InventoryGroup
        # then append it on the lists above
        for filepath in self.filepath:
            path = filepath + '/Items.xml'
            if os.path.isfile(path):
                xtree = et.parse(path)
                xroot = xtree.getroot()
                for item in xtree.iterfind('Item'):
                    ItemId.append(item.attrib['id'])
                    Description.append(item.findtext('Description'))
                    CaseQty.append(item.findtext('CaseQty'))
                    CaseUOM.append(item.findtext('CaseUOM'))
                    PakQty.append(item.findtext('PakQty'))
                    PakUOM.append(item.findtext('PakUOM'))
                    InventoryGroup.append(item.findtext('InventoryGroup'))
        # Create a dataframe from the lists created above.
        self.Items = pd.DataFrame({'ItemId': ItemId, 'Description': Description, 'CaseQty': CaseQty, 
                            'CaseUOM': CaseUOM, 'PakQty': PakQty, 'PakUOM': PakUOM, 'InventoryGroup': InventoryGroup}
                            )
        self.Items.drop_duplicates(inplace=True)
        self.Items.reset_index(drop=True, inplace=True)

    def readIngredients(self) -> None:
        # Read ingredients.xml files in the filepath_list and construct a dataframe
        IngredientId = []
        Conversion = []
        InvFactor = []
        Qty = []
        Recipe = []
        Uom = []
        # Using the Ingredients XML file, we extract attributes containing ingredients, conversion, invFactor, qty, recipe, and uom. 
        # Then we append it onto the IngredientId, Coversion, InvFactor, Qty, Recipe, and Uom lists
        # Then we create a dataframe using the lists created. 
        for filepath in self.filepath:
            path = filepath + '/Ingredients.xml'
            if os.path.isfile(path):
                xtree = et.parse(path)
                xroot = xtree.getroot()
                for x in xtree.iterfind('Ingredient'):
                    IngredientId.append(x.attrib['ingredient'])
                    Conversion.append(x.attrib['conversion'])
                    InvFactor.append(x.attrib['invFactor'])
                    Qty.append(x.attrib['qty'])
                    Recipe.append(x.attrib['recipe'])
                    Uom.append(x.attrib['uom'])            
        self.Ingredients = pd.DataFrame({'IngredientId': IngredientId, 'Qty': Qty,'Uom': Uom, 'Conversion': Conversion, 
                            'InvFactor': InvFactor,'Recipe': Recipe}).drop_duplicates()
        self.Ingredients.drop_duplicates(subset=["IngredientId", "Recipe"], inplace=True)
        self.Ingredients.reset_index(drop=True, inplace=True)
    
    def readPreps(self) -> None:
        PrepId = []
        Description = []
        PakQty = []
        PakUOM = []
        InventoryGroup = []
        for filepath in self.filepath:
            path = filepath + '/Preps.xml'
            if os.path.isfile(path):
                xtree = et.parse(path)
                xroot = xtree.getroot()
                for x in xtree.iterfind('Prep'):
                    PrepId.append(x.attrib['id'])
                    Description.append(x.findtext('Description'))
                    PakQty.append(x.findtext('PakQty'))
                    PakUOM.append(x.findtext('PakUOM'))
                    InventoryGroup.append(x.findtext('InventoryGroup'))
        self.Preps = pd.DataFrame({'PrepId': PrepId, 'Description': Description,
                        'PakQty': PakQty, 'PakUOM':PakUOM, 'InventoryGroup': InventoryGroup}).drop_duplicates()
        preps_columns = self.Preps.columns
        self.Preps.drop_duplicates(subset=["PrepId"], inplace=True)
        self.Preps.reset_index(drop=True, inplace=True)
    
    def readProducts(self) -> None:
        # Read products.xml files in the filepath_list and construct a dataframe
        ProdId = []
        Description = []
        SalesGroup = []
        for filepath in self.filepath:
            path = filepath + '/Products.xml'
            if os.path.isfile(path):
                xtree = et.parse(path)
                xroot = xtree.getroot()
                for x in xtree.iterfind('Prod'):
                    ProdId.append(x.attrib['id'])
                    Description.append(x.findtext('Description'))
                    SalesGroup.append(x.findtext('SalesGroup'))
        self.Products = pd.DataFrame({'ProdId': ProdId, 'Description': Description, 'SalesGroup': SalesGroup})
        self.Products.drop_duplicates(inplace=True)
        self.Products.reset_index(drop=True, inplace=True)

    def readConversions(self) -> None:
        ConversionId = []
        Multiplier = []
        ConvertFromQty = []
        ConvertFromUom = []
        ConvertToQty = []
        ConvertToUom = []
        for filepath in self.filepath:
            path = filepath + '/Conversions.xml'
            if os.path.isfile(path):
                xtree = et.parse(path)
                xroot = xtree.getroot()
                for x in xtree.iterfind('Conversion'):
                    ConversionId.append(x.attrib['id'])
                    Multiplier.append(x.attrib['multiplier'])
                    ConvertFromQty.append(x.find('ConvertFrom').attrib['qty'])
                    ConvertFromUom.append(x.find('ConvertFrom').attrib['uom'])
                    ConvertToQty.append(x.find('ConvertTo').attrib['qty'])
                    ConvertToUom.append(x.find('ConvertTo').attrib['uom'])
        self.Conversions = pd.DataFrame({'ConversionId': ConversionId, 'Multiplier': Multiplier, 'ConvertFromQty': ConvertFromQty,
                                'ConvertFromUom': ConvertFromUom, 'ConvertToQty': ConvertToQty, 'ConvertToUom': ConvertToUom}
                                ).drop_duplicates()
        self.Conversions.reset_index(drop=True, inplace=True)

    def readRecipes(self):
        self.readItems()
        self.readIngredients()
        self.readPreps()
        self.readProducts()
        self.readConversions()

