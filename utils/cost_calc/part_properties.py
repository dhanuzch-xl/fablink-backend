import random

class GetPartProperties:
    def __init__(self, step_file_path):
        self.step_file_path = step_file_path

        self.flat_area = self.get_flat_area_of_part()
        self.flat_perimeter = self.get_flat_perimeter_of_part()
        self.flat_bounding_box = self.get_flat_bounding_box()
        self.folded_bounding_box = self.get_folded_bounding_box()
        self.is_part_sheet_metal = self.is_part_sheet_metal()
        self.material_thickness = self.get_material_thickness()
        self.num_bends = self.get_num_bends()
        self.num_holes = self.get_num_holes()

    def get_flat_area_of_part(self):
        # output random float
        return random.uniform(0, 100)
    
    def get_flat_bounding_box(self):
        return [random.uniform(0, 100), random.uniform(0, 100), random.uniform(0, 100)]

    def get_flat_perimeter_of_part(self):
        return random.uniform(0, 100)

    def get_folded_bounding_box(self):
        return [random.uniform(0, 100), random.uniform(0, 100), random.uniform(0, 100)]

    def is_part_sheet_metal(self):
        return random.choice([True, False])

    def get_material_thickness(self):
        return random.uniform(0, 10)

    def get_num_bends(self):
        return random.uniform(0, 10)

    def get_num_holes(self):
        return random.uniform(0, 10)

if __name__ == "__main__":
    part_id = "WP-2"

    # replace the below logic to use DB
    import csv
    with open('utils/cost_calc/part_properties.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["part_id", "flat_area", "flat_perimeter", "flat_bounding_box", "folded_bounding_box", "is_part_sheet_metal", "material_thickness", "num_bends", "num_holes"])
        
        part_properties = GetPartProperties(f"models/{part_id}.step")
        writer.writerow([
            part_id,
            part_properties.flat_area,
            part_properties.flat_perimeter,
            part_properties.flat_bounding_box,
            part_properties.folded_bounding_box,
            part_properties.is_part_sheet_metal,
            part_properties.material_thickness,
            part_properties.num_bends,
            part_properties.num_holes
        ])