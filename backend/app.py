from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Flask app config
app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

# Use database named in MONGO_URI
staff_collection = mongo.db.staff

# Routes

@app.route("/staff", methods=["GET"])
def get_staff():
    staff = staff_collection.find()
    return jsonify([
        {
            "_id": str(s["_id"]),
            "name": s.get("name"),
            "birthday": s.get("birthday"),
            "house": s.get("house"),
            "contact": s.get("contact", {}),
            "certifications": s.get("certifications", {}),
            "CEUs": s.get("CEUs", {})
        }
        for s in staff
    ])

@app.route("/staff", methods=["POST"])
def add_staff():
    data = request.get_json()
    new_staff = {
        "name": data["name"],
        "birthday": data["birthday"],
        "house": data.get("house"),
        "contact": data.get("contact", {}),
        "certifications": data.get("certifications", {}),
        "CEUs": data.get("CEUs", {})
    }
    result = staff_collection.insert_one(new_staff)
    return jsonify({"message": "Staff added", "id": str(result.inserted_id)}), 201

@app.route("/staff/<id>", methods=["PUT"])
def update_staff(id):
    data = request.get_json()
    result = staff_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count:
        return jsonify({"message": "Staff updated"})
    else:
        return jsonify({"error": "Staff not found"}), 404

@app.route("/staff/<id>", methods=["DELETE"])
def delete_staff(id):
    result = staff_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message": "Staff deleted"})
    else:
        return jsonify({"error": "Staff not found"}), 404

# Run server
if __name__ == "__main__":
    app.run(debug=True)
