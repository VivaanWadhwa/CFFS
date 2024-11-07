from src.backend.core.lib.recipe import Recipe
import json

class Product(Recipe):
    """
    Class representing a Product

    Attributes:
    Inherits from Recipe
    Label: String
    """
    def __init__(self, idx: int, name: str, ingredients: list) -> None:
        """
        Constructor for Product class, calling the Recipe constructor and setting label.

        Input:
        idx: Integer
        name: String
        ingredients: list of Ingredient
        label: String
        
        Output:
        None
        """
        super().__init__(idx, name, ingredients)  # Initialize Recipe attributes
        self.label = None
        # self.label = label  # Initialize Product-specific attribute
    
    def set_label(self, label: str) -> None:
        """
        Function for setting the label of the product

        Input:
        label: String

        Output:
        None
        """
        self.label = label

    def get_ingredients(self):
        """
        Getter for the ingredients attribute.
        
        Input:
        None
        
        Output:
        List of Ingredients
        """
        return self.ingredients
    def to_dict(self):
        """
        Function to convert the Product object to a dictionary
        
        Input:
        None
        
        Output:
        Dictionary
        """
        d = super().to_dict()
        d["Label"] = self.label
        return d
    def from_json(self, data: str):
        """
        Function to convert a json string to a Product object
        
        Input:
        data: String: JSON String
        
        Output:
        None
        """
        d = json.loads(data)
        self.idx = d["idx"]
        self.name = d["name"]
        from src.backend.core.lib.ingredient import Ingredient
        self.ingredients = [Ingredient().from_json(ingredient) for ingredient in d["ingredients"]]
        self.label = d["label"]
        return self