from src.core.recipe import Recipe
from src.core.ingredient import Ingredient

class Product(Recipe):
    """
    Class representing a Product

    Attributes:
    Inherits from Recipe
    Label: String
    """
    def __init__(self, idx: int, name: str, ingredients: list[Ingredient], label: str) -> None:
        """
        Constructor for the Product class.

        Input:
        idx: Integer
        name: String
        ingredients: Ingredient[]

        Output:
        None
        """
        super().__init__(idx, name, ingredients)
        self.label = label