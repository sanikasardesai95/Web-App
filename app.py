from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
import os

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/sanik/Desktop/Web-App_Assignment/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Set up logging to a file
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a model for the data
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Ensure the database file exists and initialize tables
if not os.path.exists('C:/Users/sanik/Desktop/Web-App_Assignment/data.db'):
    with app.app_context():
        db.create_all()

@app.route('/initialize_db')
def initialize_db():
    try:
        # Ensure the tables are created
        with app.app_context():
            db.create_all()
        return jsonify({"message": "Database initialized successfully!"}), 200
    except Exception as e:
        logging.error(f'Error initializing the database: {e}')
        return jsonify({"error": f"An error occurred during initialization: {e}"}), 500

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Log the request
        logging.info('Received form submission request')

        # Get data from the form
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        message = data.get('message')

        # Validate data
        if not all([name, email, phone, message]):
            logging.error('Validation failed: Missing field')
            return jsonify({"error": "All fields are required."}), 400

        # Insert data into the database
        new_contact = Contact(name=name, email=email, phone=phone, message=message)
        db.session.add(new_contact)
        db.session.commit()
        logging.info('Data inserted successfully')

        return jsonify({"message": "Form submitted successfully!"}), 201

    except Exception as e:
        logging.error(f'Error processing the form: {e}')
        return jsonify({"error": "An error occurred while processing the form."}), 500

@app.route('/test_db')
def test_db():
    try:
        # Create a test record
        test_contact = Contact(name="Test User", email="test@example.com", phone="1234567890", message="Hello World!")
        db.session.add(test_contact)
        db.session.commit()

        # Retrieve the record
        retrieved_contact = Contact.query.filter_by(name="Test User").first()
        
        if retrieved_contact:
            return jsonify({
                "name": retrieved_contact.name,
                "email": retrieved_contact.email,
                "phone": retrieved_contact.phone,
                "message": retrieved_contact.message
            })
        else:
            return jsonify({"error": "Test record not found"}), 404
        
    except Exception as e:
        logging.error(f'Error testing the database: {e}')
        return jsonify({"error": f"An error occurred: {e}"}), 500

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
