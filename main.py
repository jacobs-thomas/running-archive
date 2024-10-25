# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import datetime

import flask
from flask import Flask, jsonify, render_template, request
import persistance

DATABASE_FILENAME: str = "running_logs.json"
database: persistance.LogsDatabase = persistance.LogsDatabase(DATABASE_FILENAME)

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
	successful, events = database.get_all()  # Retrieve all logs from TinyDB
	if not successful:
		return render_template("index.html", events=[])

	event_dictionaries = [event.to_dictionary_with_id() for event in events]  # Add doc_id to each log
	return render_template("index.html", events=event_dictionaries)


@app.route('/events', methods=["GET"])
def all_logs():
	successful, events = database.get_all()  # Retrieve all logs from TinyDB
	if not successful:
		return jsonify({"successful": False, "message": "Error retrieving the events"}), 404

	event_dictionaries = [event.to_dictionary_with_id() for event in events]  # Add doc_id to each log
	return jsonify({"successful": True, "message": "Success in retrieving the events", "events": event_dictionaries}), 200


@app.route("/delete_log/<int:log_id>", methods=["DELETE"])
def delete_log(log_id: int):
	if database.remove_by_id(log_id):
		return jsonify({"message": "Log deleted successfully", "status": "success"}), 200

	return jsonify({"message": "Log not found", "status": "error"}), 404


@app.route("/add_log", methods=["POST"])
def add_log():
	# Get the JSON data from the request body
	data = request.get_json()

	if data:
		# Extract the data from the JSON
		title = data.get('title')
		date = data.get('date')
		time = data.get('time')
		notes = data.get('notes')

		# Here you can add the logic to save this data to the database
		# For example, using SQLAlchemy or any database of your choice.
		# Assuming a LogModel:
		# new_log = LogModel(title=title, date=date, time=time, notes=notes)
		# db.session.add(new_log)
		# db.session.commit()
		id: int = database.add_log(title, date, time, notes)

		# Return a success response
		return jsonify({'success': True, 'message': 'Log added successfully!', 'date': date, 'title': title, 'time': time, 'notes': notes, 'id': id}), 200
	else:
		# Handle the case where no data is sent
		return jsonify({'status': 'error', 'message': 'No data provided'}), 400


# main driver function
if __name__ == '__main__':
	# For testing only...

	# run() method of Flask class runs the application
	# on the local development server.
	app.run()
