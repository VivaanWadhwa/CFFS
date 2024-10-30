class Ingredient:
    """
    Class for representing an ingredient of
    a recipe or a preparation.

    It can be one of the following:
    - Ingredient
    - Preparation
    """
    def __init__(self, name: str, item, quantity: int) -> None:
        """
        Constructor for the Ingredient class.

        Input:
        name: String
        item: Item
        quantity: Integer

        Output:
        None
        """
        self.name = name
        self.item = item
        self.quantity = quantity
