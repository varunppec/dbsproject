from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from cs50 import SQL
import string

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///dbsproject.db")

imp_seat = []
imp_train = ""

test = {
    1: ['Srirampura', 'Mantri Mall', 'Kempegowda', 'M G Road', 'Peenya'],
    2 : ['Mahalakshmi Layout', 'Mantri Mall', 'Kempegowda', 'Lalbagh', 'K R Market'],
    3 : ['Orion Mall', 'Kempegowda', 'Rajajinagar', 'M G Road'],
    4 : ['Peenya',  'M G Road', 'Kempegowda', 'Mantri Mall', 'Srirampura'],
    5 : ['K R Market', 'Lalbagh','Kempegowda','Mantri Mall','Mahalakshmi Layout'],
    6 : ['M G Road', 'Rajajinagar', 'Kempegowda','Orion Mall']
}


rows = db.execute("SELECT * FROM train")
if (len(rows) == 0):
    db.execute("INSERT INTO train('trainname', 'trainname', 'destination') VALUES(?,?,?)", 1,'Hyper','Peenya')
    db.execute("INSERT INTO train('trainname', 'trainname', 'destination') VALUES(?,?,?)", 2,'Ninja','K R Market')
    db.execute("INSERT INTO train('trainname', 'trainname', 'destination') VALUES(?,?,?)", 3,'Phantom','M G Road')
    db.execute("INSERT INTO train('trainname', 'trainname', 'destination') VALUES(?,?,?)", 4,'Shatter','Srirampura')
    db.execute("INSERT INTO train('trainname', 'trainname', 'destination') VALUES(?,?,?)", 5,'Everfast','Mahalakshmi Layout')
    db.execute("INSERT INTO train('trainname', 'trainname', 'destination') VALUES(?,?,?)", 6,'Bullet','Orion Mall')


sheesh = ['a','b','c','d', 'e','f']

db.execute("CREATE TABLE IF NOT EXISTS train_seats('seatno' VARchar(2), 'userid' VARCHAR(255), 'trainno' VARCHAR(255), PRIMARY key('seatno'), FOREIGN KEY('userid') REFERENCES user(userid), FOREIGN kEY('trainno') REFERENCES train(trainno))")
row = db.execute("SELECT * FROM train_seats")
if len(row) == 0:
    for j in sheesh:
        for i in range(1, 21):
            db.execute("INSERT OR REPLACE INTO train_seats(seatno, trainno, userid) VALUES(?, ?, NULL)", str(i) + j, sheesh.index(j) + 1)



@app.route("/", methods=["GET", "POST"])
def index ():
    if request.method == "GET" and  session.get("userid") is None:
        return render_template("login.html")
    if request.method == "GET" and session['userid']:
        row = db.execute("SELECT * FROM user where passenger is not null and userid = :userid", userid=session["userid"])
        if (row):
            ab = db.execute("SELECT distinct trainno from train_seats where userid=:id", id=session["userid"])[0]["trainno"]
            seat = db.execute("SELECT seatno from train_seats where userid=:id", id=session["userid"])
            seats = []
            for s in seat:
                seats.append(s["seatno"])
            return render_template("yup.html", row = row, seats = seats, train = ab)
        return redirect("/book")
    userid = request.form.get("userid")
    password = request.form.get("password")
    row = db.execute("SELECT * FROM user WHERE userid = :userid AND password = :password", userid = userid, password = password);
    if (len(row) == 0):
        return render_template("failure.html", message="User doesn't exist")
    session["userid"] = userid;
    row = db.execute("SELECT * FROM train_seats where userid=:userid", userid = session["userid"])
    row = db.execute("SELECT * FROM user where passenger is not null and userid = :userid", userid=session["userid"])

    if (row):
        ab = db.execute("SELECT distinct trainno from train_seats where userid=:id", id=session["userid"])[0]["trainno"]
        seat = db.execute("SELECT seatno from train_seats where userid=:id", id=session["userid"])
        seats = []
        for s in seat:
            seats.append(s["seatno"])
        return render_template("yup.html", row = row, seats = seats, train = ab)
    return redirect("/book")

@app.route("/register", methods=["GET", "POST"])
def register ():
    session.clear()
    if request.method == "GET":
        return render_template("register.html")
    username = request.form.get("username")
    password = request.form.get("password")
    userid = request.form.get("userid")
    if not username or not password or not userid:
        return render_template("failure.html", message="Provide details")
    Symbols =['$', '@', '#', '%']

    if len(password) < 8:
        return render_template("failure.html", message="length should be at least 8")

    if len(password) > 20:
        return render_template("failure.html", message='length should be not be greater than 20')

    if not any(char.isdigit() for char in password):
        return render_template("failure.html", message='Password should have at least one numeral')

    if not any(char.isupper() for char in password):
        return render_template("failure.html", message='Password should have at least one uppercase letter')

    if not any(char.islower() for char in password):
        return render_template("failure.html",message='Password should have at least one lowercase letter')

    if not any(char in Symbols for char in password):
        return render_template("failure.html",message='Password should have at least one of the symbols $@#%')
    rows = db.execute("SELECT * FROM user WHERE userid = :userid", userid=userid)
    if (len(rows) != 0):
        return render_template("failure.html", message="User already exists");
    db.execute("INSERT INTO user('username', 'userid', 'password', 'balance') VALUES (?, ?, ?, ?)", username, userid, password, 100)
    return redirect("/")

@app.route("/book", methods=["GET","POST"])
def home():
    if (session.get("userid") is None):
        return redirect("/");
    row = db.execute("SELECT * FROM user where userid = :userid AND passenger is not null", userid=session["userid"])

    if request.method == "GET" and session["userid"] and row:
        return redirect("/")
    if (request.method == "GET"):
        trains = db.execute("SELECT * FROM train");
        destinations = db.execute("SELECT * FROM station")
        arrives = db.execute("SELECT * FROM arrives_at")
        seats = db.execute("SELECT trainno, seatno  FROM train_seats WHERE userid is not null")
        #if (len(seats) == 0):
        if not session["userid"]:
            return redirect("/")
        return render_template("book.html", trains = trains, destinations = destinations, arrives = arrives, test = test,sheesh="test", seats = seats);
    train = request.form.get("train")
    start = request.form.get('start')
    end = request.form.get('end')
    no = request.form.get('no');

    if not train or not start or not end or not no:
        return render_template("failure.html", message="Fill the parameters")
    no = int(no)
    seats = []
    for i in range(0, no):
        seats.append(request.form.get('seat' + str(i + 1)))
        if seats[i] is None:
            return render_template("failure.html", message="Fill the parameters")
    if (len(seats) != len(set(seats))):
        return render_template("failure.html", message="Dont select the same seats")
    trainn = int(db.execute("select trainno from train where trainname = :train", train = train)[0]['trainno'])
    startt = db.execute("select stationno from station where stationname = :start", start = start)[0]['stationno']
    endd = db.execute("select stationno from station where stationname = :end", end = end)[0]['stationno']

    for seat in seats:
        result = db.execute("select * from train_seats where trainno=:trainn and seatno = :seatno and userid IS NOT NULL", trainn = trainn, seatno = seats[0] + sheesh[trainn - 1])
        if (len(result) != 0):
            return render_template("failure.html", message="found row")

    for seat in seats:
        #db.execute("insert into train_seats(userid, trainno, seatno) values(?,?,?)", session["userid"], trainn, seat +  sheesh[trainn - 1])
        db.execute("UPDATE train_seats set userid=:id where trainno=:trainn and seatno=:seatno", id=session["userid"], trainn = trainn, seatno = seat + sheesh[trainn - 1])
    source = test[trainn].index(start)
    destination = test[trainn].index(end)
    fare = (destination - source) * 5 * no
    balance = db.execute("select * from user where userid=:id", id=session["userid"])
    balance = balance[0]["balance"] - fare
    if (balance < 0):
        return render_template("failure.html", message="no balance")
    db.execute("UPDATE user set stationentry = :start, stationexit=:end, passenger=:no, balance=:balance where userid=:id", start=start, end=end, no=no, id=session["userid"], balance=balance)
    row = db.execute("select * from user where userid=:userid", userid=session["userid"])
    seat = db.execute("SELECT seatno from train_seats where userid=:id", id=session["userid"])
    seats = []
    for s in seat:
        seats.append(s["seatno"])
    return render_template("yup.html", row = row, seats = seats, train = train)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

