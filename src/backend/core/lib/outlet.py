import pandas as pd
from src.backend.core.lib.labeller import Labeller
from src.backend.core.lib.product import Product
from src.backend.core.lib.ingredient import Ingredient
from src.backend.core.lib.item import Item
from src.backend.core.lib.prep import Prep


class Outlet:
    """
    Class representing all the data of an outlet

    Attributes:
        Name: String
        Owner: String
        Products: Product[]
        Preps: Prep[]
        Items: Item[]
    """
    preps: list[Prep]
    items: list[Item]

    def __init__(self, name: str, owner: str, products: list[Product]) -> None:
        self.name = name
        self.owner = owner
        self.products = products
        self.preps = []
        self.items = []
    ##Getters
    def get_name(self):
        """
        Get the name of the outlet
        """
        return self.name
    def get_owner(self):
        """
        Get the owner of the outlet
        """
        return self.owner
    def get_products(self):
        """
        Get the products of the outlet
        """
        return self.products
    def add_product(self, product: Product):
        """
        Add a product to the outlet
        """
        self.products.append(product)
    def add_products(self, filepath: list[str]):
        """
        Add products to the outlet from a file

        Input:
        filepath: String

        Output:
        None
        """
        labeller = Labeller(filepath, self.name)
        labeller.read_recipes()
        def create_item(item: pd.DataFrame):
            idx = item["ItemId"].values[0]
            for x in self.items:
                if x.idx == idx:
                    return x
            name = item["Description"].values[0]
            item_obj = Item(idx, name)
            self.items.append(item_obj)
            return item_obj
        def create_prep(prep : pd.DataFrame):
            idx = prep["PrepId"].values[0]
            for x in self.preps:
                if x.idx == idx:
                    return x
            name = prep["Description"].values[0]
            prep_ingredients = labeller.ingredients.loc[labeller.ingredients['Recipe'] == idx]
            prep_ingredients = create_ingredients(prep_ingredients)
            prep_weight = prep["PakQty"].values[0]
            prep_uom = prep["PakUOM"].values[0]
            prep_obj = Prep(idx, name, prep_ingredients, prep_weight, prep_uom)
            self.preps.append(prep_obj)
            return prep_obj
        def create_ingredients(ingredients: pd.DataFrame):
            ingredient_list = []
            try:
                for _,row in ingredients.iterrows():
                    if row["IngredientId"].startswith("I"):
                        item_data = labeller.items.loc[labeller.items['ItemId'] == row["IngredientId"]]
                        item = create_item(item_data)
                        ingredient = Ingredient(item.name, row["Qty"], row["Uom"], item)
                    elif row["IngredientId"].startswith("P"):
                        prep_data = labeller.preps.loc[labeller.preps['PrepId'] == row["IngredientId"]]
                        prep = create_prep(prep_data)
                        ingredient = Ingredient(prep.name, row["Qty"],row["Uom"] ,prep)
                    elif row["IngredientId"].startswith("R"):
                        prod_data = labeller.products.loc[labeller.products['ProdId'] == row["IngredientId"]]
                        prod = create_product(prod_data['ProdId'].values[0])
                        ingredient = Ingredient(prod.name, row["Qty"],row["Uom"] ,prod)
                    else:
                        print("Invalid Ingredient ID: ", row["IngredientId"])
                        continue
                    ingredient_list.append(ingredient)
            except KeyError as e:
                print("KeyError in creating ingredients: ", e)
                print("Row: ", row)
                print("Ingredients: ", ingredients)
            except ValueError as e:
                print("ValueError in creating ingredients: ", e)
                print("Row: ", row)
                print("Ingredients: ", ingredients)
            except TypeError as e:
                print("TypeError in creating ingredients: ", e)
                print("Row: ", row)
                print("Ingredients: ", ingredients)
            return ingredient_list
        def create_product(prodid: str):
            #Data from Products Dataframe
            prod_row = labeller.products.loc[labeller.products['ProdId'] == prodid]
            name = prod_row['Description'].values[0]
            #Data from Ingredients Dataframe
            ingredients = labeller.ingredients.loc[labeller.ingredients['Recipe'] == prodid]
            ingredients = create_ingredients(ingredients)
            return Product(prodid, name, ingredients)
        for _,row in labeller.products.iterrows():
            self.products.append(create_product(row['ProdId']))
    def remove_product(self, product: Product):
        """
        Remove a product from the outlet
        """
        self.products.remove(product)
    def __str__(self) -> str:
        """
        String representation of the Outlet class.
        """
        return self.name + " (" + self.owner+ ")"
    def to_dict(self) -> dict:
        """
        Convert the Outlet object to a dictionary
        """
        return {
            "name": self.name,
            "owner": self.owner,
            "products": [product.to_dict() for product in self.products],
            "preps": [prep.to_dict() for prep in self.preps],
            "items": [item.to_dict() for item in self.items]
        }
    
    