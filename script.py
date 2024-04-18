# Requirements:
# Fetch Data: 
# Write a Python script to perform an HTTP GET request to fetch JSON data from a public API (example URL: https://jsonplaceholder.typicode.com/todos).

# Process Data with Conditional List Comprehension:
# Extract titles from the JSON data, but only include those that contain a specific string (e.g., 'qui').
# Implement this using list comprehension.

# Display Results with f-Strings:
# Format and print the filtered titles using f-strings.
# Ensure that each printed title is a string.

# Type Checking:
# Demonstrate checking whether one of the extracted titles is of type int.

# Notes:
# Aim for clear, efficient, and concise code.
# Basic error handling is encouraged, but focus on the core functionalities.
# You can use online resources for reference, but ensure the coding is your own work.
# Please record your coding session using a screen recorder, explaining your thought process as you write the script.
# Provide the result in a publicly viewable google doc link, with the link to the session recording included inside.

import json
import requests
import pandas as pd
import re

# Get values from the url
url = 'https://jsonplaceholder.typicode.com/todos'
txt = json.loads(requests.get(url).text)

print(f'Number of dictionaries inside list: {len(txt)}')

# Checking names of dictionaries
all_keys = set()
for x in txt:
    all_keys |= set(list(x.keys()))
print('Keys inside dictionaries:', all_keys)

# Convert this list to a dataframe
list_for_pandas = []
for x in txt:
    list_for_pandas += [[x[key] for key in ['userId','id','title','completed']]]
df = pd.DataFrame(list_for_pandas,columns=['userId','id','title','completed'])

print(f'False rows: {len(df[df['completed'] == False])}')
print(f'False rows: {len(df[df['completed'] == True])}')

# Number of rows per user
for userid in set(df['userId'].values):
    print(f'The User {userid} has {len(df[df['userId'] == userid])}' )

# New column Number_of_letters, that gives for every row the number of letter of the string
df['Number_of_letters'] = df['title'].apply(lambda x: len(x))

# Counting number of letters per user
user_map_nbofletters = {}
for userid in set(df['userId'].values):
    numer_of_letters = sum(df[df['userId'] == userid]['Number_of_letters'].values)
    print(f'The User {userid} has {numer_of_letters} letters')
    user_map_nbofletters[userid] = numer_of_letters

# Sort the dictionarie by values
user_map_nbofletters = { x:y for x,y in sorted(user_map_nbofletters.items(), key=lambda item: item[1])}

# Looking for a specific pattern: d.*ect.*aut.*m
# delectus aut autem -> d.*ect.*aut.*m -> True
df['re_combiantion'] = df['title'].apply(lambda x: True if re.search('^d.*?ect.*?aut.*?m$',x) else False)
print(df[df['re_combiantion'] == True]) # Gives only one row

# Looking for a specific sub string
# qui
df['re_combiantion'] = df['title'].apply(lambda x: True if 'qui' in x else False)
print(df[df['re_combiantion'] == True]) # Gives multiple rows

# Managing errors
for line in df.to_dict(orient='records'):
    try:
        print(f"Element between d and b: {re.search('.*?d(.*?)b.*?',line['title']).group(1)}")
        print(f"Original: {line['title']}\n")
    except Exception as error:
        print(f'Fail, element dosent exist: {error}')

# Understanding element type
for value,col in zip(df.values[0],['userid','id','title','completed']):
    print(f'The column {col} type is {type(value)}')

###################################
########## NOT IN VIDEO ###########
###################################

# Checking if any title is int from the original dictionary

correct = []
incorrect = []
for line in txt:
    if type(line['title']) == int:
        incorrect += [line['title']]
    elif type(line['title']) == str:
        correct+= [line['title']]
    else:
        print(f'Wrong format: {type(line["title"])}')
if len(incorrect) > 0:
    print('Wrong format',incorrect)
else:
    print('Every title is a string')

