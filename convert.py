import pandas as pd

# Load Excel
df = pd.read_excel(r"C:\Users\Dell\HadoopProjects\CropYieldMapReduce\crop_analysis_output.xlsx")

# Save as CSV
df.to_csv(r"C:\Users\Dell\HadoopProjects\CropYieldMapReduce\crop_analysis_output.csv", index=False)

print("✅ CSV saved!")
