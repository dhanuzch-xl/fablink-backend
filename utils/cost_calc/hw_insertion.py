import math
from pprint import pprint

# Global Constants for Hardware Insertion and Tapping
INSERTION_MACHINE_RATE_INR = 800  # INR per hour for insertion machine
TAPPING_MACHINE_RATE_INR = 900  # INR per hour for tapping machine
LABOR_RATE_INR_PER_HOUR = 600  # INR per hour for labor
SETUP_TIME_MIN = 15  # Setup time in minutes per batch

# Insertion Parameters
INSERTION_TIME_PER_HARDWARE_MIN = 0.2  # Time to insert one piece of hardware (in minutes)
HARDWARE_COST_PER_UNIT_INR = 5  # Cost per hardware piece in INR

# Tapping Parameters
TAPPING_SPEED_HOLES_PER_MIN = 5  # Number of holes tapped per minute
CONSUMABLE_COST_PER_HOLE_INR = 2  # Cost per consumable for each tapped hole

def calculate_insertion_time_min(num_hardware):
    """
    Calculate the total time required for hardware insertion per part.

    Parameters:
    - num_hardware: Number of hardware pieces to be inserted per part.

    Returns:
    - Total insertion time per part in minutes.
    """
    total_time_min = num_hardware * INSERTION_TIME_PER_HARDWARE_MIN
    return round(total_time_min, 2)

def calculate_tapping_time_min(num_holes):
    """
    Calculate the total tapping time per part based on the number of holes.

    Parameters:
    - num_holes: Number of holes to be tapped per part.

    Returns:
    - Total tapping time per part in minutes.
    """
    total_time_min = num_holes / TAPPING_SPEED_HOLES_PER_MIN
    return round(total_time_min, 2)

def calculate_insertion_cost_inr(insertion_time_min, num_hardware, quantity):
    """
    Calculate the total hardware insertion cost.

    Parameters:
    - insertion_time_min: Time per part in minutes
    - num_hardware: Number of hardware pieces per part
    - quantity: Total number of parts

    Returns:
    - Total insertion cost in INR.
    """
    total_time_in_hours = (insertion_time_min * quantity + SETUP_TIME_MIN) / 60
    machine_cost_inr = total_time_in_hours * INSERTION_MACHINE_RATE_INR
    labor_cost_inr = total_time_in_hours * LABOR_RATE_INR_PER_HOUR
    hardware_cost_inr = num_hardware * quantity * HARDWARE_COST_PER_UNIT_INR
    total_cost_inr = machine_cost_inr + labor_cost_inr + hardware_cost_inr
    return round(total_cost_inr, 2)

def calculate_tapping_cost_inr(tapping_time_min, num_holes, quantity):
    """
    Calculate the total tapping cost.

    Parameters:
    - tapping_time_min: Time per part in minutes
    - num_holes: Number of holes per part
    - quantity: Total number of parts

    Returns:
    - Total tapping cost in INR.
    """
    total_time_in_hours = (tapping_time_min * quantity + SETUP_TIME_MIN) / 60
    machine_cost_inr = total_time_in_hours * TAPPING_MACHINE_RATE_INR
    labor_cost_inr = total_time_in_hours * LABOR_RATE_INR_PER_HOUR
    consumable_cost_inr = num_holes * quantity * CONSUMABLE_COST_PER_HOLE_INR
    total_cost_inr = machine_cost_inr + labor_cost_inr + consumable_cost_inr
    return round(total_cost_inr, 2)

def calculate_insertion_and_tapping_for_item(item):
    """
    Calculate the insertion and tapping costs for a given item.

    Parameters:
    - item: Dictionary containing part details.

    Returns:
    - Dictionary with customer and internal-use information.
    """
    num_hardware = item["num_hardware"]
    num_holes = item["num_holes"]
    quantity = item["quantity"]

    # Calculate insertion time and cost
    insertion_time_min = calculate_insertion_time_min(num_hardware)
    insertion_cost_inr = calculate_insertion_cost_inr(insertion_time_min, num_hardware, quantity)

    # Calculate tapping time and cost
    tapping_time_min = calculate_tapping_time_min(num_holes)
    tapping_cost_inr = calculate_tapping_cost_inr(tapping_time_min, num_holes, quantity)

    total_cost_inr = insertion_cost_inr + tapping_cost_inr

    result = {
        "customer_info": {
            "total_cost_inr": total_cost_inr,
            "insertion_cost_inr": insertion_cost_inr,
            "tapping_cost_inr": tapping_cost_inr,
        },
        "internal_use": {
            "insertion_time_per_part_min": insertion_time_min,
            "total_insertion_time_min": insertion_time_min * quantity + SETUP_TIME_MIN,
            "tapping_time_per_part_min": tapping_time_min,
            "total_tapping_time_min": tapping_time_min * quantity + SETUP_TIME_MIN,
        }
    }

    return result

# Example Usage for Insertion and Tapping
if __name__ == "__main__":
    item = {
        "num_hardware": 4,  # Number of hardware pieces per part
        "num_holes": 6,  # Number of holes to be tapped per part
        "quantity": 100  # Number of parts
    }

    result = calculate_insertion_and_tapping_for_item(item)

    pprint({
        "Customer Info": result["customer_info"],
        "Internal Use": result["internal_use"]
    })
