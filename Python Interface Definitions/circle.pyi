from typing import Tuple

def area(radius: float) -> float:
    """Calculate the area of a circle with the given radius.

    Args:
        radius (float): The radius of the circle.

    Returns:
        float: The area of the circle.
    """
    ...

def circumference(radius: float) -> float:
    """Calculate the circumference of a circle with the given radius.

    Args:
        radius (float): The radius of the circle.

    Returns:
        float: The circumference of the circle.
    """
    ...

def radius_from_area(area: float) -> float:
    """Calculate the radius of a circle with the given area.

    Args:
        area (float): The area of the circle.

    Returns:
        float: The radius of the circle.
    """
    ...

def radius_from_circumference(circumference: float) -> float:
    """Calculate the radius of a circle with the given circumference.

    Args:
        circumference (float): The circumference of the circle.

    Returns:
        float: The radius of the circle.
    """
    ...

def circle_info(radius: float) -> Tuple[float, float]:
    """Calculate both the area and circumference of a circle with the given radius.

    Args:
        radius (float): The radius of the circle.

    Returns:
        Tuple[float, float]: A tuple containing the area and circumference of the circle.
    """
    ...
