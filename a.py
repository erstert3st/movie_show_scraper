hoster = ["c","b","a","d","f"]

avlHoster = [
  {'text': 'a', 'working':'yes'},
  {'text': 'b', 'working':'no'},
  {'text': 'c', 'working':'yes'},
  {'text': 'd', 'working':'no'}
]
ready = []
newList = []
for host in hoster:
    for avl in avlHoster:
        if avl['text'] == host and avl['working'] == 'yes':
            ready.append(host)
            break
        elif avl['text'] == host and avl['working'] == 'no':  
          break
    else:
        newList.append(host)

ready = sorted(ready, key=lambda x: [avl['text'] for avl in avlHoster if avl['text'] == x][0])


print(ready)
print(newList)

hoster_in_avlHoster=[]
hoster_not_in_avlHoster=[]

# for item in avlHoster:
#   if item['text'] in hoster and item['working'] == 'yes':
#     hoster_in_avlHoster.append(item['text'])
#   elif item['text'] not in hoster:
#     hoster_not_in_avlHoster.append(item['text'])
# sortet = hoster_in_avlHoster.sort(key=lambda element: hoster.index(element['text']))
# print(hoster_in_avlHoster)
# print(hoster_not_in_avlHoster)
#print(non_working_elements) 
# Output: ['d', 'c']


#[{'text': 'b'}, {'text': 'b'}, {'text': 'a'}, {'text': 'c'}]


# Remove all elements that are not in list a
new_elements = [elem for elem in elements if elem['text'] in a]

# Sort the list based on list a
new_elements.sort(key=lambda x: a.index(x['text']))

# Print the results
print(new_elements)

# Output: [{'text': 'b'}, {'text': 'a'}, {'text': 'c'}]
print(result)
