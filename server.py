import flask

app = flask.Flask(__name__)

# Klasa reprezentująca osobę
class Osoba:
    def __init__(self, imie, nazwisko, wiek, plec):
        self.imie = imie
        self.nazwisko = nazwisko
        self.wiek = wiek
        self.plec = plec

    def __str__(self):
        return f'{self.imie};{self.nazwisko};{self.wiek};{self.plec}\n'

# Klasa zarządzająca bazą danych osób
class BazaDanych:
    def __init__(self):
        self.osoby = []

    def dodaj_osobe(self, imie, nazwisko, wiek, plec):
        osoba = Osoba(imie, nazwisko, wiek, plec)
        self.osoby.append(osoba)
        with open('db/base.csv', 'a') as f:
            f.write(str(osoba))

    def usun_osobe(self, imie, nazwisko):
        self.osoby = [osoba for osoba in self.osoby if osoba.imie != imie or osoba.nazwisko != nazwisko]
        with open('db/base.csv', 'w') as f:
            for osoba in self.osoby:
                f.write(str(osoba))

    def pobierz_osoby(self):
        return self.osoby

baza = BazaDanych()

@app.route('/')
def home():
    return flask.render_template("index.html")

@app.route('/add/<imie>/<nazwisko>/<wiek>/<plec>', methods=['POST'])
def add_user(imie, nazwisko, wiek, plec):
    baza.dodaj_osobe(imie, nazwisko, wiek, plec)
    return ''

@app.route('/list')
def list():
    list_lines = ''
    for osoba in baza.pobierz_osoby():
        list_lines += f'<tr><td>{osoba.imie}</td><td>{osoba.nazwisko}</td><td>{osoba.wiek}</td><td>{osoba.plec}</td><td><button data-action="edit" data-id="{osoba.imie};{osoba.nazwisko}">Edytuj</button></td><td><button data-action="del"  data-id="{osoba.imie};{osoba.nazwisko}">Usuń</button></td></tr>'
    return flask.render_template("list.html", list_values=list_lines)

@app.route('/del/<imie>/<nazwisko>', methods=['POST'])
def deletef(imie, nazwisko):
    baza.usun_osobe(imie, nazwisko)
    return ''

@app.route('/edit/<imie>/<nazwisko>', methods=['POST'])
def editform(imie, nazwisko):
    return flask.render_template("edit.html", imie=imie, nazwisko=nazwisko)

@app.route('/updatedb/<imie>/<nazwisko>', methods=['POST'])
def updatedb(imie, nazwisko):
    nowe_imie = flask.request.form['imie']
    nowe_nazwisko = flask.request.form['nazwisko']
    baza.usun_osobe(imie, nazwisko)
    baza.dodaj_osobe(nowe_imie, nowe_nazwisko)
    return ''
