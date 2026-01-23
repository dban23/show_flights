from flask import Flask, render_template, url_for, request
from main import Flight_locator

app = Flask(__name__)


@app.route("/")
def make_page():
    return render_template("index.html")


@app.route("/run_get_flight", methods=["POST"])
def locate_flight():
    address = request.form.get("address")
    flight_locator = Flight_locator(address)

    return flight_locator.get_flight()


if __name__ == "__main__":
    app.run(debug=True)
