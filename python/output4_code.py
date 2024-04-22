import pandas as pd
import numpy as np

# Load CSV file
input_file = "input.csv"
df = pd.read_csv("/Users/mv802/Downloads/output1.csv")

# Add earned_income column
df['earned_income'] = np.random.choice([0, 1], size=len(df), p=[0.2, 0.8])

# Add unearned_income column
df['unearned_income'] = np.random.choice([0, 1], size=len(df), p=[0.9, 0.1])

# Add marital_status column
df['marital_status'] = np.random.choice([0, 1], size=len(df), p=[0.7, 0.3])

# Add hhsize column
df['hhsize'] = np.random.choice([1, 2, 3, 4], size=len(df), p=[0.10, 0.20, 0.15, 0.55])

# Add age_of_children column
df.loc[df['hhsize'] >= 2, 'age_of_children'] = np.random.choice(['youngest<6', '6<19'], size=sum(df['hhsize'] >= 2))

# Add age_of_adults column
df['age_of_adults'] = np.where(df['hhsize'] == 1, np.random.choice(['19<65', '65+'], size=len(df), p=[0.8, 0.2]), np.random.choice(['19<65', '65+'], size=len(df)))

# Add Receiving_TANF column
df['Receiving_TANF'] = 0
df.loc[np.random.choice(df.index, size=int(0.4*len(df))), 'Receiving_TANF'] = 1
df.loc[(df['hhsize'] >= 2) & (df['Receiving_TANF'] == 1), 'Receiving_TANF'] = 1

# Add Receiving_SNAP column
df['Receiving_SNAP'] = np.random.choice([0, 1], size=len(df), p=[0.2, 0.8])

# Add preferred_method_of_contact column
df['preferred_method_of_contact'] = np.random.choice(['phone', 'email', 'text'], size=len(df), p=[0.25, 0.25, 0.5])
df.loc[df['age_of_adults'] == '19<65', 'preferred_method_of_contact'] = np.random.choice(['phone', 'email', 'text'], size=sum(df['age_of_adults'] == '19<65'), p=[0.2, 0.2, 0.6])

# Save the modified DataFrame to a new CSV file
output_file = "CT40_output4.csv"
df.to_csv(output_file, index=False)
