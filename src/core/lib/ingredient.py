class Ingredient:
    """
    Class for representing an ingredient of
    a recipe or a preparation.

    It can be one of the following:
    - Ingredient
    - Preparation
    """
    def __init__(self, name: str, quantity: int, ingredient) -> None:
        """
        Constructor for the Ingredient class.

        Input:
        name: String
        quantity: Integer
        Ingredient: one of Item or Prep

        Output:
        None
        """
        self.name = name
        self.quantity = quantity
        self.ingredient = ingredient
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
