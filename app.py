from flask import Flask, request, jsonify

app = Flask(__name__)

destinations = [
    {"name": "Hunza Valley", "price": 25000},
    {"name": "Skardu", "price": 35000},
    {"name": "Murree", "price": 15000},
    {"name": "Swat", "price": 20000}
]

@app.route("/")
def home():
    return "Welcome to Explore Pakistan Travel Agency!"

@app.route("/destinations")
def get_destinations():
    return jsonify(destinations)

@app.route("/book", methods=["POST"])
def book_trip():
    data = request.json

    name = data.get("name")
    destination = data.get("destination")
    people = int(data.get("people", 1))

    return jsonify({
        "message": "Booking request received successfully!",
        "customer": name,
        "destination": destination,
        "people": people
    })

if __name__ == "__main__":
    app.run(debug=True)
  
