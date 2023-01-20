# Flask importieren
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

# JSON importieren
import json

# Homepage
@app.route('/', methods=["GET", "POST"])
def homepage():
    # JSON File wird gelesen
    with open('data/reservationen.json', 'r') as f:
        file = json.load(f)
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
        # Wenn die Telefonnummer keine Zahl ist, kommt eine Fehlermeldung.
        try:
            telefonnummer = int(form["Telefonnummer"])
        except ValueError:
            return render_template("error.html", title='Fehlermeldung', nachricht="Telefonnummer ist ungültig.")
        # Wenn Anzahl Personen keine Zahl st
        try:
            anzahl = int(form["Anzahl Personen"])
        except ValueError:
            return render_template("error.html", title='Fehlermeldung', nachricht="Anzahl Personen kann nur aus Zahlen bestehen.")

#   newRes = {
#      "Name": reservation["Name"],
#       "Anzahl Personen": reservation["Anzahl Personen"],
#      "Datum": reservation.strftime("%d.%m.%Y")
#     "Uhrzeit": reservation["Uhrzeit"],
#    "Telefonnummer": reservation["Telefonnummer"],
#       }
#   reservationen.append(newRes)

if __name__ == "__main__":
    app.run(debug=True, port=5000)


