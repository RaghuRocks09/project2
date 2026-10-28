from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "transigo-class-project-change-this"
BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "transigo.db"

# Vehicle fare rates are illustrative project values (rupees per kilometre).
RATES = {
    "Bike": 12,
    "Auto": 18,
    "Cab": 25,
}
MIN_FARE = 40


def get_db_connection():
    """Open a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the bookings table if it does not already exist."""
    connection = get_db_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pickup TEXT NOT NULL,
            drop_location TEXT NOT NULL,
            vehicle TEXT NOT NULL,
            distance REAL NOT NULL,
            fare INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)
    connection.commit()
    connection.close()


def calculate_fare(vehicle, distance):
    """Calculate the demo fare for the chosen vehicle and distance."""
    return max(MIN_FARE, round(RATES[vehicle] * distance))


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        pickup = request.form.get("pickup", "").strip()
        drop_location = request.form.get("drop", "").strip()
        vehicle = request.form.get("vehicle", "Bike")
        distance_text = request.form.get("distance", "").strip()

        # Validate the form before saving anything.
        if not pickup or not drop_location:
            flash("Please enter both pickup and drop locations.", "error")
            return redirect(url_for("home"))

        if pickup.casefold() == drop_location.casefold():
            flash("Pickup and drop locations must be different.", "error")
            return redirect(url_for("home"))

        if vehicle not in RATES:
            flash("Please select a valid vehicle.", "error")
            return redirect(url_for("home"))

        try:
            distance = float(distance_text)
        except ValueError:
            distance = 0

        if not 0 < distance <= 500:
            flash("Enter a distance greater than 0 and no more than 500 km.", "error")
            return redirect(url_for("home"))

        fare = calculate_fare(vehicle, distance)

        connection = get_db_connection()
        cursor = connection.execute(
            """INSERT INTO bookings
               (pickup, drop_location, vehicle, distance, fare)
               VALUES (?, ?, ?, ?, ?)""",
            (pickup, drop_location, vehicle, distance, fare)
        )
        booking_id = cursor.lastrowid
        connection.commit()
        connection.close()

        return redirect(url_for("confirmation", booking_id=booking_id))

    return render_template("index.html", rates=RATES, min_fare=MIN_FARE)


@app.route("/booking/<int:booking_id>")
def confirmation(booking_id):
    connection = get_db_connection()
    booking = connection.execute(
        "SELECT * FROM bookings WHERE id = ?", (booking_id,)
    ).fetchone()
    connection.close()

    if booking is None:
        flash("That booking could not be found.", "error")
        return redirect(url_for("home"))

    return render_template("confirmation.html", booking=booking)


@app.route("/history")
def history():
    connection = get_db_connection()
    bookings = connection.execute(
        "SELECT * FROM bookings ORDER BY id DESC"
    ).fetchall()
    connection.close()
    return render_template("history.html", bookings=bookings)


@app.route("/delete-history", methods=["POST"])
def delete_history():
    # Demo-only admin action: clears all bookings from the local project database.
    connection = get_db_connection()
    connection.execute("DELETE FROM bookings")
    connection.commit()
    connection.close()
    flash("All demo bookings have been deleted.", "success")
    return redirect(url_for("history"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
