from flask import Flask
from flask import request
import os, time
import pymongo
import setting
import json


def turnier():
    # Turnierneuanlage 
   
    # Verbindung zur MongoDB herstellen
    aroclient = setting.aroclient
    arodb = setting.arodb
    arocol = setting.arocol

    # Datensatz eintragen - wenn erfasst / Fehler werden im Frontend abgefangen    
    if request.method == 'POST':
       
        neues_Turnier = {
            "tnummer" : request.form['form_turniernummer'],
            "tname" : request.form['form_turniername'],
            "taktiv" : "J",
            "tveranstalter" : request.form['form_ausrVerein'],
            "tak" : request.form['form_ak'],
            "tdatum" : request.form['form_tdatum'], 
            "tansprechpartner" : request.form['form_ansprechpartner'], 
            "tmobil" : request.form['form_mobil'],
            "temail" : request.form['form_email'], 
            "tuwgprivat" : request.form['form_uwg'], 
            }
            
        ergebnis = arocol.insert_one(neues_Turnier)
        
        # with open('daten/turniere.txt', 'a') as datei:
        #     datei.write(request.form['form_turniernummer']+'\n')
        # schreibt nur Turniere in eine txt Dati ohne Fkt 
            
        if os.path.exists("daten/turnier.json"):
            with open('daten/turnier.json', "r") as datei:
                daten = json.load(datei)
                daten["turnier"] = request.form['form_turniernummer']

            with open("daten/turnier.json", "w") as datei:
                json.dump(daten, datei)

        else:
            daten = {
                "turnier" : request.form['form_turniernummer']
                }
            with open("daten/turnier.json", "w") as datei:
                json.dump(daten, datei)
            
# Turnierwechsel klappt nicht, wenn neues T angelegt wird.
# Funktion Turnierauswahl fehlt komplett
# 20240526                
        pass
    else:
        pass
    return
#ok 20240418

def turnierloeschen():
    #turniere löschen
    
    if request.method == "POST":
        var_text=request.form['form_turniernummer']
                
        aroclient = setting.aroclient
        arodb = setting.arodb
        arocol = setting.arocol
        
        query = { "tnummer": var_text }
        result = arocol.find_one_and_delete(query)
        
        with open('daten/turniere.txt', 'r') as datei:
            lines = datei.readlines()
        lines = [line for line in lines if line.strip() != var_text]

        with open('daten/turniere.txt', 'w') as datei:
            datei.writelines(lines)
  
    else:
        pass    
    
    return
#ok 20240418