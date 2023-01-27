a = ["c","b","a"]

elements = [
  {'text': 'a','hallo':'a'},
  {'text': 'a','hallo':'b'},
  {'text': 'c','hallo':'c'},
  {'text': 'd','hallo':'d'},
  {'text': 'd','hallo':'e'},
  {'text': 'e','hallo':'f'},
  {'text': 'f','hallo':'g'},
]

sorted_elements = [element for element in elements if element['text'] in a]
sorted_elements.sort(key=lambda element: a.index(element['text']))

print(sorted_elements)

#[{'text': 'b'}, {'text': 'b'}, {'text': 'a'}, {'text': 'c'}]


# Remove all elements that are not in list a
new_elements = [elem for elem in elements if elem['text'] in a]

# Sort the list based on list a
new_elements.sort(key=lambda x: a.index(x['text']))

# Print the results
print(new_elements)

# Output: [{'text': 'b'}, {'text': 'a'}, {'text': 'c'}]
print(result)
