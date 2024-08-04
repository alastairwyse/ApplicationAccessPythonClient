from enum import Enum

class ApplicationScreen(Enum):
    """Represents different screens within an application.
    """
    order = 0,
    summary = 1,
    manage_products = 2,
    settings = 3, 
    delivery = 4, 
    review = 5