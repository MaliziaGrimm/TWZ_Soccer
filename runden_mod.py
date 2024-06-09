from pydoc import Doc
from winreg import REG_NOTIFY_CHANGE_ATTRIBUTES
from flask import Flask
from flask import request
import os, time
from networkx.algorithms.tree.branchings import docstring_arborescence
import pymongo, setting

import networkx as nx
import matplotlib.pyplot as plt
import itertools


def rundeneu():
    rundenvorschlag()
    
    if request.method == 'POST':
    # Verbindung zur MongoDB herstellen
        aroclient = setting.aroclient
        arodb = setting.arodb
        arocol = setting.arocol 

        # Anzahl der gesendeten Zeilen
        num_rows = len(request.form) // 9

        # Daten aus dem Formular abrufen und in eine Python-Liste laden
        daten = []
        for i in range(1, num_rows + 1):
            brett = request.form.get(f'Brett_{i}')
            spieler1_initialen = request.form.get(f'Spieler1_Initialen_{i}')
            spieler1_name = request.form.get(f'Spieler1_Name_{i}')
            spieler1_namezwei = request.form.get(f'Spieler1_Namezwei_{i}')
            spieler1_farbe = request.form.get(f'Spieler1_Farbe_{i}')
            spieler2_initialen = request.form.get(f'Spieler2_Initialen_{i}')
            spieler2_name = request.form.get(f'Spieler2_Name_{i}')
            spieler2_namezwei = request.form.get(f'Spieler2_Namezwei_{i}')
            spieler2_farbe = request.form.get(f'Spieler2_Farbe_{i}')

            zeile = [brett, spieler1_initialen, spieler1_name, spieler1_namezwei, spieler1_farbe, spieler2_initialen, spieler2_name, spieler2_namezwei, spieler2_farbe]
            print(str(zeile))
            

            var_t1 = spieler1_initialen # request.form['form_f'+str(i)+'t1']
            var_f1 = 'Feld'+str(i)+'t1'
            filtert1 = {'mnummer' : var_t1}
            doc1 = arocol.find_one(filtert1, {'farbew' : 1})
            var_farbew = (doc1['farbew'])+1    
            
            var_t2 = spieler2_initialen # request.form['form_f'+str(i)+'t2']
            var_f2 = 'Feld'+str(i)+'t2'
            filtert2 = {'mnummer' : var_t2}
            doc2 = arocol.find_one(filtert2, {'farbes' : 1})
            var_farbes = (doc2['farbes'])+1
            

            
            if doc1 is not None:
                filtert1_id = {'_id': doc1['_id']}
                new_data1 = {'$set' : {'gegner' : var_t2, 'feld' : var_f1, 'farbew' : var_farbew}}
                arocol.update_one(filtert1_id, new_data1)

            if doc2 is not None:
                filtert2_id = {'_id': doc2['_id']}
                new_data2 = {'$set' : {'gegner' : var_t1, 'feld' : var_f2, 'farbes' : var_farbes}}
                arocol.update_one(filtert2_id, new_data2)

            
            daten.append(zeile)
        
         
      
    return 


def rundeneuerf():
#    rundenvorschlag()
    
    if request.method == 'POST':
        # Verbindung zur MongoDB herstellen
        aroclient = setting.aroclient
        arodb = setting.arodb
        arocol = setting.arocol

        i = 0
        while i < 10:
            i = i + 1

            if request.form['form_f'+str(i)+'t1'] == "" and request.form['form_f'+str(i)+'t2'] == "":
                # beide leer nichts machen
                pass

            elif request.form['form_f'+str(i)+'t1'] == "" and request.form['form_f'+str(i)+'t2'] != "":
                var_team = request.form['form_f'+str(i)+'t2']
                var_feld = 'Feld'+str(i)+'t2'
                filter = {'mnummer' : var_team}
                doc = arocol.find_one(filter)    
                if doc is not None:
                    filtert_id = {'_id': doc['_id']}
                    new_data = {'$set' : {'gegner' : "spielfrei", 'feld' : "kein Feld"}}
                    arocol.update_one(filtert_id, new_data)
                pass
                
            elif request.form['form_f'+str(i)+'t1'] != "" and request.form['form_f'+str(i)+'t2'] == "":
                var_team = request.form['form_f'+str(i)+'t1']
                var_feld = 'Feld'+str(i)+'t1'
                filter = {'mnummer' : var_team}
                doc = arocol.find_one(filter)    
                if doc is not None:
                    filtert_id = {'_id': doc['_id']}
                    new_data = {'$set' : {'gegner' : "spielfrei", 'feld' : "kein Feld"}}
                    arocol.update_one(filtert_id, new_data)
                pass

            else:
                # kein spielfrei = normale Paarung
                var_t1 = request.form['form_f'+str(i)+'t1']
                var_f1 = 'Feld'+str(i)+'t1'
                filtert1 = {'mnummer' : var_t1}
                doc1 = arocol.find_one(filtert1, {'farbew' : 1})
                var_farbew = (doc1['farbew'])+1
                
                var_t2 = request.form['form_f'+str(i)+'t2']
                var_f2 = 'Feld'+str(i)+'t2'
                filtert2 = {'mnummer' : var_t2}
                doc2 = arocol.find_one(filtert2, {'farbes' : 1})
                var_farbes = (doc2['farbes'])+1
                
                if doc1 is not None:
                    filtert1_id = {'_id': doc1['_id']}
                    new_data1 = {'$set' : {'gegner' : var_t2, 'feld' : var_f1, 'farbew' : var_farbew}}
                    arocol.update_one(filtert1_id, new_data1)
                                
                if doc2 is not None:
                    filtert2_id = {'_id': doc2['_id']}
                    new_data2 = {'$set' : {'gegner' : var_t1, 'feld' : var_f2, 'farbes' : var_farbes}}
                    arocol.update_one(filtert2_id, new_data2)
                pass
        else:
            pass
        
    return 
#sollte erst mal stimmen für manuelle Auslosung - Info zur Paarung steht in der Konsole

def rundenvorschlag():
    # Erstellen Sie einen Graphen
    G = nx.Graph()
    
    aroclient = setting.aroclient
    arodb = setting.arodb
    arocol = setting.arocol
    paarungcol = setting.aropaarungcol

    paarungcol.delete_many({})
################################
# var_punkte und var_tn ermitteln aus db
     
    mtwz = []
    teams = []
    verbotenepaarungen = []   
    farbecalc = []
     
    for doc in arocol.find():
        if "mtwz" in doc and isinstance(doc["mtwz"], int): 
            if doc["gegner"] != "spielfrei":
                mtwz.append(doc[str("mtwz")])
    
    for doc in arocol.find():
        if "mnummer" in doc:
            if doc["gegner"] != "spielfrei":
                teams.append(doc["mnummer"])
                
    for doc in arocol.find():
        if "gegnerm1" in doc:
            verbotenepaarungen.append((doc["mnummer"],doc["gegnerm1"]))
        if "gegnerm2" in doc:
             verbotenepaarungen.append((doc["mnummer"],doc["gegnerm2"]))
             
             
    var_punkte = mtwz
    var_tn = teams
        
    anzahl = len(var_punkte)
    
    for i in range(anzahl):
        G.add_node(var_tn[i], var_punkte=var_punkte[i])

    # Definieren der Paare, die nicht gegeneinander spielen sollen
    var_verbotene_paarung = verbotenepaarungen
    # Erstellen einer Liste aller möglichen Paare, die nicht in der Liste der verbotenen Paare sind
    var_erlaubte_paarung = [paarung for paarung in itertools.combinations(var_tn, 2) if paarung not in var_verbotene_paarung and paarung[::-1] not in var_verbotene_paarung]

    # Erstellen einer Kopie der var_erlaubte_paarung Liste für die spätere Verwendung ??????
    var_erlaubte_paarung_copy = var_erlaubte_paarung.copy()

    # Für jeden Spieler, das Paar auswählen mit den ähnlichsten Punkten
    for player in var_tn:
        # Überprüfen, ob es noch erlaubte Paare für den aktuellen Spieler gibt
        player_paarungs = [paarung for paarung in var_erlaubte_paarung if player in paarung]
        if not player_paarungs:
            continue  # Überspringen der Schleife für den aktuellen Spieler, wenn keine Paare mehr vorhanden sind

        min_diff_paarung = min(player_paarungs, key=lambda paarung: abs(G.nodes[paarung[0]]['var_punkte'] - G.nodes[paarung[1]]['var_punkte']))
        G.add_edge(*min_diff_paarung)
        var_erlaubte_paarung = [paarung for paarung in var_erlaubte_paarung if player not in paarung]  # Entfernen aller Paare mit diesem Spieler

    # Berechnen der Gesamtpunktzahl für jedes Paar
    paarung_scores = [(paarung, G.nodes[paarung[0]]['var_punkte'] + G.nodes[paarung[1]]['var_punkte']) for paarung in var_erlaubte_paarung_copy]

    # Sortieren der Paare nach ihrer Gesamtpunktzahl
    sorted_paarungs = sorted(paarung_scores, key=lambda x: x[1], reverse=True)

    # Sortieren der Paare nach dem ersten Spieler
    sorted_paarungs_by_first_player = sorted(sorted_paarungs, key=lambda x: x[0][0])

    # Erstellen einer Textdatei und öffnen im Schreibmodus
    with open('daten/alleansetzungen.txt', 'w') as f:
        # Schreiben der sortierten Liste der Paare (sortiert nach dem ersten Spieler) und der Gesamtpunktzahl in die Datei
        f.write("\nPaare sortiert nach dem ersten Spieler:\n\n")
        for paarung, score in sorted_paarungs_by_first_player:
            f.write(f"Paar: {paarung}, Gesamtpunktzahl: {score}\n")
        
    with open('daten/ansetzungen.txt', 'w') as f:
        # Erstelle ein Set, um die Spieler zu speichern, die bereits in der Datei erwähnt wurden
        mentioned_var_tn = set()

        # Sortieren der Paare nach ihrer Gesamtpunktzahl
        sorted_paarungs_by_score = sorted(sorted_paarungs_by_first_player, key=lambda x: x[1], reverse=True)
        for paarung, score in sorted_paarungs_by_score:
            # Überprüfen, ob der erste oder der zweite Spieler bereits erwähnt wurde
            if paarung[0] not in mentioned_var_tn and paarung[1] not in mentioned_var_tn:
                f.write(f"Paar: {paarung}, Gesamtpunktzahl: {score}\n")
                # Hinzufügen der Spieler zum Set der erwähnten Spieler
                mentioned_var_tn.add(paarung[0])
                mentioned_var_tn.add(paarung[1])  
    
    import re
    with open('daten/Ansetzungen_mit_Name.txt', 'w') as f:
        with open('daten/ansetzungen.txt', 'r') as file:
            content = file.read()
            matches = re.findall(r"\('(.*?)'\)", content)
            ausgabe = []
            for match in matches:
                match = match.replace("'", "").replace(",", "")
                var_match1 = match[0]+match[1]
                var_match2 = match[3]+match[4]
                 


                if var_match1 is not None and var_match2 is not None:  # Überprüfung, ob die Variablen definiert sind
                    for doc in arocol.find({"mnummer": {"$in": [var_match1, var_match2]}}):
                        var_farbe1 = (f"{doc['farbew']}")
                        var_farbe2 = (f"{doc['farbes']}")
                        var_farbeSumme = int(var_farbe1) - int(var_farbe2) #Info zur Farbwahl, damit dann Ansetzungen getauscht werden können
                        ausgabe.append(f"{doc['mnummer']}, {doc['mname']}, {doc['mnamezwei']}"+" W:"+str(var_farbeSumme))  # Füge die Ausgabe zur Liste hinzu
                                                
            j = 0           
            for i in range(0, len(ausgabe), 2):
                j = j+1
                wert1 = int(ausgabe[i].split('W:')[-1])
#                if i+1 < len(ausgabe):
                wert2 = int(ausgabe[i+1].split('W:')[-1])
                if wert1 > wert2:
                    ausgabe[i], ausgabe[i+1] = ausgabe[i+1], ausgabe[i]
                # Paarungen in txt Datei speichern        
                f.write("Brett "+str(j)+": "+ausgabe[i] + " - " + ausgabe[i+1] + " : ___:___\n")
                # Paarungen auf cmd ausgeben
                print("Brett "+str(j)+": "+ausgabe[i] + " - " + ausgabe[i+1])

                # Paarungen in mongodb speichern in Dokument "aktuellePaarung" 
                name1 = ausgabe[i].split(',') # trenne ID und Name
                name2 = ausgabe[i+1].split(',')
                
                farbe1 = name1[2].split(' ') # trenne NameZwei und Anzahl W
                farbe2 = name2[2].split(' ')

                daten = {
                    "Brett": j,
                    "Spieler1": {
                        "Initialen": name1[0],
                        "Name": name1[1],
                        "Namezwei": farbe1[1],  # Erster Teil der Farbe
                        "Farbe": farbe1[2]  # Zweiter Teil der Farbe
                        },
                    "Spieler2": {
                        "Initialen": name2[0],
                        "Name": name2[1],
                        "Namezwei": farbe2[1],
                        "Farbe" : farbe2[2]
                    }                    
                }
                paarungcol.insert_one(daten)               


def ergebnisseintragenneu():
    # Verbindung zur MongoDB herstellen

    aroclient = setting.aroclient
    arodb = setting.arodb
    arocol = setting.arocol
    aropaarungcol = setting.aropaarungcol
    
    n = aropaarungcol.count_documents({}) # Anzahl DS in Mongobd Paarungen
    wb = {} # Wörterbuch für dyn variable
    i = 0 
    while i < n:
        i = i + 1
        
        var_f1 = 'Feld'+str(i)+'t1'
        var_t1 = 'gegner'
        filtert1 = {"feld" : var_f1}
        doc1 = arocol.find_one(filtert1, {"gegner" : 1, "mtwz" : 1, "mnummer" : 1, "mname" : 1, "mnamezwei" : 1, "ergt1" : 1, "ergt2" : 1})
        
        var_f2 = 'Feld'+str(i)+'t2'
        var_t2 = 'gegner'
        filtert2 = {"feld" : var_f2}
        doc2 = arocol.find_one(filtert2, {"gegner" : 1, "mtwz" : 1, "mnummer" : 1, "mname" : 1, "mnamezwei" : 1, "ergt1" : 1, "ergt2" : 1})
        
        if doc1 is not None or doc2 is not None:
            wb['var_f'+str(i)+'t1'] = (doc1['mnummer'], doc1['mtwz'], doc1['gegner'], doc2['mtwz'], doc1['ergt1'], doc1['ergt2'])            
            wb['var_f'+str(i)+'t2'] = (doc2['mnummer'], doc2['mtwz'], doc2['gegner'], doc1['mtwz'], doc2['ergt1'], doc2['ergt2'])
            wb['filtert'+str(i)+'1_id'] = {'_id': doc1['_id']}
            wb['filtert'+str(i)+'2_id'] = {'_id': doc2['_id']}
            wb['var_f'+str(i)+'t1name'] = str(doc1['mname']), str(' '), str(doc1['mnamezwei'])
            wb['var_f'+str(i)+'t1name'] = [str(wert) for wert in wb['var_f'+str(i)+'t1name']]
            wb['var_f'+str(i)+'t1name'] = ', '.join(wb['var_f'+str(i)+'t1name'])
            wb['var_f'+str(i)+'t1name'] = wb['var_f'+str(i)+'t1name'].replace(",","")
            wb['var_f'+str(i)+'t2name'] = str(doc2['mname']), str(' '), str(doc2['mnamezwei'])
            wb['var_f'+str(i)+'t2name'] = [str(wert) for wert in wb['var_f'+str(i)+'t2name']]
            wb['var_f'+str(i)+'t2name'] = ', '.join(wb['var_f'+str(i)+'t2name'])
            wb['var_f'+str(i)+'t2name'] = wb['var_f'+str(i)+'t2name'].replace(",","")
            wb['var_mtwz'+str(i)+'1'] = int(doc1['mtwz'])
            wb['var_mtwz'+str(i)+'2'] = int(doc2['mtwz'])

    return wb


               

def ergebnisseintragen():
    # Verbindung zur MongoDB herstellen

    aroclient = setting.aroclient
    arodb = setting.arodb
    arocol = setting.arocol
    
    i = 0 
    while i < 10:
        i = i + 1
        
        var_f1 = 'Feld'+str(i)+'t1'
        var_t1 = 'gegner'
        filtert1 = {"feld" : var_f1}
        doc1 = arocol.find_one(filtert1, {"gegner" : 1, "mtwz" : 1, "mnummer" : 1, "mname" : 1, "mnamezwei" : 1, "ergt1" : 1, "ergt2" : 1})
        
        var_f2 = 'Feld'+str(i)+'t2'
        var_t2 = 'gegner'
        filtert2 = {"feld" : var_f2}
        doc2 = arocol.find_one(filtert2, {"gegner" : 1, "mtwz" : 1, "mnummer" : 1, "mname" : 1, "mnamezwei" : 1, "ergt1" : 1, "ergt2" : 1})
        

        if i == 1:
            var_f1t1 = []
            var_f1t2 = []
            if doc1 is not None or doc2 is not None:
                var_f1t1 = (doc1['mnummer'], doc1['mtwz'], doc1['gegner'], doc2['mtwz'], doc1['ergt1'], doc1['ergt2'])            
                var_f1t2 = (doc2['mnummer'], doc2['mtwz'], doc2['gegner'], doc1['mtwz'], doc2['ergt1'], doc2['ergt2'])
                filtert11_id = {'_id': doc1['_id']}
                filtert12_id = {'_id': doc2['_id']}
                var_f1t1name = str(doc1['mname']), str(' '), str(doc1['mnamezwei'])
                var_f1t1name = [str(wert) for wert in var_f1t1name]
                var_f1t1name = ', '.join(var_f1t1name)
                var_f1t1name = var_f1t1name.replace(",","")
            
                var_f1t2name = str(doc2['mname']), str(' '), str(doc2['mnamezwei'])
                var_f1t2name = [str(wert) for wert in var_f1t2name]
                var_f1t2name = ', '.join(var_f1t2name)
                var_f1t2name = var_f1t2name.replace(",","")
                var_mtwz11 = int(doc1['mtwz'])
                var_mtwz12 = int(doc2['mtwz'])
            else:
                var_f1t1name = "nicht belegt"
                var_f1t2name = "nicht belegt"
            pass     
        
        elif i == 2:
            var_f2t1 = []
            var_f2t2 = []
            if doc1 is not None or doc2 is not None:
                var_f2t1 = (doc1['mnummer'], doc1['mtwz'], doc1['gegner'], doc2['mtwz'], doc1['ergt1'], doc1['ergt2'])            
                var_f2t2 = (doc2['mnummer'], doc2['mtwz'], doc2['gegner'], doc1['mtwz'], doc2['ergt1'], doc2['ergt2']) 
                filtert21_id = {'_id': doc1['_id']}
                filtert22_id = {'_id': doc2['_id']}
                
                var_f2t1name = str(doc1['mname']), str(' '), str(doc1['mnamezwei'])
                var_f2t1name = [str(wert) for wert in var_f2t1name]
                var_f2t1name = ', '.join(var_f2t1name)
                var_f2t1name = var_f2t1name.replace(",","")
                var_f2t2name = str(doc2['mname']), str(' '), str(doc2['mnamezwei'])
                var_f2t2name = [str(wert) for wert in var_f2t2name]
                var_f2t2name = ', '.join(var_f2t2name)
                var_f2t2name = var_f2t2name.replace(",","")
                var_mtwz21 = int(doc1['mtwz'])
                var_mtwz22 = int(doc2['mtwz'])
            else:
                var_f2t1name = "nicht belegt"
                var_f2t2name = "nicht belegt"
            pass
        elif i == 3:
            var_f3t1 = []
            var_f3t2 = []
            var_f3t1name = []
            var_f3t2name = []
            if doc1 is not None or doc2 is not None:
                var_f3t1 = (doc1['mnummer'], doc1['mtwz'], doc1['gegner'], doc2['mtwz'], doc1['ergt1'], doc1['ergt2'])            
                var_f3t2 = (doc2['mnummer'], doc2['mtwz'], doc2['gegner'], doc1['mtwz'], doc2['ergt1'], doc2['ergt2'])
                filtert31_id = {'_id': doc1['_id']}
                filtert32_id = {'_id': doc2['_id']}
                var_f3t1name = str(doc1['mname']), str(' '), str(doc1['mnamezwei'])
                var_f3t1name = [str(wert) for wert in var_f3t1name]
                var_f3t1name = ', '.join(var_f3t1name)
                var_f3t1name = var_f3t1name.replace(",","")
                var_f3t2name = str(doc2['mname']), str(' '), str(doc2['mnamezwei'])
                var_f3t2name = [str(wert) for wert in var_f3t2name]
                var_f3t2name = ', '.join(var_f3t2name)
                var_f3t2name = var_f3t2name.replace(",","")   
                
                var_mtwz31 = int(doc1['mtwz'])
                var_mtwz32 = int(doc2['mtwz'])
               
            else:
                var_f3t1name = "nicht belegt"
                var_f3t2name = "nicht belegt"
            pass
        
        elif i == 4:
            var_f4t1 = []
            var_f4t2 = []
            var_f4t1name = []
            var_f4t2name = []
            if doc1 is not None or doc2 is not None:
                var_f4t1 = (doc1['mnummer'], doc1['mtwz'], doc1['gegner'], doc2['mtwz'], doc1['ergt1'], doc1['ergt2'])            
                var_f4t2 = (doc2['mnummer'], doc2['mtwz'], doc2['gegner'], doc1['mtwz'], doc2['ergt1'], doc2['ergt2'])
                filtert41_id = {'_id': doc1['_id']}
                filtert42_id = {'_id': doc2['_id']}
                var_f4t1name = str(doc1['mname']), str(' '), str(doc1['mnamezwei'])
                var_f4t1name = [str(wert) for wert in var_f4t1name]
                var_f4t1name = ', '.join(var_f4t1name)
                var_f4t1name = var_f4t1name.replace(",","")
                var_f4t2name = str(doc2['mname']), str(' '), str(doc2['mnamezwei'])
                var_f4t2name = [str(wert) for wert in var_f4t2name]
                var_f4t2name = ', '.join(var_f4t2name)
                var_f4t2name = var_f4t2name.replace(",","")   
                
                var_mtwz41 = int(doc1['mtwz'])
                var_mtwz42 = int(doc2['mtwz'])

            else:
                var_f4t1name = "nicht belegt"
                var_f4t2name = "nicht belegt"
            pass     
        
        elif i == 5:
            var_f5t1 = []
            var_f5t2 = []
            var_f5t1name = []
            var_f5t2name = []
            if doc1 is not None or doc2 is not None:
                var_f5t1 = (doc1['mnummer'], doc1['mtwz'], doc1['gegner'], doc2['mtwz'], doc1['ergt1'], doc1['ergt2'])            
                var_f5t2 = (doc2['mnummer'], doc2['mtwz'], doc2['gegner'], doc1['mtwz'], doc2['ergt1'], doc2['ergt2']) 
                filtert51_id = {'_id': doc1['_id']}
                filtert52_id = {'_id': doc2['_id']}
                var_f5t1name = str(doc1['mname']), str(' '), str(doc1['mnamezwei'])
                var_f5t1name = [str(wert) for wert in var_f5t1name]
                var_f5t1name = ', '.join(var_f5t1name)
                var_f5t1name = var_f5t1name.replace(",","")
                var_f5t2name = str(doc2['mname']), str(' '), str(doc2['mnamezwei'])
                var_f5t2name = [str(wert) for wert in var_f5t2name]
                var_f5t2name = ', '.join(var_f5t2name)
                var_f5t2name = var_f5t2name.replace(",","") 
                
                var_mtwz51 = int(doc1['mtwz'])
                var_mtwz52 = int(doc2['mtwz'])
            else:
                var_f5t1name = "nicht belegt"
                var_f5t2name = "nicht belegt"
            pass
        
        elif i == 6:
            var_f6t1 = []
            var_f6t2 = []
            var_f6t1name = []
            var_f6t2name = []
            if doc1 is not None or doc2 is not None:
                var_f6t1 = (doc1['mnummer'], doc1['mtwz'], doc1['gegner'], doc2['mtwz'], doc1['ergt1'], doc1['ergt2'])            
                var_f6t2 = (doc2['mnummer'], doc2['mtwz'], doc2['gegner'], doc1['mtwz'], doc2['ergt1'], doc2['ergt2']) 
                filtert61_id = {'_id': doc1['_id']}
                filtert62_id = {'_id': doc2['_id']}
                var_f6t1name = str(doc1['mname']), str(' '), str(doc1['mnamezwei'])
                var_f6t1name = [str(wert) for wert in var_f6t1name]
                var_f6t1name = ', '.join(var_f6t1name)
                var_f6t1name = var_f6t1name.replace(",","")
                var_f6t2name = str(doc2['mname']), str(' '), str(doc2['mnamezwei'])
                var_f6t2name = [str(wert) for wert in var_f6t2name]
                var_f6t2name = ', '.join(var_f6t2name)
                var_f6t2name = var_f6t2name.replace(",","") 
                
                var_mtwz61 = int(doc1['mtwz'])
                var_mtwz62 = int(doc2['mtwz'])
            else:
                var_f6t1name = "nicht belegt"
                var_f6t2name = "nicht belegt"
            pass
        
        elif i == 7:
            var_f7t1 = []
            var_f7t2 = []
            var_f7t1name = []
            var_f7t2name = []
            if doc1 is not None or doc2 is not None:
                var_f7t1 = (doc1['mnummer'], doc1['mtwz'], doc1['gegner'], doc2['mtwz'], doc1['ergt1'], doc1['ergt2'])            
                var_f7t2 = (doc2['mnummer'], doc2['mtwz'], doc2['gegner'], doc1['mtwz'], doc2['ergt1'], doc2['ergt2']) 
                filtert71_id = {'_id': doc1['_id']}
                filtert72_id = {'_id': doc2['_id']}
                var_f7t1name = str(doc1['mname']), str(' '), str(doc1['mnamezwei'])
                var_f7t1name = [str(wert) for wert in var_f7t1name]
                var_f7t1name = ', '.join(var_f7t1name)
                var_f7t1name = var_f7t1name.replace(",","")
                var_f7t2name = str(doc2['mname']), str(' '), str(doc2['mnamezwei'])
                var_f7t2name = [str(wert) for wert in var_f7t2name]
                var_f7t2name = ', '.join(var_f7t2name)
                var_f7t2name = var_f7t2name.replace(",","") 
                
                var_mtwz71 = int(doc1['mtwz'])
                var_mtwz72 = int(doc2['mtwz'])
            else:
                var_f7t1name = "nicht belegt"
                var_f7t2name = "nicht belegt"
            pass

        elif i == 8:
            var_f8t1 = []
            var_f8t2 = []
            var_f8t1name = []
            var_f8t2name = []
            if doc1 is not None or doc2 is not None:
                var_f8t1 = (doc1['mnummer'], doc1['mtwz'], doc1['gegner'], doc2['mtwz'], doc1['ergt1'], doc1['ergt2'])            
                var_f8t2 = (doc2['mnummer'], doc2['mtwz'], doc2['gegner'], doc1['mtwz'], doc2['ergt1'], doc2['ergt2']) 
                filtert81_id = {'_id': doc1['_id']}
                filtert82_id = {'_id': doc2['_id']}
                var_f8t1name = str(doc1['mname']), str(' '), str(doc1['mnamezwei'])
                var_f8t1name = [str(wert) for wert in var_f8t1name]
                var_f8t1name = ', '.join(var_f8t1name)
                var_f8t1name = var_f8t1name.replace(",","")
                var_f8t2name = str(doc2['mname']), str(' '), str(doc2['mnamezwei'])
                var_f8t2name = [str(wert) for wert in var_f8t2name]
                var_f8t2name = ', '.join(var_f8t2name)
                var_f8t2name = var_f8t2name.replace(",","") 
                
                var_mtwz81 = int(doc1['mtwz'])
                var_mtwz82 = int(doc2['mtwz'])
            else:
                var_f8t1name = "nicht belegt"
                var_f8t2name = "nicht belegt"
            pass
        
        elif i == 9:
            var_f9t1 = []
            var_f9t2 = []
            var_f9t1name = []
            var_f9t2name = []
            if doc1 is not None or doc2 is not None:
                var_f9t1 = (doc1['mnummer'], doc1['mtwz'], doc1['gegner'], doc2['mtwz'], doc1['ergt1'], doc1['ergt2'])            
                var_f9t2 = (doc2['mnummer'], doc2['mtwz'], doc2['gegner'], doc1['mtwz'], doc2['ergt1'], doc2['ergt2']) 
                filtert91_id = {'_id': doc1['_id']}
                filtert92_id = {'_id': doc2['_id']}
                var_f9t1name = str(doc1['mname']), str(' '), str(doc1['mnamezwei'])
                var_f9t1name = [str(wert) for wert in var_f9t1name]
                var_f9t1name = ', '.join(var_f9t1name)
                var_f9t1name = var_f9t1name.replace(",","")
                var_f9t2name = str(doc2['mname']), str(' '), str(doc2['mnamezwei'])
                var_f9t2name = [str(wert) for wert in var_f9t2name]
                var_f9t2name = ', '.join(var_f9t2name)
                var_f9t2name = var_f9t2name.replace(",","") 
                
                var_mtwz91 = int(doc1['mtwz'])
                var_mtwz92 = int(doc2['mtwz'])
            else:
                var_f9t1name = "nicht belegt"
                var_f9t2name = "nicht belegt"
            pass
        
        
        elif i == 10:
            var_f10t1 = []
            var_f10t2 = []
            var_f10t1name = []
            var_f10t2name = []
            if doc1 is not None or doc2 is not None:
                var_f10t1 = (doc1['mnummer'], doc1['mtwz'], doc1['gegner'], doc2['mtwz'], doc1['ergt1'], doc1['ergt2'])            
                var_f10t2 = (doc2['mnummer'], doc2['mtwz'], doc2['gegner'], doc1['mtwz'], doc2['ergt1'], doc2['ergt2']) 
                filtert101_id = {'_id': doc1['_id']}
                filtert102_id = {'_id': doc2['_id']}
                var_f10t1name = str(doc1['mname']), str(' '), str(doc1['mnamezwei'])
                var_f10t1name = [str(wert) for wert in var_f10t1name]
                var_f10t1name = ', '.join(var_f10t1name)
                var_f10t1name = var_f10t1name.replace(",","")
                var_f10t2name = str(doc2['mname']), str(' '), str(doc2['mnamezwei'])
                var_f10t2name = [str(wert) for wert in var_f10t2name]
                var_f10t2name = ', '.join(var_f10t2name)
                var_f10t2name = var_f10t2name.replace(",","") 
                
                var_mtwz101 = int(doc1['mtwz'])
                var_mtwz102 = int(doc2['mtwz'])
            else:
                var_f10t1name = "nicht belegt"
                var_f10t2name = "nicht belegt"
            pass
       
        else:
            pass

        
    if request.method == 'POST':
        i = 0
        while i < 10:
            i = i + 1

            if request.form['form_Feld'+str(i)+'t1'] == "" and request.form['form_Feld'+str(i)+'t2'] == "":
#                print("Es wurde am Feld: "+str(i)+" keine Ansetzung erfasst!")
                pass
            elif request.form['form_Feld'+str(i)+'t1'] == "" and request.form['form_Feld'+str(i)+'t2'] != "":
 #               print("Das Team "+request.form['form_Feld'+str(i)+'t2']+" auf Feld Nummer: "+str(i)+" hat spielfrei. Es wurde kein Gegner erfasst")
                pass
            elif request.form['form_Feld'+str(i)+'t1'] != "" and request.form['form_Feld'+str(i)+'t2'] == "":
  #              print("Das Team "+request.form['form_f'+str(i)+'t1']+" auf Feld Nummer: "+str(i)+" hat spielfrei. Es wurde kein Gegner erfasst")
                pass
            elif request.form['form_Feld'+str(i)+'t1'] == "nicht belegt" and request.form['form_Feld'+str(i)+'t2'] == "nicht belegt":
   #             print("Das Feld Nummer: "+str(i)+" ist nicht belegt!")
                pass

            else:
                if i == 1:
                    var_ergt1 = request.form['form_erg1t1']
                    var_ergt2 = request.form['form_erg1t2']
                    var_mtwz1 = var_mtwz11
                    var_mtwz2 = var_mtwz12
                    twz1neu, twz2neu = twzberechnen(arocol, var_ergt1, var_ergt2, var_mtwz1, var_mtwz2)
                    new_data1 = {'$set' : {'neuetwz' : twz1neu, 'ergt1' : var_ergt1, 'ergt2' : var_ergt2}}  
                    new_data2 = {'$set' : {'neuetwz' : twz2neu, 'ergt1' : var_ergt2, 'ergt2' : var_ergt1}}  
                    arocol.update_one(filtert11_id, new_data1)
                    arocol.update_one(filtert12_id, new_data2)
                    pass
                
                elif i == 2:
                    var_ergt1 = request.form['form_erg2t1']
                    var_ergt2 = request.form['form_erg2t2']
                    var_mtwz1 = var_mtwz21
                    var_mtwz2 = var_mtwz22
                    twz1neu, twz2neu = twzberechnen(arocol, var_ergt1, var_ergt2, var_mtwz1, var_mtwz2)
                    new_data1 = {'$set' : {'neuetwz' : twz1neu, 'ergt1' : var_ergt1, 'ergt2' : var_ergt2}}  
                    new_data2 = {'$set' : {'neuetwz' : twz2neu, 'ergt1' : var_ergt2, 'ergt2' : var_ergt1}}  
                    arocol.update_one(filtert21_id, new_data1)
                    arocol.update_one(filtert22_id, new_data2)
                    pass
                
                elif i == 3:
                    var_ergt1 = request.form['form_erg3t1']
                    var_ergt2 = request.form['form_erg3t2']
                    var_mtwz1 = var_mtwz31
                    var_mtwz2 = var_mtwz32
                    twz1neu, twz2neu = twzberechnen(arocol, var_ergt1, var_ergt2, var_mtwz1, var_mtwz2)
                    new_data1 = {'$set' : {'neuetwz' : twz1neu, 'ergt1' : var_ergt1, 'ergt2' : var_ergt2}}  
                    new_data2 = {'$set' : {'neuetwz' : twz2neu, 'ergt1' : var_ergt2, 'ergt2' : var_ergt1}}  
                    arocol.update_one(filtert31_id, new_data1)
                    arocol.update_one(filtert32_id, new_data2)
                    pass   

                elif i == 4:
                    var_ergt1 = request.form['form_erg4t1']
                    var_ergt2 = request.form['form_erg4t2']
                    var_mtwz1 = var_mtwz41
                    var_mtwz2 = var_mtwz42
                    twz1neu, twz2neu = twzberechnen(arocol, var_ergt1, var_ergt2, var_mtwz1, var_mtwz2)
                    new_data1 = {'$set' : {'neuetwz' : twz1neu, 'ergt1' : var_ergt1, 'ergt2' : var_ergt2}}  
                    new_data2 = {'$set' : {'neuetwz' : twz2neu, 'ergt1' : var_ergt2, 'ergt2' : var_ergt1}}   
                    arocol.update_one(filtert41_id, new_data1)
                    arocol.update_one(filtert42_id, new_data2)
                    pass   
        
                elif i == 5:
                    var_ergt1 = request.form['form_erg5t1']
                    var_ergt2 = request.form['form_erg5t2']
                    var_mtwz1 = var_mtwz51
                    var_mtwz2 = var_mtwz52
                    twz1neu, twz2neu = twzberechnen(arocol, var_ergt1, var_ergt2, var_mtwz1, var_mtwz2)
                    new_data1 = {'$set' : {'neuetwz' : twz1neu, 'ergt1' : var_ergt1, 'ergt2' : var_ergt2}}  
                    new_data2 = {'$set' : {'neuetwz' : twz2neu, 'ergt1' : var_ergt2, 'ergt2' : var_ergt1}}  
                    arocol.update_one(filtert51_id, new_data1)
                    arocol.update_one(filtert52_id, new_data2)
                    pass  

                elif i == 6:
                    var_ergt1 = request.form['form_erg6t1']
                    var_ergt2 = request.form['form_erg6t2']
                    var_mtwz1 = var_mtwz61
                    var_mtwz2 = var_mtwz62
                    twz1neu, twz2neu = twzberechnen(arocol, var_ergt1, var_ergt2, var_mtwz1, var_mtwz2)
                    new_data1 = {'$set' : {'neuetwz' : twz1neu, 'ergt1' : var_ergt1, 'ergt2' : var_ergt2}}  
                    new_data2 = {'$set' : {'neuetwz' : twz2neu, 'ergt1' : var_ergt2, 'ergt2' : var_ergt1}}  
                    arocol.update_one(filtert61_id, new_data1)
                    arocol.update_one(filtert62_id, new_data2)
                    pass  
                
                elif i == 7:
                    var_ergt1 = request.form['form_erg7t1']
                    var_ergt2 = request.form['form_erg7t2']
                    var_mtwz1 = var_mtwz71
                    var_mtwz2 = var_mtwz72
                    twz1neu, twz2neu = twzberechnen(arocol, var_ergt1, var_ergt2, var_mtwz1, var_mtwz2)
                    new_data1 = {'$set' : {'neuetwz' : twz1neu, 'ergt1' : var_ergt1, 'ergt2' : var_ergt2}}  
                    new_data2 = {'$set' : {'neuetwz' : twz2neu, 'ergt1' : var_ergt2, 'ergt2' : var_ergt1}}  
                    arocol.update_one(filtert71_id, new_data1)
                    arocol.update_one(filtert72_id, new_data2)
                    pass  
                
                elif i == 8:
                    var_ergt1 = request.form['form_erg8t1']
                    var_ergt2 = request.form['form_erg8t2']
                    var_mtwz1 = var_mtwz81
                    var_mtwz2 = var_mtwz82
                    twz1neu, twz2neu = twzberechnen(arocol, var_ergt1, var_ergt2, var_mtwz1, var_mtwz2)
                    new_data1 = {'$set' : {'neuetwz' : twz1neu, 'ergt1' : var_ergt1, 'ergt2' : var_ergt2}}  
                    new_data2 = {'$set' : {'neuetwz' : twz2neu, 'ergt1' : var_ergt2, 'ergt2' : var_ergt1}}  
                    arocol.update_one(filtert81_id, new_data1)
                    arocol.update_one(filtert82_id, new_data2)
                    pass  
                
                elif i == 9:
                    var_ergt1 = request.form['form_erg9t1']
                    var_ergt2 = request.form['form_erg9t2']
                    var_mtwz1 = var_mtwz91
                    var_mtwz2 = var_mtwz92
                    twz1neu, twz2neu = twzberechnen(arocol, var_ergt1, var_ergt2, var_mtwz1, var_mtwz2)
                    new_data1 = {'$set' : {'neuetwz' : twz1neu, 'ergt1' : var_ergt1, 'ergt2' : var_ergt2}}  
                    new_data2 = {'$set' : {'neuetwz' : twz2neu, 'ergt1' : var_ergt2, 'ergt2' : var_ergt1}}  
                    arocol.update_one(filtert91_id, new_data1)
                    arocol.update_one(filtert92_id, new_data2)
                    pass  

                elif i == 10:
                    var_ergt1 = request.form['form_erg10t1']
                    var_ergt2 = request.form['form_erg10t2']
                    var_mtwz1 = var_mtwz101
                    var_mtwz2 = var_mtwz102
                    twz1neu, twz2neu = twzberechnen(arocol, var_ergt1, var_ergt2, var_mtwz1, var_mtwz2)
                    new_data1 = {'$set' : {'neuetwz' : twz1neu, 'ergt1' : var_ergt1, 'ergt2' : var_ergt2}}  
                    new_data2 = {'$set' : {'neuetwz' : twz2neu, 'ergt1' : var_ergt2, 'ergt2' : var_ergt1}}  
                    arocol.update_one(filtert101_id, new_data1)
                    arocol.update_one(filtert102_id, new_data2)
                    pass  

                else:
                    
                    pass
        else:
            pass
    else:
        pass
    
    return var_f1t1, var_f1t2, var_f2t1, var_f2t2, var_f3t1, var_f3t2, var_f4t1, var_f4t2, var_f5t1, var_f5t2, var_f6t1, var_f6t2, var_f7t1, var_f7t2, var_f8t1, var_f8t2, var_f9t1, var_f9t2, var_f10t1, var_f10t2, var_f1t1name, var_f1t2name, var_f2t1name, var_f2t2name, var_f3t1name, var_f3t2name, var_f4t1name, var_f4t2name, var_f5t1name, var_f5t2name, var_f6t1name, var_f6t2name, var_f7t1name, var_f7t2name, var_f8t1name, var_f8t2name, var_f9t1name, var_f9t2name, var_f10t1name, var_f10t2name

#ok Ansetzungenm werden gefunden und eingetragen 20240421
#ok Ergebnisse speichern für Feld 1 bis 5 .. auch bis 10??


def rundebeenden():
        
    if request.method == 'POST':
        if request.form['form_ergf'] == "1":
            
            aroclient = setting.aroclient
            arodb = setting.arodb
            arocol = setting.arocol

            result = arocol.update_many(
            {'gegner': {'$ne': None}},  
            [
                {'$set':  
                 {
                    'mtwz': '$neuetwz',
                    'gegnerm3': '$gegnerm2',
                    'gegnerm2' : '$gegnerm1',
                    'gegnerm1' : '$gegner',
                    'gegner': "nicht gelost",
                    'ergt1' : "0",
                    'ergt2' : "0",
                    'feld' : "kein Feld"
                 }
                }
             ]
            )           
            
            pass
        else:
            pass
    else:
        pass
    return

def twzberechnen(arocol, var_t1, var_t2, var_mtwz1, var_mtwz2):

    if int(var_t1) == int(var_t2):
        var_twzdiff = var_mtwz1 - var_mtwz2
        if var_twzdiff < -350:
            var_twzdiff = -350
        elif var_twzdiff > 350:
            var_twzdiff = 350
        else:
            pass
        
        if var_twzdiff > 0:
            var_twzdiff2 = var_twzdiff*0.04
            var_twzdiff2 = round(var_twzdiff2)
            twz1neu = int(var_mtwz1-8-var_twzdiff2)
   
            var_twzdiff3 = var_twzdiff*0.04
            var_twzdiff3 = round(var_twzdiff3)
            twz2neu = int(var_mtwz2+8+var_twzdiff3)
            
            pass
        
        elif var_twzdiff == 0:
            twz1neu = var_mtwz1
            twz2neu = var_mtwz2
            
            pass
            
        else:
            var_twzdiff2 = var_twzdiff*0.04
            var_twzdiff2 = round(var_twzdiff2)
            twz2neu = int(var_mtwz2-8-var_twzdiff2)
   
            var_twzdiff3 = var_twzdiff*0.04
            var_twzdiff3 = round(var_twzdiff3)
            twz1neu = int(var_mtwz1+8+var_twzdiff3)
            
            pass
        
    elif int(var_t1) > int(var_t2):
        var_tordiff = int(var_t1)-int(var_t2) 
        if var_tordiff > 9:
            var_twzbonus = 2
            pass
        elif var_tordiff > 4:
            var_twzbonus = 1
            pass
        else:
            var_twzbonus = 0
            
        var_twzdiff = var_mtwz1 - var_mtwz2
        if var_twzdiff < -350:
            var_twzdiff = -350
        elif var_twzdiff > 350:
            var_twzdiff = 350
        else:
            pass
        
        var_twzdiff2 = var_twzdiff*0.04
        var_twzdiff2 = round(var_twzdiff2+var_twzbonus)
        twz1neu = int(var_mtwz1+16+var_twzdiff2)
   
        var_twzdiff3 = var_twzdiff*0.04*(-1)
        var_twzdiff3 = round(var_twzdiff3-var_twzbonus)
        twz2neu = int(var_mtwz2-16+var_twzdiff3)
        
    else:
        var_twzdiff = var_mtwz2 - var_mtwz1
        if var_twzdiff < -350:
            var_twzdiff = -350
        elif var_twzdiff > 350:
            var_twzdiff = 350
        else:
            pass
        
        var_tordiff = int(var_t2)-int(var_t1) 
        if var_tordiff > 9:
            var_twzbonus = 2
            pass
        elif var_tordiff > 4:
            var_twzbonus = 1
            pass
        else:
            var_twzbonus = 0
        
        var_twzdiff2 = var_twzdiff*0.04
        var_twzdiff2 = round(var_twzdiff2+var_twzbonus)
        twz2neu = int(var_mtwz2+16+var_twzdiff2)
   
        var_twzdiff3 = var_twzdiff*0.04*(-1)
        var_twzdiff3 = round(var_twzdiff3-var_twzbonus)
        twz1neu = int(var_mtwz1-16+var_twzdiff3)
        

    return twz1neu, twz2neu
# ok 20240424