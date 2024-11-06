from src.backend.core.lib.recipe import Recipe

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
