import json

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
        self.ghg_emissions = 0
        self.water_use = 0
        self.stress_weighted_water_use = 0
        self.land_use = 0
        self.nitrogen_lost = 0
    
    def to_dict(self) -> dict:
        """
        Function to convert the Item object to a dictionary

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
                "nitrogen_lost": self.nitrogen_lost}
    def from_json(self, data: str) -> None:
        """
        Function to convert a JSON string to an Item object

        Input:
        data: String

        Output:
        None
        """
        data = json.loads(data)
        self.idx = data["idx"]
        self.name = data["name"]
        self.ghg_emissions = data["ghg_emissions"]
        self.water_use = data["water_use"]
        self.stress_weighted_water_use = data["stress_weighted_water_use"]
        self.land_use = data["land_use"]
        self.nitrogen_lost = data["nitrogen_lost"]
        