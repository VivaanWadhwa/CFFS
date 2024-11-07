import json

class Recipe:
    """
    Class representing a recipe.

    Attributes:
    Optimum Control ID: Integer
    Name: String
    GHG Emissions: float
    Water use: float
    Stress Weighted Water Use: float
    Land Use: float
    Nitrogen Lost: float
    Ingredients: Ingredient[]
    """
    def __init__(self, idx: int, name: str, ingredients) -> None:
        """
        Constructor for the Recipe class.

        Input:
        idx: Integer
        name: String
        ingredients: Ingredient[]

        Output:
        None
        """
        self.idx = idx
        self.name = name
        self.ingredients = ingredients
        self.ghg_emissions = 0
        self.water_use = 0
        self.stress_weighted_water_use = 0
        self.land_use = 0
        self.nitrogen_lost = 0
    def __str__(self) -> str:
        """
        String representation of the Recipe class.

        Input:
        None

        Output:
        String
        """
        return (f"OC ID: {self.idx}\n"
                f"Recipe Name: {self.name}\n"
                f"GHG Emissions: {self.ghg_emissions}\n"
                f"Water Use: {self.water_use}\n"
                f"Stress Weighted Water Use: {self.stress_weighted_water_use}\n"
                f"Land Use: {self.land_use}\n"
                f"Nitrogen Lost: {self.nitrogen_lost}\n"
                f"Number of ingredients: {len(self.ingredients)}\n")
    def __repr__(self) -> str:
        return self.__str__()
    # def set_label(self, label: str) -> None:
    #     """
    #     Setter for the label attribute.
         
    #     Input:
    #     label: String
        
    #     Output:
    #     None
    #     """
    #     self.label = label
    def set_emissions(self, ghg: float, water_use: float, stress_water_use: float, land_use: float, nitrogen_lost: float) -> None:
        """
        Setter for the ghg_emissions attribute.
        
        Input:
        ghg: float
        
        Output:
        None
        """
        self.ghg_emissions = ghg
        self.water_use = water_use
        self.stress_weighted_water_use = stress_water_use
        self.land_use = land_use
        self.nitrogen_lost = nitrogen_lost
    def get_emissions(self) -> dict[str, float]:
        """
        Getter for the ghg_emissions attribute.
        
        Input:
        None
        
        Output:
        Dictionary of Emissions
        """
        return {"GHG Emissions": self.ghg_emissions, "Water Use": self.water_use, "Stress Weighted Water Use": self.stress_weighted_water_use, "Land Use": self.land_use, "Nitrogen Lost": self.nitrogen_lost}
    def to_dict(self) -> dict:
        """
        Function to convert the Recipe object to a dictionary

        Input:
        None

        Output:
        Dictionary
        """
        return {"idx": self.idx,
                "name": self.name,
                "ghg_emissions": self.ghg_emissions,
                "water_use": self.water_use,
                "stress_weighted_water_use": self.stress_weighted_water_use,
                "land_use": self.land_use,
                "nitrogen_lost": self.nitrogen_lost,
                "ingredients": [ingredient.to_dict() for ingredient in self.ingredients]}
