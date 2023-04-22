from Database import Database 
db = Database()
with open("output_file1.txt", "r") as input_file:
    lines = input_file.readlines()

values = []
for line in lines:
    if ',' in line:
        templineSplit = line.replace('"',"").replace("\\", "/").split(",")
       # templineSplit = line.replace('"',"").replace('\\',"/").replace('//',"/").replace
        if "Air Base" in templineSplit[0]: continue 
        if len(templineSplit) > 9: 
            name = templineSplit[0].replace("Airport","").replace("International ","").replace("National","")
            city = templineSplit[1]
            land = templineSplit[2]
            int_short = templineSplit[3]
            coord_N = templineSplit[5]
            coord_O = templineSplit[6]
            continent = templineSplit[10]
           # values.append((name, city, land, int_short, coord_N, coord_O, continent))
            sql = ""
            try:
                sql = "INSERT INTO airports (name, city, land, int_short, coord_N, coord_O, continent) VALUES ('"+name+"', '"+city+"', '"+land+"', '"+int_short+"', '"+coord_N+"', '"+coord_O+"', '"+continent+"')"
                print(sql)
                db.insertSql(sql)
            except:
                print(sql +" not working ")


