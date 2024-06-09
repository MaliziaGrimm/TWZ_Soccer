import pymongo
import json, os

Flask_Server_Name = 'localhost:17102'
Version_Titel = 'Turnierwertzahl Turniere V0.3'
Version_Program = 'Tool für Turniere mit Turnierwertzahl'
Version_Name = 'ARM-Tools - Andreé Rosenkranz 2023-2024'


# if os.path.exists("daten/turnier.json"):
#     # print("Der Pfad existiert.")
#     with open('daten/turnier.json', "r") as datei:
#         daten = json.load(datei)
#         turnier = daten["turnier"]

# # Jetzt kannst du auf die Daten zugreifen
#       #  print(turnier)

# else:
# #    print("Der Pfad existiert nicht.")
#     daten = {
#         "turnier" : "standard"
#         }
#     with open("daten/turnier.json", "w") as datei:
#         json.dump(daten, datei)
        


aroclient = pymongo.MongoClient("mongodb://localhost:27017/")
arodb = aroclient["ARo_Datenbank"]
arocol = arodb["Turnier_Sammlung_TSG"]
#arocol = arodb["Turnier_Sammlung_"+turnier]
# das funktioniert nicht 
# es sollte das Dokument gewechselt werden können - dazu gehört die turnier_mod.py
#20240525




aropaarungcol = arodb["aktuellePaarung"]

