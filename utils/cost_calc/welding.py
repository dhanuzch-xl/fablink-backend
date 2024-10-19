import math
from pprint import pprint

# Global Constants for Welding
WELDING_SPEED_M_PER_MIN = 0.2  # Meters per minute (welding rate)
WELDING_MACHINE_RATE_INR = 1000  # INR per hour for machine
LABOR_RATE_INR_PER_HOUR = 600  # INR per hour for labor
SETUP_TIME_MIN = 15  # Setup time in minutes per batch
CONSUMABLE_COST_PER_METER_INR = 50  # Cost of welding consumables per meter of weld

def calculate_welding_time_min(weld_length_m):
    """
    Calculate the total welding time based on weld length.

    Parameters:
    - weld_length_m: Length of the weld in meters

    Returns:
    - Total welding time in minutes.
    """
    total_time_min = weld_length_m / WELDING_SPEED_M_PER_MIN
    return round(total_time_min, 2)

def calculate_welding_cost_inr(welding_time_min, weld_length_m, quantity):
    """
    Calculate the total welding cost including operational and consumable costs.

    Parameters:
    - welding_time_min: Welding time per part in minutes
    - weld_length_m: Length of the weld in meters
    - quantity: Number of parts to be welded

    Returns:
    - Total welding cost in INR.
    """
    total_time_in_hours = (welding_time_min * quantity + SETUP_TIME_MIN) / 60
    machine_cost_inr = total_time_in_hours * WELDING_MACHINE_RATE_INR
    labor_cost_inr = total_time_in_hours * LABOR_RATE_INR_PER_HOUR
    consumable_cost_inr = weld_length_m * quantity * CONSUMABLE_COST_PER_METER_INR
    total_cost_inr = machine_cost_inr + labor_cost_inr + consumable_cost_inr
    return round(total_cost_inr, 2)

def calculate_welding_for_item(item):
    """
    Calculate the welding costs for a given item.

    Parameters:
    - item: Dictionary containing part details.

    Returns:
    - Dictionary with customer and internal-use information.
    """
    weld_length_m = item["weld_length_m"]
    quantity = item["quantity"]

    # Calculate welding time and cost
    welding_time_min = calculate_welding_time_min(weld_length_m)
    welding_cost_inr = calculate_welding_cost_inr(welding_time_min, weld_length_m, quantity)

    result = {
        "customer_info": {
            "welding_cost_inr": welding_cost_inr,
        },
        "internal_use": {
            "welding_time_per_part_min": welding_time_min,
            "total_welding_time_min": welding_time_min * quantity + SETUP_TIME_MIN,
        }
    }

    return result

# Example Usage for Welding
if __name__ == "__main__":
    item = {
        "weld_length_m": 0.8,  # Length of each weld in meters
        "quantity": 50  # Number of parts
    }

    result = calculate_welding_for_item(item)

    pprint({
        "Customer Info": result["customer_info"],
        "Internal Use": result["internal_use"]
    })
