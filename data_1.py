import csv
import sqlite3
import re
from new_1 import main
import pandas as pd

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Read the CSV file
with open('customer.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    headers = next(csvreader)

    # Sanitize column names
    sanitized_headers = [re.sub(r'[^a-zA-Z0-9_]', '_', header.replace(' ', '_')).lower() for header in headers]

    # Identify the index of the 'currensalary' column
    currensalary_index = sanitized_headers.index('currensalary')
    age_index = sanitized_headers.index('age')

    # Generate the SQL query
    table_name = 'customer'
    columns = ', '.join(f'"{column}"' for column in sanitized_headers)
    values_placeholders = ', '.join(['?'] * len(sanitized_headers))
    create_table_query = f'CREATE TABLE {table_name} ({columns})'
    insert_query = f'INSERT INTO {table_name} VALUES ({values_placeholders})'

    # Create the table
    cursor.execute(create_table_query)

    # Insert data into the table
    for row in csvreader:
        # Remove commas from the 'currensalary' column and convert to integer
        currensalary_value = row[currensalary_index].replace(',', '')
        if currensalary_value:
            row[currensalary_index] = int(currensalary_value)
        else:
            row[currensalary_index] = None

        # Extract the numeric part from the 'age' column and convert to integer
        age_value = re.search(r'\d+', row[age_index])
        if age_value:
            row[age_index] = int(age_value.group())
        else:
            row[age_index] = None

        cursor.execute(insert_query, row)

# Commit the changes
conn.commit()

# Execute the SQL query (assuming it's generated dynamically)
# dynamic_query = "SELECT name, age, currensalary FROM customer WHERE currensalary IS NOT NULL AND currensalary > 5000000"
dynamic_query = main()
cursor.execute(dynamic_query)
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)


############################################ PANDAS ANALYSIS OPERATION"S  ############################################

# Create a DataFrame from the list of tuples
df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

# Close the connection
conn.close()

print(df.head())
print(df.describe())

# # Calculate mean of all numeric columns
# numeric_df = df._get_numeric_data()
# print(numeric_df.mean())
 
##################################### PLOTS  ###############################################
# import matplotlib.pyplot as plt

# # Count the occurrences of each job title
# job_title_counts = df['designation'].value_counts()

# # Create a bar chart
# job_title_counts.plot(kind='bar', figsize=(10, 6))
# plt.xlabel('Designation')
# plt.ylabel('Count')
# plt.title('Distribution of Designation')
# plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
# plt.show()

# import matplotlib.pyplot as plt
# import pandas as pd

# Assuming you have the DataFrame 'df' with column names ['name', 'functional_area', 'currensalary', 'current_location', 'gender', 'age', 'designation']

# # Bar Chart for Salary Distribution
# plt.figure(figsize=(10, 6))
# df['currensalary'].value_counts().sort_index().plot(kind='bar')
# plt.title('Salary Distribution')
# plt.xlabel('Salary')
# plt.ylabel('Count')
# plt.show()

# # Pie Chart for Gender Distribution
# plt.figure(figsize=(6, 6))
# df['gender'].value_counts().plot(kind='pie', autopct='%1.1f%%')
# plt.axis('equal')
# plt.title('Gender Distribution')
# plt.show()

# # Bar Chart for Functional Area Distribution
# plt.figure(figsize=(12, 6))
# df['functional_area'].value_counts().plot(kind='bar')
# plt.title('Functional Area Distribution')
# plt.xlabel('Functional Area')
# plt.ylabel('Count')
# plt.xticks(rotation=45)
# plt.show()

# # Scatter Plot for Age vs. Salary
# plt.figure(figsize=(8, 6))
# plt.scatter(df['age'], df['currensalary'])
# plt.title('Age vs. Salary')
# plt.xlabel('Age')
# plt.ylabel('Salary')
# plt.show()

# # Box Plot for Salary Distribution by Gender
# plt.figure(figsize=(6, 6))
# df.boxplot(column='currensalary', by='gender')
# plt.title('Salary Distribution by Gender')
# plt.xlabel('Gender')
# plt.ylabel('Salary')
# plt.show()