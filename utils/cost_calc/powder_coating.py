import math
from pprint import pprint

# Global Constants for Powder Coating
COATING_MACHINE_RATE_INR = 1200  # INR per hour for the coating machine
LABOR_RATE_INR_PER_HOUR = 500  # INR per hour for labor
SETUP_TIME_MIN = 20  # Setup time in minutes per batch
COATING_SPEED_M2_PER_MIN = 1.0  # Square meters coated per minute
CONSUMABLE_COST_PER_M2_INR = 15  # Powder cost per square meter

def calculate_coating_time_min(area_m2):
    """
    Calculate the total powder coating time per part based on the surface area.

    Parameters:
    - area_m2: Surface area of the part in square meters.

    Returns:
    - Total coating time per part in minutes.
    """
    total_time_min = area_m2 / COATING_SPEED_M2_PER_MIN
    return round(total_time_min, 2)

def calculate_coating_cost_inr(coating_time_min, area_m2, quantity):
    """
    Calculate the total powder coating cost for the batch.

    Parameters:
    - coating_time_min: Coating time per part in minutes.
    - area_m2: Surface area of each part in square meters.
    - quantity: Total number of parts.

    Returns:
    - Total powder coating cost in INR.
    """
    total_time_in_hours = (coating_time_min * quantity + SETUP_TIME_MIN) / 60
    machine_cost_inr = total_time_in_hours * COATING_MACHINE_RATE_INR
    labor_cost_inr = total_time_in_hours * LABOR_RATE_INR_PER_HOUR
    consumable_cost_inr = area_m2 * quantity * CONSUMABLE_COST_PER_M2_INR
    total_cost_inr = machine_cost_inr + labor_cost_inr + consumable_cost_inr
    return round(total_cost_inr, 2)

def calculate_coating_for_item(item):
    """
    Calculate the powder coating costs for a given item.

    Parameters:
    - item: Dictionary containing part details.

    Returns:
    - Dictionary with customer and internal-use information.
    """
    area_m2 = item["area_m2"]
    quantity = item["quantity"]

    # Calculate coating time and cost
    coating_time_min = calculate_coating_time_min(area_m2)
    coating_cost_inr = calculate_coating_cost_inr(coating_time_min, area_m2, quantity)

    result = {
        "customer_info": {
            "coating_cost_inr": coating_cost_inr,
        },
        "internal_use": {
            "coating_time_per_part_min": coating_time_min,
            "total_coating_time_min": coating_time_min * quantity + SETUP_TIME_MIN,
        }
    }

    return result

# Example Usage for Powder Coating
if __name__ == "__main__":
    item = {
        "area_m2": 0.75,  # Surface area per part in square meters
        "quantity": 100  # Number of parts
    }

    result = calculate_coating_for_item(item)

    pprint({
        "Customer Info": result["customer_info"],
        "Internal Use": result["internal_use"]
    })
