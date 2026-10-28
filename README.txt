TRANSIGO — Python Flask + SQLite
=================================

A Class 12 Computer Science ride-booking website project.

FEATURES
--------
- Responsive ride-booking homepage
- Bike, Auto and Cab selection
- Fare estimate based on the chosen vehicle and distance
- Form validation
- Booking confirmation page
- Ride history page
- SQLite database stores bookings even after the app is closed

TECHNOLOGIES
------------
- Python: backend logic
- Flask: web framework and routes
- HTML: page structure
- CSS: website design
- JavaScript: live fare preview
- SQLite: booking database

PROJECT FILES
-------------
app.py
templates/
    index.html
    confirmation.html
    history.html
static/
    style.css
requirements.txt
README.txt

SETUP (Windows)
---------------
1. Install Python 3 from https://www.python.org/downloads/
   During installation, tick "Add Python to PATH".

2. Extract this ZIP file into a folder.

3. Open Command Prompt or Terminal in the TRANSIGO_Flask folder.

4. Install Flask:
       py -m pip install -r requirements.txt

   If the "py" command does not work, try:
       python -m pip install -r requirements.txt

5. Start the website:
       py app.py

   Or:
       python app.py

6. Open this address in your browser:
       http://127.0.0.1:5000

7. Book a test ride. Open "Ride History" to see saved bookings.

DATABASE
--------
The first run creates transigo.db automatically in this folder.
Do not delete it if you want to keep the saved bookings.

FARE RULES
----------
Bike: ₹12 per km
Auto: ₹18 per km
Cab: ₹25 per km
Minimum fare: ₹40

These are example values for the school project, not real market prices.
Fare = the greater of ₹40 and (distance × selected rate), rounded to a whole rupee.

IMPORTANT NOTES
---------------
- This is a local educational prototype, not a real transport service.
- It does not contact drivers, track live locations, process payments, or provide real maps.
- Ride history is stored in the local SQLite database.
- "Clear all demo bookings" deletes all rows from this project's database.
- Debug mode is enabled for local learning only. Do not deploy this app publicly as-is.
- The demo secret key should be changed before any real deployment.
