# Flask importieren
from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime

app = Flask(__name__)

# JSON importieren
import json

# Homepage
@app.route('/', methods=["GET", "POST"])
def homepage():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        return new_reservation(request.form)

#Eingabe von neue Reservierungen
def new_reservation(form):
    for field in form.keys():
        # Wenn ein oder mehrere Felder leer sind, kommt eine Fehlermeldung.
        if form[field] == "":
            return render_template("error.html", title="Fehlermeldung", nachricht="Felder dürfen nicht leer sein.")

        anzahlp = int(form['anzahlp'])
        if anzahlp == 1 or anzahlp == 2:
            tabletype = "Zweiertisch"
        elif anzahlp == 3 or anzahlp == 4:
            tabletype = "Vierertisch"
        else:
            return render_template("error.html", title='Fehlermeldung',
                                   nachricht="Anzahl Personen ist ungültig. nur 1, 2, 3 oder 4 Personen erlaubt.")

        targetdatum = datetime.strptime(form['datum'], "%Y-%m-%d")
        targettime = form['uhrzeit']

    with open("data/tische.json", "r") as file:
        tables = json.loads(file.read())

    with open("data/reservationen.json", "r") as file:
        reservations = json.loads(file.read())


    # Angefragtes Datum wird aus dem Formular geholt.
    requested_date = datetime.strptime(form['datum'], '%Y-%m-%d')
    requested_time = form['uhrzeit']

    # Reservationen Datei wird geöffnet.
    with open("data/reservationen.json", "r") as file:
        reservations = json.loads(file.read())

    # Es wird kontrolliert, ob ein Tisch frei ist.
    table_available = True
    for reservation in reservations:
        reservation_date = datetime.strptime(reservation["Datum"], "%d.%m.%Y")
        reservation_time = reservation["Uhrzeit"]
        tabletype = reservation["Anzahl Personen"].split(" ")[0]
        table_number = reservation["Anzahl Personen"].split(" ")[1]

        # reservationen.json wird geöffnet und als variable gelesen.
        with open("data/reservationen.json", "r") as file:
            reservations = json.loads(file.read())

        for reservation in reservations:
            fields = reservation.split(";")
            name = fields[0]
            anzahlp = fields[1]
            datum = fields[2]
            uhrzeit = fields[3]
            telefonnummer = fields[4]

        # Die Eingabe wird mit den existierenden Reservationen verglichen.
        if (requested_date == reservation_date) and (requested_time == reservation_time) and (
                table_number == tabletype):
            table_available = False
            break

        if table_available:
            # Wenn Tisch frei ist, Reservation bestätigen.
            return render_template("success.html",
                               nachricht="Wir bestätigen Ihnen hiermit die Reservation und freuen uns auf Sie! Vielen Dank!")
        else:
            # Wenn Tisch nicht frei ist, dann Gast informieren.
            return render_template("error.html", title='Fehlermeldung',
                               nachricht="Keine Tische verfügbar zu diesem Zeitpunkt.")


if __name__ == "__main__":
    app.run(debug=True, port=5000)


