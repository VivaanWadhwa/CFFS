import os
from labeller import Labeller
from product import Product
from ingredient import Ingredient
from item import Item
from prep import Prep

class Outlet:
    """
    Class representing all the data of an outlet

    Attributes:
        Name: String
        Owner: String
        Products: Product[]
    """

    def __init__(self, name, owner, products):
        self.name = name
        self.owner = owner
        self.products = products
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
    def add_product(self, product):
        """
        Add a product to the outlet
        """
        self.products.append(product)
    def add_products(self, filepath):
        """
        Add products to the outlet from a file

        Input:
        filepath: String

        Output:
        None
        """
        labeller = Labeller(filepath, self.name)
        labeller.read_recipes()
        def create_item(item):
            idx = item["ItemId"].values[0]
            name = item["Description"].values[0]
            return Item(idx, name)
        def create_prep(prep):
            idx = prep["PrepId"].values[0]
            name = prep["Description"].values[0]
            prep_ingredients = labeller.ingredients.loc[labeller.ingredients['Recipe'] == idx]
            prep_ingredients = create_ingredients(prep_ingredients)
            return Prep(idx, name, prep_ingredients)
        def create_ingredients(ingredients):
            ingredient_list = []
            try:
                for _,row in ingredients.iterrows():
                    if row["IngredientId"].startswith("I"):
                        item_data = labeller.items.loc[labeller.items['ItemId'] == row["IngredientId"]]
                        item = create_item(item_data)
                        ingredient = Ingredient(item.name, row["Qty"], item)
                    elif row["IngredientId"].startswith("P"):
                        prep_data = labeller.preps.loc[labeller.preps['PrepId'] == row["IngredientId"]]
                        prep = create_prep(prep_data)
                        ingredient = Ingredient(prep.name, row["Qty"], prep)
                    elif row["IngredientId"].startswith("R"):
                        prod_data = labeller.products.loc[labeller.products['ProdId'] == row["IngredientId"]]
                        prod = create_product(prod_data['ProdId'].values[0])
                        ingredient = Ingredient(prod.name, row["Qty"], prod)
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
        def create_product(prodID):
            #Data from Products Dataframe
            Prod_row = labeller.products.loc[labeller.products['ProdId'] == prodID]
            name = Prod_row['Description'].values[0]
            #Data from Ingredients Dataframe
            ingredients = labeller.ingredients.loc[labeller.ingredients['Recipe'] == prodID]
            ingredients = create_ingredients(ingredients)
            return Product(prodID, name, ingredients)
        for _,row in labeller.products.iterrows():
            self.products.append(create_product(row['ProdId']))
    def remove_product(self, product):
        """
        Remove a product from the outlet
        """
        self.products.remove(product)
    def __str__(self):
        return self.name + " (" + self.owner+ ")"
    
    