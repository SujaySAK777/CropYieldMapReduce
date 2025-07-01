import pandas as pd

def parse_line(line):
    key, values = line.split("\t")
    state, crop = key.split(",")

    value_dict = {}
    for part in values.split(","):
        if ":" in part:
            k, v = part.strip().split(": ")
            value_dict[k.strip()] = float(v.strip())

    return {
        "State": state.strip(),
        "Crop": crop.strip(),
        "Avg Area": value_dict.get("Avg Area", 0.0),
        "Avg Agri Land": value_dict.get("Avg Agri Land", 0.0),
        "Avg Barren Land": value_dict.get("Avg Barren Land", 0.0),
        "Avg Yield": value_dict.get("Avg Yield", 0.0),
        "Avg Rainfall": value_dict.get("Avg Rainfall", 0.0),
        "Fertilizer per ha": value_dict.get("Fertilizer per ha", 0.0),
        "Pesticide per ha": value_dict.get("Pesticide per ha", 0.0)
    }

# Path to your MapReduce output text file
input_path = r"C:/Users/Dell/HadoopProjects/CropYieldMapReduce/final_output.txt"

# Read and parse all lines
with open(input_path, "r") as f:
    lines = f.readlines()

data = [parse_line(line) for line in lines]

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
output_excel = r"C:/Users/Dell/HadoopProjects/CropYieldMapReduce/crop_analysis_output.xlsx"
df.to_excel(output_excel, index=False)

print(f"Excel file saved at: {output_excel}")
