import pandas as pd
import random

# Read input CSV file
input_file = "/Users/mv802/Desktop/CT40_output2.csv"
df = pd.read_csv(input_file)

# Select required columns
df = df[['simulant_id', 'Unnamed: 0', 'household_id', 'first_name', 'last_name', 'ssn', 'mailing_address_zipcode', 'spouse_ssn']]

# Program variable
program_variable = "GYR"

# Year variables
years = [2021, 2022, 2023]
year_var = random.choice(years)

# Generate random DOB values
dob_values = pd.to_datetime(pd.Series([random.randint(pd.Timestamp('1950-01-01').value // 10**9, pd.Timestamp('2000-01-01').value // 10**9) for _ in range(len(df))]), unit='s')
df['DOB'] = dob_values.dt.strftime('%m%d%Y')

# Generate OutreachSource variable
outreach_sources = [1, 2, 3, 4]
df['OutreachSource'] = random.choices(outreach_sources, k=len(df))

# Generate Remote_VITA_tool_used column
df['Remote_VITA_tool_used'] = random.choices([0, 1], k=len(df))

# Generate consent column
df['consent'] = random.choices([0, 1], k=len(df))

# Generate intake column
df['intake'] = random.choices([0, 1], k=len(df), weights=[0.5, 0.5])

# Generate upload column
df['upload'] = random.choices([0, 1], k=len(df), weights=[0.5, 0.5])

# Generate phone_call column
df['phone_call'] = random.choices([0, 1], k=len(df), weights=[0.5, 0.5])

# Generate VITA_review column
df['VITA_review'] = random.choices([0, 1], k=len(df), weights=[0.5, 0.5])

# Generate Filer column
df['Filer'] = random.choices([0, 1], k=len(df), weights=[0.4, 0.6])

# Generate accepted column
df.loc[df['Filer'] == 1, 'accepted'] = random.choices([0, 1], k=sum(df['Filer'] == 1))

# Generate status column
status_values = ['Started', 'Submitted', 'Accepted', 'Other']
df['status'] = random.choices(status_values, k=len(df), weights=[0.27, 0.27, 0.27, 0.19])

# Write output to CSV
output_file = "CT40_output6.csv"
df.to_csv(output_file, index=False)

print("CSV file created successfully.")
