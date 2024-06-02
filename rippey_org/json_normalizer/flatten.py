import json
import pandas as pd 


#read file
with open ("normalized_data.json", "r") as json_file:
    data = json.load(json_file)

df = pd.json_normalize(data)
print(df.head())


output_file = "flattened_data.xlsx"
df.to_excel(output_file, index=False)

print(f"Data has been exported to {output_file}")