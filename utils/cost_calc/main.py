import json
from bending import calculate_bending_for_item
from welding import calculate_welding_for_item
from hw_insertion import calculate_insertion_and_tapping_for_item
from powder_coating import calculate_coating_for_item
from laser_cutting import calculate_laser_cutting_cost_inr

class CostCalculator:
    def __init__(self, cost_params, country_of_buyer):
        # Initialize parity multipliers based on the buyer's country
        if country_of_buyer == 'india':
            self.parity_multiplier = cost_params['parity_pricing']['india_multiplier']
        else:
            self.parity_multiplier = cost_params['parity_pricing']['us_multiplier']

        self.cost_params = cost_params

        # Initialize labor costs
        self.skilled_labour_cost = cost_params['labour_charges']['skilled']
        self.unskilled_labour_cost = cost_params['labour_charges']['unskilled']

        # Initialize profit margins
        self.xlogic_profit_margin = cost_params['profit_margins']['xlogic']
        self.third_party_profit_margin = cost_params['profit_margins']['third_party']

    def calc_parity_pricing(self, base_cost):
        """Apply the parity multiplier to base cost."""
        return base_cost * self.parity_multiplier

    def calc_total_profit_margin(self):
        """Calculate the total profit margin (xLogic + third party)."""
        return self.xlogic_profit_margin + self.third_party_profit_margin

    def calc_total_labour_cost(self, skilled_labour_days, unskilled_labour_days):
        """Calculate total labor cost based on skilled and unskilled labor days."""
        total_labour_cost = (
            self.skilled_labour_cost * skilled_labour_days +
            self.unskilled_labour_cost * unskilled_labour_days
        )
        return total_labour_cost

    def calc_labour_days(self):
        """Stub method to calculate labor days, modify as needed."""
        skilled_days = 5  # Example value
        unskilled_days = 2  # Example value
        return skilled_days, unskilled_days

    def calc_final_cost(self, item):
        """Calculate the final cost considering all operations and profit margins."""
        # Calculate labor days
        skilled_labour_days, unskilled_labour_days = self.calc_labour_days()

        # Calculate total labor cost
        total_labour_cost = self.calc_total_labour_cost(skilled_labour_days, unskilled_labour_days)

        # Calculate individual operation costs
        laser_cutting_cost = calculate_laser_cutting_cost_inr(item['length'], item['material'], item['thickness'])
        bending_cost = calculate_bending_for_item(item)['customer_info']['bending_cost_inr']
        welding_cost = calculate_welding_for_item(item)['customer_info']['welding_cost_inr']
        insertion_cost = calculate_insertion_and_tapping_for_item(item)['customer_info']['insertion_cost_inr']
        coating_cost = calculate_coating_for_item(item)['customer_info']['coating_cost_inr']

        # Sum all operation costs
        total_operation_cost = (
            laser_cutting_cost + bending_cost + welding_cost + insertion_cost + coating_cost
        )

        # Calculate total profit margin
        total_profit_margin = self.calc_total_profit_margin()

        # Calculate final cost with parity pricing and profit margin
        final_cost = self.calc_parity_pricing((1 + total_profit_margin) * (total_labour_cost + total_operation_cost))
        return final_cost

if __name__ == "__main__":
    # Load cost parameters from JSON file
    with open('./cost_params.json', 'r') as file:
        cost_params = json.load(file)

    # Create an instance of the CostCalculator for 'india'
    cost_calculator = CostCalculator(cost_params, 'india')

    # Example item details
    item = {
        "material": "aluminum",
        "thickness": 3.0,  # mm
        "length": 2.0,  # meters for laser cutting
        "bend_length_m": 0.5,  # meters per bend
        "num_bends": 2,  # Number of bends
        "weld_length_m": 0.8,  # Length of each weld in meters
        "num_hardware": 4,  # Number of hardware pieces per part
        "num_holes": 6,  # Number of holes to be tapped
        "area_m2": 0.75,  # Surface area for powder coating in square meters
        "quantity": 100  # Number of parts
    }

    # Calculate and print the final cost
    final_cost = cost_calculator.calc_final_cost(item)
    print(f"Final Cost: INR {final_cost}")
