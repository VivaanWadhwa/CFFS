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
        uom: String: Unit of measurement

        Output:
        None
        """
        self.name = name
        self.quantity = quantity
        self.ingredient = ingredient
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
                "ingredient": self.ingredient.to_dict()}
    
