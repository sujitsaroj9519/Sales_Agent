import openai
import pandas as pd
from data_1 import df
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
import base64

# Set up your OpenAI API key
openai.api_key = "Your API KEY"


def generate_chart_code(user_query):
    # Get the column names from the DataFrame
    column_names = list(df.columns)

    # Define the context
    context = f"You have a pandas DataFrame named 'df' with columns: {', '.join(column_names)}. The goal is to generate Python code to create visualizations (charts) based on natural language queries from the user. The code should use the existing 'df' DataFrame and the user's query to generate the appropriate chart. You must use the exact column names from the DataFrame in the generated code, without modifying or assuming different names. Ensure that your code includes the necessary imports for the libraries used. Additionally, provide labeled sections or comments in the code to explain the purpose and context of each section."
    # context = f"You have a pandas DataFrame named 'df' with columns: {', '.join(column_names)}. The goal is to generate Python code to create visualizations (charts) based on natural language queries from the user. The code should use the existing 'df' DataFrame and the user's query to generate the appropriate chart. You must use the exact column names from the DataFrame in the generated code, without modifying or assuming different names. Ensure that your code includes the necessary imports for the libraries used."
    
    # Construct the prompt
    prompt = f"Context: {context}\nQuery: {user_query}"

    # Generate the code using the OpenAI API
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )
#    

    generated_code = response.choices[0].text

    # Print the generated code
    print(df.columns)
    print("Generated Code:")
    print(generated_code)

    # # Execute the generated code
    exec(generated_code)

      # Execute the generated code and capture the chart
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.read()).decode('utf-8')
    # print(chart_image)

    return generated_code, chart_image

# Get the user's query
user_query = input("Enter your query for creating a chart: ")
# user_query = "Generate a bar chart showing the average 'currensalary' grouped by 'gender'."

# Generate and execute the chart code
generate_chart_code(user_query)


