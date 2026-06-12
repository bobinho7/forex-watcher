from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from models import db, User, Bureau, ExchangeRate

app = Flask(__name__)

app.config["SECRET_KEY"] = "forex-secret-key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forex.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):
            login_user(user)
            return redirect(url_for("home"))

        return "Invalid username or password"

    return render_template("login.html")
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))  

@app.route("/add-rate", methods=["GET", "POST"])
@login_required
def add_rate():

    if current_user.role not in ["admin", "analyst"]:
        return "Access Denied"

    bureaus = Bureau.query.all()

    if request.method == "POST":

        rate = ExchangeRate(
            bureau_id=int(request.form["bureau_id"]),
            buy_rate=float(request.form["buy_rate"]),
            sell_rate=float(request.form["sell_rate"])
        )

        db.session.add(rate)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template(
        "add_rate.html",
        bureaus=bureaus
    )

@app.route("/add-bureau", methods=["GET", "POST"])
@login_required
def add_bureau():

    if current_user.role != "admin":
        return "Access Denied"

    if request.method == "POST":

        bureau = Bureau(
            name=request.form["name"],
            location=request.form["location"]
        )

        db.session.add(bureau)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("add_bureau.html")

@app.route("/bureaus")
@login_required
def bureaus():

    all_bureaus = Bureau.query.all()

    return render_template(
        "bureaus.html",
        bureaus=all_bureaus
    )

@app.route("/")
@login_required
def home():

    # ALWAYS define this first
    selected_bureau = request.args.get("bureau")

    # Now safe to use it
    if selected_bureau:

        rates = ExchangeRate.query.filter_by(
            bureau_id=int(selected_bureau)
        ).all()

    else:
        rates = ExchangeRate.query.all()

    if not rates:
        return "<h1>No data available</h1>"

    labels = [r.recorded_at.strftime("%Y-%m-%d %H:%M") for r in rates]
    buy_rates = [r.buy_rate for r in rates]
    sell_rates = [r.sell_rate for r in rates]

    avg_buy = sum(buy_rates) / len(buy_rates)
    avg_sell = sum(sell_rates) / len(sell_rates)

    best_buy = max(rates, key=lambda r: r.buy_rate)
    best_sell = min(rates, key=lambda r: r.sell_rate)

    all_bureaus = Bureau.query.all()

    return render_template(
        "index.html",
        rates=rates,
        labels=labels,
        buy_rates=buy_rates,
        sell_rates=sell_rates,
        avg_buy=avg_buy,
        avg_sell=avg_sell,
        best_buy=best_buy,
        best_sell=best_sell,
        all_bureaus=all_bureaus,
        selected_bureau=selected_bureau
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # ALWAYS seed bureaus first if empty
        if Bureau.query.count() == 0:

            bureaus = [

                Bureau(
                    name="Kampala Forex Bureau",
                    location="Kampala Road"
                ),

                Bureau(
                    name="City Exchange",
                    location="Nakasero"
                ),

                Bureau(
                    name="Alpha Forex Bureau",
                    location="Wandegeya"
                ),

                Bureau(
                    name="Premier Exchange",
                    location="Ntinda"
                ),

                Bureau(
                    name="East Africa Forex",
                    location="Kireka"
                )
            ]

            db.session.add_all(bureaus)
            db.session.commit()

        # NOW seed rates safely (important fix)
        if ExchangeRate.query.count() == 0:

            bureaus = Bureau.query.all()

            rates = [

                ExchangeRate(
                    bureau_id=bureaus[0].id,
                    buy_rate=3670,
                    sell_rate=3710
                ),

                ExchangeRate(
                    bureau_id=bureaus[1].id,
                    buy_rate=3665,
                    sell_rate=3705
                ),

                ExchangeRate(
                    bureau_id=bureaus[2].id,
                    buy_rate=3668,
                    sell_rate=3708
                ),

                ExchangeRate(
                    bureau_id=bureaus[3].id,
                    buy_rate=3672,
                    sell_rate=3712
                ),

                ExchangeRate(
                    bureau_id=bureaus[4].id,
                    buy_rate=3669,
                    sell_rate=3709
                )

            ]

            db.session.add_all(rates)
            db.session.commit()
        if User.query.count() == 0:

            admin = User(
                username="admin",
                password=generate_password_hash("admin123"),
                role="admin"
            )

            db.session.add(admin)
            db.session.commit()

        if User.query.count() == 1:

            analyst = User(
                username="analyst",
                password=generate_password_hash("analyst123"),
                role="analyst"
            )

            viewer = User(
                username="viewer",
                password=generate_password_hash("viewer123"),
                role="viewer"
    )

            db.session.add_all([analyst, viewer])
            db.session.commit()

    app.run(debug=True)