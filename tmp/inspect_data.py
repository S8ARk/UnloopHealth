import csv
files = ["health_fitness_dataset.csv", "Nutrition__Physical_Activity__and_Obesity.csv", "Personalized_Diet_Recommendations.csv"]
for f in files:
    try:
        with open(f, mode='r', encoding='utf-8') as file:
            line = file.readline().strip()
            print(f"{f}: {line}")
            # Also print the first data row to see values
            data_line = file.readline().strip()
            print(f"Row 1: {data_line}\n")
    except Exception as e:
        print(f"Error reading {f}: {e}")
