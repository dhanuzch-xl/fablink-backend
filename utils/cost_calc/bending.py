import math
from pprint import pprint

# Global Constants for Bending
BENDING_MACHINE_RATE_INR = 800  # INR per hour for machine
LABOR_RATE_INR_PER_HOUR = 500  # INR per hour for labor
SETUP_TIME_MIN = 10  # Setup time in minutes per batch
BENDING_SPEED_M_PER_MIN = 0.5  # Meters per minute (bending rate)

def calculate_bending_time_min(bend_length_m, num_bends):
    """
    Calculate the total bending time based on bend length and number of bends.

    Parameters:
    - bend_length_m: Length of a single bend in meters
    - num_bends: Number of bends per part

    Returns:
    - Total bending time in minutes.
    """
    total_time_min = (bend_length_m * num_bends) / BENDING_SPEED_M_PER_MIN
    return round(total_time_min, 2)

def calculate_bending_cost_inr(bending_time_min, quantity):
    """
    Calculate the total bending cost based on operational and labor costs.

    Parameters:
    - bending_time_min: Bending time per part in minutes
    - quantity: Number of parts to be bent

    Returns:
    - Total bending cost in INR.
    """
    total_time_in_hours = (bending_time_min * quantity + SETUP_TIME_MIN) / 60
    machine_cost_inr = total_time_in_hours * BENDING_MACHINE_RATE_INR
    labor_cost_inr = total_time_in_hours * LABOR_RATE_INR_PER_HOUR
    total_cost_inr = machine_cost_inr + labor_cost_inr
    return round(total_cost_inr, 2)

def calculate_bending_for_item(item):
    """
    Calculate the bending costs for a given item.

    Parameters:
    - item: Dictionary containing part details.

    Returns:
    - Dictionary with customer and internal-use information.
    """
    bend_length_m = item["bend_length_m"]
    num_bends = item["num_bends"]
    quantity = item["quantity"]

    # Calculate bending time and cost
    bending_time_min = calculate_bending_time_min(bend_length_m, num_bends)
    bending_cost_inr = calculate_bending_cost_inr(bending_time_min, quantity)

    result = {
        "customer_info": {
            "bending_cost_inr": bending_cost_inr,
        },
        "internal_use": {
            "bending_time_per_part_min": bending_time_min,
            "total_bending_time_min": bending_time_min * quantity + SETUP_TIME_MIN,
        }
    }

    return result

# Example Usage for Bending
if __name__ == "__main__":
    item = {
        "bend_length_m": 0.5,  # Length of each bend in meters
        "num_bends": 2,  # Number of bends per part
        "quantity": 100  # Number of parts
    }

    result = calculate_bending_for_item(item)

    pprint({
        "Customer Info": result["customer_info"],
        "Internal Use": result["internal_use"]
    })
