import numpy as np

class Item:
    """
    Class representing an Item

    Attributes:
        Optimum Control ID: Integer
        Name: String
        Category ID: Integer
        GHG Emissions: float
        Water Use: float
        Stress Weighted Water Use: float
        Land Use: float
        Nitrogen Lost: float
    """
    def __init__(self, idx: int, name: str) -> None:
        """
        Constructor for the Item class.

        Input:
        idx: Integer
        name: String
        category_id: Integer

        Output:
        None
        """
        self.idx = idx
        self.name = name
        self.ghg_emissions = np.nan
        self.water_use = np.nan
        self.stress_weighted_water_use = np.nan
        self.land_use = np.nan
        self.nitrogen_lost = np.nan
        