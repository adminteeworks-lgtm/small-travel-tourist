from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os
import re
from datetime import date
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "bookings.db"

# Travel packages and estimated prices per person (PKR)
DESTINATIONS = [
    {
        "id": 1,
        "name": "Hunza Valley",
        "country": "Pakistan",
        "price": 45000,
        "category": "Mountain Adventure"
    },
    {
        "id": 2,
        "name": "Skardu",
        "country": "Pakistan",
        "price": 55000,
        "category": "Nature & Adventure"
    },
    {
        "id": 3,
        "name": "Swat Valley",
        "country": "Pakistan",
        "price": 28000,
        "category": "Family Vacation"
    },
    {
        "id": 4,
        "name": "Murree",
        "country": "Pakistan",
        "price": 22000,
        "category": "Hill Station"
    },
    {
        "id": 5,
        "name": "Dubai",
        "country": "UAE",
        "price": 150000,
        "category": "International Tour"
    },
    {
        "id": 6,
        "name": "Istanbul",
        "country": "Turkey",
        "price": 180000,
        "category": "International Tour"
    }
]


# Database connection
def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# Create database automatically
def initialize_database():
    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                destination TEXT NOT NULL,
                travel_date TEXT NOT NULL,
                travelers INTEGER NOT NULL,
                price_per_person INTEGER NOT NULL,
                total_price INTEGER NOT NULL,
                message TEXT,
                status TEXT DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


initialize_database()


# Serve the website
@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/<path:filename>")
def website_files(filename):
    allowed_files = {"style.css", "script.js"}
    if filename in allowed_files:
        return send_from_directory(BASE_DIR, filename)
    return jsonify({"error": "File not found"}), 404


# Test backend
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "TravelEase backend is running!"
    })


# Get all travel destinations
@app.route("/api/destinations", methods=["GET"])
def get_destinations():
    return jsonify(DESTINATIONS)


# Calculate travel package price
@app.route("/api/calculate", methods=["POST"])
def calculate_price():
    data = request.get_json(silent=True) or {}

    try:
        destination_id = int(data.get("destination_id"))
        travelers = int(data.get("travelers"))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid destination or traveler count"}), 400

    destination = next(
        (item for item in DESTINATIONS
         if item["id"] == destination_id),
        None
    )

    if not destination or not 1 <= travelers <= 20:
        return jsonify({"error": "Please select a valid package and 1-20 travelers"}), 400

    total = destination["price"] * travelers

    return jsonify({
        "destination": destination["name"],
        "travelers": travelers,
        "price_per_person": destination["price"],
        "total_price": total,
        "currency": "PKR"
    })


# Submit a travel booking
@app.route("/api/bookings", methods=["POST"])
def create_booking():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    phone = str(data.get("phone", "")).strip()
    travel_date = str(data.get("travel_date", "")).strip()
    message = str(data.get("message", "")).strip()

    try:
        destination_id = int(data.get("destination_id"))
        travelers = int(data.get("travelers"))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid booking details"}), 400

    destination = next(
        (item for item in DESTINATIONS
         if item["id"] == destination_id),
        None
    )

    if not name or len(name) > 100:
        return jsonify({"error": "Enter a valid customer name"}), 400

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return jsonify({"error": "Enter a valid email address"}), 400

    if not re.fullmatch(r"[0-9+\-\s()]{7,20}", phone):
        return jsonify({"error": "Enter a valid phone number"}), 400

    if not destination:
        return jsonify({"error": "Please select a destination"}), 400

    try:
        selected_date = date.fromisoformat(travel_date)
        if selected_date < date.today():
            raise ValueError
    except ValueError:
        return jsonify({"error": "Choose a valid future travel date"}), 400

    if not 1 <= travelers <= 20:
        return jsonify({"error": "Travelers must be between 1 and 20"}), 400

    if len(message) > 1000:
        return jsonify({"error": "Message is too long"}), 400

    price = destination["price"]
    total = price * travelers

    with get_db() as connection:
        cursor = connection.execute("""
            INSERT INTO bookings (
                customer_name, email, phone, destination,
                travel_date, travelers, price_per_person,
                total_price, message
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, email, phone, destination["name"],
            travel_date, travelers, price, total, message
        ))

        booking_id = cursor.lastrowid

    return jsonify({
        "status": "success",
        "message": "Your travel booking has been received!",
        "booking_id": booking_id,
        "destination": destination["name"],
        "total_price": total,
        "currency": "PKR"
    }), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)

