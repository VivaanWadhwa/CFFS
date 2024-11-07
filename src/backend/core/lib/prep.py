from src.backend.core.lib.recipe import Recipe
import json

class Prep(Recipe):
    """"
    Class representing a Preparation

    Inherits from Recipe
    """
    def __init__(self, idx: int, name: str, ingredients, qty: int, uom: str) -> None:
        super().__init__(idx, name, ingredients)
        self.qty = qty
        self.uom = uom
    def to_dict(self) -> dict:
        """
        Function to convert the Prep object to a dictionary

        Input:
        None

        Output:
        Dictionary
        """
        d = super().to_dict()
        d["qty"] = self.qty
        d["uom"] = self.uom
        return d
    def from_json(self, data: str) -> None:
        """
        Function to convert a json string to a Prep object

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
        self.qty = d["qty"]
        self.uom = d["uom"]

    