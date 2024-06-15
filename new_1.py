import csv
import openai

openai.api_key="Your API Key"


# Engine creation
def generate_sql(prompt):
  response = openai.Completion.create(
    engine="gpt-3.5-turbo-instruct", 
    prompt=prompt,
    max_tokens=100,
    temperature=0.5,
  )
  return response.choices[0].text

def main():
  
  table_name ="customer.csv"

# Read csv and take header
  with open(table_name) as f:
    reader = csv.reader(f)
    headers = next(reader)

# column rename
  result = []
  for word in headers:
      if ' ' in word:
          word = word.replace(' ','_')
      result.append(word)
  
  sujit =[]
  for i in result:
     sujit.append(i.lower())

  # print(sujit)
  
  # print("CSV headers:", headers)
  print("CSV headers:", sujit)
  table_name = table_name.split(".")[0]
 

  while True:
    query = input("Enter query: ")
    # prompt = f"Convert this to SQL based on columns {headers}: {query}\n"
    prompt = f"Convert this to SQL query on table {table_name} with columns {sujit}: {query}\n"
 
    sql = generate_sql(prompt)
    print("SQL:", sql)
    break
  return sql


if __name__ == "__main__":
  sql=main()
  # main()