from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
import os

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a model for the data
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Ensure the database file exists
if not os.path.exists('data.db'):
    db.create_all()

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Get data from the form
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        message = data.get('message')

        # Validate data
        if not all([name, email, phone, message]):
            logging.error('Validation failed: Missing fields')
            return jsonify({"error": "All fields are required."}), 400

        # Insert data into the database
        new_contact = Contact(name=name, email=email, phone=phone, message=message)
        db.session.add(new_contact)
        db.session.commit()
        logging.info('Data inserted successfully')

        return jsonify({"message": "Form submitted successfully!"}), 200

    except Exception as e:
        logging.error(f'Error processing the form: {e}')
        return jsonify({"error": "An error occurred while processing the form."}), 500

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
