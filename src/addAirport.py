from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from Database import Database

db = Database()

#sql = "SELECT name FROM airports WHERE your_column IS NOT NULL AND your_column != '' UNION ALL SELECT int_short FROM airports WHERE your_column IS NOT NULL AND your_column != '';"
sql = "SELECT name FROM airports WHERE name IS NOT NULL AND name != ''"
sql1 = "SELECT int_short FROM airports WHERE int_short IS NOT NULL AND int_short != ''"
liste = db.select(sql,clean=True)
shortList = db.select(sql1,clean=True)

test = ['Goroka ', 'Madang ', 'Mount Hagen Kagamuga ']
for item in liste:
    if not item:
        print("The list contains empty elements.")
        break
else:
    print("The list does not contain empty elements.")

#CompinedList = new_list = [item for item in results.extend(short1) if item]
tempVar = ""
while True:
    completer = WordCompleter(liste + shortList)
   # completer = WordCompleter(liste.extend(shortList))

    # Get user input with autocompletion
    search_term = prompt('Enter a name to search for: ', completer=completer)
    # Search for matching names
    where= "name"
    if len(search_term) < 6 and search_term in shortList:
        where = "int_short"
    elif search_term in liste:
        where= "name"
    else:
        if tempVar == search_term:
            tempVar = ""
            default_values = {'name': 'Airport Name',
                'city': 'City Name',
                'land': 'Land Name',
                'continent': 'Europe/Berlin',
                'coord_N': 'Default N Coordinate',
                'coord_O': 'Default O Coordinate',
                'search_B': 1,
            }

            # Prompt user for values for each column in the "airports" table, using default values if none provided
            name = input("Enter airport name (default: {}): ".format(default_values['name'])) or default_values['name']
            city = input("Enter city name (default: {}): ".format(default_values['city'])) or default_values['city']
            land = input("Enter land name (default: {}): ".format(default_values['land'])) or default_values['land']
            continent = input("Enter continent name (default: {}): ".format(default_values['continent'])) or default_values['continent']
            coord_N = input("Enter N coordinate (default: {}): ".format(default_values['coord_N'])) or default_values['coord_N']
            coord_O = input("Enter O coordinate (default: {}): ".format(default_values['coord_O'])) or default_values['coord_O']
            search_B = default_values['search_B']

            # Construct and execute the INSERT statement
            insert_stmt = ("INSERT INTO airports name,int_short, city, land, continent, coord_N, coord_O, search_B VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            data = (name,search_term, city, land, continent, coord_N, coord_O, search_B)
            db.insert(sql=insert_stmt,values=data)
        tempVar = search_term
        print("NOT FOUND try Again")
        continue
    sql1 = "UPDATE airports SET search_B = 1 WHERE "+where+" = '" + search_term + "'"
    res = db.update(sql=sql1)