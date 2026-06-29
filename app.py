from flask import Flask, render_template, request
from main import Flight_locator

app = Flask(__name__)


@app.route("/")
def make_page():
    ua = request.headers.get("User-Agent")
    ua_split = ua.split(" ")
    platform = ua_split[1].lstrip("(").rstrip(";")

    if platform in ("Linux", "iPhone"):
        return render_template("mobile_index.html")
    else:
        return render_template("index.html")


@app.route("/run_get_flight", methods=["POST"])
def locate_flight():
    address = request.form.get("address")
    flight_locator = Flight_locator(address)
    flight = flight_locator.get_flight()
    return render_template("second_page.html", msg=flight)


if __name__ == "__main__":
    app.run(debug=True)
