import json
from src.backend.core.lib.item import Item
from src.backend.core.lib.prep import Prep

class Ingredient:
    """
    Class for representing an ingredient of
    a recipe or a preparation.

    It can be one of the following:
    - Ingredient
    - Preparation
    """
    def __init__(self, name: str, quantity: int, uom: str, ingredient) -> None:
        """
        Constructor for the Ingredient class.

        Input:
        name: String: Name of the ingredient
        quantity: Integer: Quantity of the ingredient
        Ingredient: one of Item or Prep: Ingredient object
        Ingredient_type: String: Type of the ingredient
        uom: String: Unit of measurement

        Output:
        None
        """
        self.name = name
        self.quantity = quantity
        self.ingredient = ingredient
        self.ingredient_type = type(ingredient).__name__
        self.uom = uom
    def __str__(self) -> str:
        """
        String representation of the Ingredient class.

        Input:
        None

        Output:
        String
        """
        return (f"Ingredient: {self.name}\n"
                f"Quantity: {self.quantity}\n"
                f"Type: {type(self.ingredient).__name__}\n")
    def __repr__(self) -> str:
        return self.__str__()
    def to_dict(self) -> dict:
        """
        Function to convert the Ingredient object to a dictionary

        Input:
        None

        Output:
        Dictionary
        """
        return {"name": self.name,
                "quantity": self.quantity,
                "uom": self.uom,
                "ingredient_type": self.ingredient_type,
                "ingredient": self.ingredient.to_dict()}
    def from_json(self, data: str) -> None:
        """
        Function to convert a JSON string to an Ingredient object

        Input:
        data: String: JSON string

        Output:
        None
        """
        data = json.loads(data)
        self.name = data["name"]
        self.quantity = data["quantity"]
        self.uom = data["uom"]
        self.ingredient_type = data["ingredient_type"]
        if self.ingredient_type == "Item":
            self.ingredient = Item()
            self.ingredient.from_json(json.dumps(data["ingredient"]))
        elif self.ingredient_type == "Prep":
            self.ingredient = Prep()
            self.ingredient.from_json(json.dumps(data["ingredient"]))
        else:
            raise ValueError("Invalid ingredient type")
