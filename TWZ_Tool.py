from flask import Flask
from flask import request
import os, webbrowser, time
from flask import render_template

import setting
import team_mod, runden_mod, turnier_mod
import pymongo

app = Flask(__name__)


@app.route("/")
def index():
    var_kalendertag = os.path.join(time.strftime("%d.%m.%Y"))

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program
    var_version_name = setting.Version_Name

    t_uebersicht = tuebersicht()
    m_uebersicht = muebersicht()

    return render_template(
        "/index.html",
        v_heute=var_kalendertag,
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        v_version_name=var_version_name,
        v_tmess=t_uebersicht,
        v_mmess=m_uebersicht,
    )


@app.route("/turnier.html", methods=["GET", "POST"])
def turnier():
    # Turnier Neuanlage

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program
    var_version_name = setting.Version_Name
    turnier_mod.turnier()

    message = tuebersicht()

    return render_template(
        "/turnier.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        v_version_name=var_version_name,
        tabelle=message,
    )
    # ok 20240418


@app.route("/turnierloeschen.html", methods=["GET", "POST"])
def turnierloeschen():
    # Turniere l�schen

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program
    var_version_name = setting.Version_Name
    turnier_mod.turnierloeschen()

    message = tuebersicht()

    return render_template(
        "/turnierloeschen.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        v_version_name=var_version_name,
        tabelle=message,
    )
    # ok 18042024


def tuebersicht():
   
    aroclient = setting.aroclient
    arodb = setting.arodb
    arocol = setting.arocol

    turnieruebersicht = arocol.find(
        {"tnummer": {"$gt": "0"}},
        {
            "tnummer": 1,
            "tname": 1,
            "tveranstalter": 1,
            "tak": 1,
            "tdatum": 1,
            "tansprechpartner": 1,
        },
    )

    return turnieruebersicht


@app.route("/team.html", methods=["GET", "POST"])
def team():
    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program
    var_version_name = setting.Version_Name
    team_mod.team()

    message = muebersicht()

    return render_template(
        "/team.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        v_version_name=var_version_name,
        tabelle=message,
    )
    # ok 20240426


@app.route("/teamloeschen.html", methods=["GET", "POST"])
def teamloeschen():
    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program
    var_version_name = setting.Version_Name
    team_mod.teamloeschen()

    message = muebersicht()

    return render_template(
        "/teamloeschen.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        v_version_name=var_version_name,
        tabelle=message,
    )

def muebersicht():
    aroclient = setting.aroclient
    arodb = setting.arodb
    arocol = setting.arocol

    muebersicht = arocol.find(
        {"mnummer": {"$gt": "0"}},
        {
            "mnummer": 1,
            "mname": 1,
            "mnamezwei": 1,
            "mak": 1,
            "mtwz": 1,
            "tdatum": 1,
            "gegner": 1,
            "gegnerm1": 1,
            "gegnerm2": 1,
            "gegnerm3": 1,
            "mansprechpartner": 1,
            "ergt1": 1,
            "ergt2": 1,
            "neuetwz": 1,
            "feld": 1,
            "spielfrei": 1,
        },
    ).sort(
        "mtwz", -1
    )  

    return muebersicht


def paarungen():
    aroclient = setting.aroclient
    arodb = setting.arodb
    aropaarung = setting.aropaarungcol

    puebersicht = aropaarung.find()
    
    return puebersicht


@app.route("/rundeneu.html", methods=["GET", "POST"])
def rundeneu():

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program
    var_version_name = setting.Version_Name
    
    runden_mod.rundeneu()
    paarung = paarungen()

    message = muebersicht()
    message2 = muebersicht()
    return render_template(
        "/rundeneu.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        v_version_name=var_version_name,
        tabelle=message, 
        tabelle2 = paarung
    )

@app.route("/rundeneuerf.html", methods=["GET", "POST"])
def rundeneuerf():

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program
    var_version_name = setting.Version_Name
    
    runden_mod.rundeneu()
    paarung = paarungen()

    message = muebersicht()
    message2 = muebersicht()
    return render_template(
        "/rundeneuerf.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        v_version_name=var_version_name,
        tabelle=message, 
        tabelle2 = paarung
    )


#pilot dyn ergebnisse eintragen:

@app.route("/ergebnisneu.html", methods=["GET", "POST"])
def ergebnis_eintragenneu():
    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program
    var_version_name = setting.Version_Name

    wb = runden_mod.ergebnisseintragenneu()

    message = muebersicht()

    return render_template(
        "/ergebnisneu.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        v_version_name=var_version_name,
        tabelle=message,
        tabelle2=wb,
    )


@app.route("/ergebnis.html", methods=["GET", "POST"])
def ergebnis_eintragen():
    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program
    var_version_name = setting.Version_Name

    (
        var_f1t1,
        var_f1t2,
        var_f2t1,
        var_f2t2,
        var_f3t1,
        var_f3t2,
        var_f4t1,
        var_f4t2,
        var_f5t1,
        var_f5t2,
        var_f6t1,
        var_f6t2,
        var_f7t1,
        var_f7t2,
        var_f8t1,
        var_f8t2,
        var_f9t1,
        var_f9t2,
        var_f10t1,
        var_f10t2,
        var_f1t1name,
        var_f1t2name,
        var_f2t1name,
        var_f2t2name,
        var_f3t1name,
        var_f3t2name,
        var_f4t1name,
        var_f4t2name,
        var_f5t1name,
        var_f5t2name,
        var_f6t1name,
        var_f6t2name,
        var_f7t1name,
        var_f7t2name,
        var_f8t1name,
        var_f8t2name,
        var_f9t1name,
        var_f9t2name,
        var_f10t1name,
        var_f10t2name,
    ) = runden_mod.ergebnisseintragen()

    message = muebersicht()

    return render_template(
        "/ergebnis.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        v_version_name=var_version_name,
        tabelle=message,
        f1t1=var_f1t1name,
        f1t2=var_f1t2name,
        f2t1=var_f2t1name,
        f2t2=var_f2t2name,
        f3t1=var_f3t1name,
        f3t2=var_f3t2name,
        f4t1=var_f4t1name,
        f4t2=var_f4t2name,
        f5t1=var_f5t1name,
        f5t2=var_f5t2name,
        f6t1=var_f6t1name,
        f6t2=var_f6t2name,
        f7t1=var_f7t1name,
        f7t2=var_f7t2name,
        f8t1=var_f8t1name,
        f8t2=var_f8t2name,
        f9t1=var_f9t1name,
        f9t2=var_f9t2name,
        f10t1=var_f10t1name,
        f10t2=var_f10t2name,
    )
# ok


@app.route("/rundebeenden.html", methods=["GET", "POST"])
def rundebeenden():

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program
    var_version_name = setting.Version_Name

    runden_mod.rundebeenden()

    message = muebersicht()
    return render_template(
        "/rundebeenden.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        v_version_name=var_version_name,
        tabelle=message,
    )


# ok


@app.route("/spielfrei.html", methods=["GET", "POST"])
def spielfrei():
    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program
    var_version_name = setting.Version_Name

    team_mod.tnspielfreisetzen()

    message = muebersicht()

    return render_template(
        "/spielfrei.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        v_version_name=var_version_name,
        tabelle=message,
    )
    # offen AKTUELL


@app.route("/turnierstand.html", methods=["GET", "POST"])
def turnierstand():

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program
    var_version_name = setting.Version_Name

    message = muebersicht()
    tabelleu16 = muebersichtu16()  
    tabelleu30 = muebersichtu30()
    tabelleue65 = muebersichtue65()
 
    return render_template(
        "/turnierstand.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        v_version_name=var_version_name,
        tabelle=message,
        tabelleu16=tabelleu16,
        tabelleu30=tabelleu30,
        tabelleue65=tabelleue65,
    )

def muebersichtu16():
    aroclient = setting.aroclient
    arodb = setting.arodb
    arocol = setting.arocol
    
    mak_wert = 'U16'
    
    muebersichtu16 = arocol.find(
        {"mnummer": {"$gt": "0"}, "mak" : mak_wert},
        {
            "mnummer": 1,
            "mname": 1,
            "mnamezwei": 1,
            "mak": 1,
            "mtwz": 1,
            "tdatum": 1,
            "gegner": 1,
            "gegnerm1": 1,
            "gegnerm2": 1,
            "gegnerm3": 1,
            "mansprechpartner": 1,
            "ergt1": 1,
            "ergt2": 1,
            "neuetwz": 1,
            "feld": 1,
            "spielfrei": 1,
        },
    ).sort(
        "mtwz", -1
    )

    return muebersichtu16

def muebersichtu30():
    aroclient = setting.aroclient
    arodb = setting.arodb
    arocol = setting.arocol
    
    mak_wert = 'U30'
    
    muebersichtu30 = arocol.find(
        {"mnummer": {"$gt": "0"}, "mak" : mak_wert},
        {
            "mnummer": 1,
            "mname": 1,
            "mnamezwei": 1,
            "mak": 1,
            "mtwz": 1,
            "tdatum": 1,
            "gegner": 1,
            "gegnerm1": 1,
            "gegnerm2": 1,
            "gegnerm3": 1,
            "mansprechpartner": 1,
            "ergt1": 1,
            "ergt2": 1,
            "neuetwz": 1,
            "feld": 1,
            "spielfrei": 1,
        },
    ).sort(
        "mtwz", -1
    )

    return muebersichtu30

def muebersichtue65():
    aroclient = setting.aroclient
    arodb = setting.arodb
    arocol = setting.arocol
    
    mak_wert = 'Ü65'
    
    muebersichtue65 = arocol.find(
        {"mnummer": {"$gt": "0"}, "mak" : mak_wert},
        {
            "mnummer": 1,
            "mname": 1,
            "mnamezwei": 1,
            "mak": 1,
            "mtwz": 1,
            "tdatum": 1,
            "gegner": 1,
            "gegnerm1": 1,
            "gegnerm2": 1,
            "gegnerm3": 1,
            "mansprechpartner": 1,
            "ergt1": 1,
            "ergt2": 1,
            "neuetwz": 1,
            "feld": 1,
            "spielfrei": 1,
        },
    ).sort(
        "mtwz", -1
    )

    return muebersichtue65



@app.route("/teamverwalten.html", methods=["GET", "POST"])
def teamverwalten():

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program

    message = muebersicht()
    return render_template(
        "/teamverwalten.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        tabelle=message,
    )


@app.route("/teamkopieren.html", methods=["GET", "POST"])
def teamkopieren():

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program

    message = muebersicht()
    return render_template(
        "/teamkopieren.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        tabelle=message,
    )
#offen


@app.route("/teamaktivieren.html", methods=["GET", "POST"])
def teamaktivieren():

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program
    var_version_name = setting.Version_Name
    team_mod.teamaktivieren()

    message = muebersicht()

    return render_template(
        "/teamaktivieren.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
        v_version_name=var_version_name,
        tabelle=message,
    )
# offen 20240420 _ aktuell sind alle Teams aktiv!


@app.route("/turnierverwalten.html", methods=["GET", "POST"])
def turnierverwalten():

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program
    return render_template(
        "/turnierverwalten.html",
        v_version_program=var_version_program,
        v_version_titel=var_version_titel,
    )
# offen ###############


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=17102, debug=False)
