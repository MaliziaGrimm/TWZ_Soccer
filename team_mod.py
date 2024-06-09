from flask import Flask
from flask import request
import os, time
import setting

import pymongo


def team():
    # neuanlage Mannschaft

    # Datensatz eintragen - wenn erfasst / Fehler werden im Frontend abgefangen
    if request.method == "POST":

        aroclient = setting.aroclient
        arodb = setting.arodb
        arocol = setting.arocol

        neue_Mannschaft = {
            "mnummer": request.form["form_teamnummer"],
            "mname": request.form["form_mname"],
            "mnamezwei": request.form["form_mnamezwei"],
            "maktiv": "J",
            "mak": request.form["form_mak"],
            "mtwz": int(request.form["form_twz"]),
            "mdatum": request.form["form_mdatum"],
            "mansprechpartner": request.form["form_map"],
            "tmobil": request.form["form_mobil"],
            "temail": request.form["form_email"],
            "tuwgprivat": request.form["form_uwg"],
            "neuetwz": 600,
            "ergt1": 0,
            "ergt2": 0,
            "gegner": "nicht gelost",
            "gegnerm1": "spielfrei",
            "gegnerm2": "spielfrei",
            "gegnerm3": "spielfrei",
            "farbew": 0,
            "farbes": 0,
            "spielfrei": "0",
        }
        arocol.insert_one(neue_Mannschaft)
        pass
    else:
        pass
    return


# ok 20240419


def teamloeschen():

    if request.method == "POST":

        var_text = request.form["form_teamnummer"]

        aroclient = setting.aroclient
        arodb = setting.arodb
        arocol = setting.arocol

        query = {"mnummer": var_text}
        result = arocol.find_one_and_delete(query)
        pass
    else:
        pass
    return


def tnspielfreisetzen():
    if request.method == "POST":

        aroclient = setting.aroclient
        arodb = setting.arodb
        arocol = setting.arocol

        var_tnid = request.form["form_tnid"]
        var_tnspf = request.form["form_tnspfrei"]
        var_tnrunde = request.form["form_runde"]

        filtert1 = {"mnummer": var_tnid}
        new_data1 = {"$set": {"spielfrei": var_tnrunde, "gegner": "spielfrei"}}
        arocol.update_one(filtert1, new_data1)
        pass
    else:
        pass
    return


def teamaktivieren():
    if request.method == "POST":
        pass
    else:
        pass
    return


def teamverwalten():
    if request.method == "POST":
        pass
    else:
        pass
    return


def teamkopieren():
    if request.method == "POST":
        pass
    else:
        pass
    return