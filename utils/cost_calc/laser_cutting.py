import math
from pprint import pprint


# for user logic


# for business logic
def calculate_laser_cutting_cost_inr(length_m, material, thickness_mm):
    speed_m_per_min = estimate_cutting_speed_meters_per_min(material, thickness_mm)
    time_in_hours = (length_m / speed_m_per_min) / 60
    total_cost_inr = time_in_hours * HOURLY_RATE_INR
    return round(total_cost_inr, 2)
def calculate_material_cost_per_meter(material, thickness_mm, width_m=1.0):
    density_kg_per_m3 = MATERIAL_DATA[material]["density_kg_per_m3"]
    price_per_kg_inr = MATERIAL_DATA[material]["price_per_kg_inr"]
    thickness_m = thickness_mm / 1000
    weight_per_meter_kg = density_kg_per_m3 * thickness_m * width_m
    cost_per_meter_inr = weight_per_meter_kg * price_per_kg_inr
    return round(cost_per_meter_inr, 2)

def estimate_cutting_speed_meters_per_min(material, thickness_mm):
    material_constant = MATERIAL_DATA[material]["material_constant"]
    speed_m_per_min = (material_constant * LASER_POWER_KW) / thickness_mm
    return round(speed_m_per_min, 2)



def calculate_for_single_item(item):
    material = item["material"]
    thickness_mm = item["thickness"]
    cutting_length_perimeter_m = item["cutting_length_perimeter"]
    item_flattened_area_m2 = item["item_flattened_area"]
    quantity = item["quantity"]
    wastage_percentage = item["wastage_percentage"]

    cost_per_meter_inr = calculate_material_cost_per_meter(material, thickness_mm)
    cutting_speed_m_per_min = estimate_cutting_speed_meters_per_min(material, thickness_mm)
    cutting_cost_perimeter_inr = calculate_laser_cutting_cost_inr(cutting_length_perimeter_m, material, thickness_mm)
    cutting_cost_area_inr = calculate_laser_cutting_cost_inr(item_flattened_area_m2, material, thickness_mm)
    weight_of_material_kg = calculate_weight_of_material_kg(material, thickness_mm, item_flattened_area_m2)

    cost_for_one_item_inr = cutting_cost_area_inr + (cost_per_meter_inr * item_flattened_area_m2)
    cost_for_n_items_inr = cost_for_one_item_inr * quantity

    result = {
        "customer_info": {
            "cost_for_one_item_inr": cost_for_one_item_inr,
            "cost_for_n_items_inr": cost_for_n_items_inr,
            "total_weight_for_n_items_kg": weight_of_material_kg * quantity,
        },
        "internal_use": {
            "sheets_needed": sheets_needed,
            "cutting_time_per_item_min": cutting_speed_m_per_min,
            "cutting_time_per_n_items_min": cutting_speed_m_per_min * quantity,
            "weight_of_material_per_item_kg": weight_of_material_kg,
            "total_material_cost_inr": cost_per_meter_inr * item_flattened_area_m2 * quantity,
        }
    }

    return result

# Main Execution
if __name__ == "__main__":

    # Item-specific Variables (Global Scope)
    item = {
        "material": "aluminum",
        "thickness": 3.0,  # mm
        "cutting_length_perimeter": 1.003,  # meters
        "item_flattened_area": 0.057409,  # m²
        "quantity": 101,
        "wastage_percentage": 10
    }

    result = calculate_for_single_item(item)
    pprint({
        "Customer Info": result["customer_info"],
        "Internal Use": result["internal_use"]
    })
