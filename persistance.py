import os

from flask import jsonify
from tinydb import TinyDB, Query
from typing import List, Dict, Any, Tuple, Optional
import datetime


class Event:
	# Initializer:
	def __init__(self, name: str, date: datetime, description: str):
		# Instance attributes:
		self.name: str = name
		self.description: str = description
		self.__date: datetime = date

	# Properties:
	@property
	def date(self) -> str:
		return self.__date.isoformat()

	@date.setter
	def date(self, value: datetime) -> None:
		self.__date = value

	def set_date_time(self, date: str, time: str) -> None:
		"""
		Sets the date and time from separate date and time strings.
		Combines them into an ISO format datetime string.

		:param date: Date string in 'YYYY-MM-DD' format.
		:param time: Time string in 'HH:MM' format.
		:return: None
		"""
		try:
			# Combine date and time into ISO format
			combined_str = f"{date}T{time}"

			# Parse the combined string into a datetime object
			dt = datetime.strptime(combined_str, '%Y-%m-%dT%H:%M')

			# Store the datetime object
			self.__date = dt
		except ValueError as e:
			# Log or handle the error appropriately
			print(f"Error setting date and time: {e}")
			return

	def to_dictionary(self) -> Dict[str, str]:
		"""
		Converts the Event object into a dictionary format.

		:return: Dictionary representation of the event.
		"""
		return {
			"title": self.name,
			"date": self.__date.isoformat(),
			"notes": self.description
		}


class Database:
	# Constructor:
	def __init__(self, filename: str) -> None:
		"""Initialize the TinyDB database."""
		if not os.path.exists(filename):
			raise FileNotFoundError(f"Database file '{filename}' does not exist.")
		self._tinyDatabase = TinyDB(filename)

	# Methods:
	def insert(self, data: Dict[str, Any]) -> None:
		"""Insert a new record into the database."""
		try:
			self._tinyDatabase.insert(data)

		except ValueError as exception:
			print(f"Error inserting data: {exception}")

	def search(self, query: Query) -> List[Dict[str, Any]]:
		"""Search for records that match the query."""
		return self._tinyDatabase.search(query)

	def all(self) -> List[Dict[str, Any]]:
		"""Retrieve all records in the database."""
		return self._tinyDatabase.all()

	def close(self) -> None:
		"""Close the database (optional; not strictly necessary with TinyDB)."""
		self._tinyDatabase.close()


# Serialization: Convert datetime to ISO 8601 string
def _serialize_log(date: datetime.datetime, distance: float, time: str, notes: str) -> Dict[str, Any]:
	return {
		"date": date.isoformat(),  # Convert datetime to string
		"distance": distance,  # Keep as float
		"time": time,
		"notes": notes
	}


# Deserialization: Convert ISO 8601 string back to datetime object
def _deserialize_log(log: Dict[str, Any]) -> Dict[str, Any]:
	log["date"] = datetime.datetime.fromisoformat(log["date"])  # Convert back to datetime
	return log


def combine_to_iso(date: str, time: str):
	# Combine date and time into ISO format
	combined_str = f"{date}T{time}"

	# Parse the combined string into a datetime object
	# Assuming the time part is 'HH:MM'
	dt = datetime.datetime.strptime(combined_str, '%Y-%m-%dT%H:%M')

	# Return the datetime object in ISO 8601 format
	return dt.isoformat()


# Base class for the database
class Database:
	def __init__(self, filename: str) -> None:
		self._tinyDatabase = TinyDB(filename)

	def insert(self, log: Dict[str, Any]) -> int:
		return self._tinyDatabase.insert(log)

	def search(self, query: Query) -> List[Dict[str, Any]]:
		return self._tinyDatabase.search(query)

	def remove(self, query: Query):
		return self._tinyDatabase.remove(query)


# LogsDatabase class extending the Database class
class LogsDatabase(Database):
	def __init__(self, filename: str) -> None:
		"""Initialize the LogsDatabase."""
		super().__init__(filename)

	# Add a new log entry
	def add_log(self, title: str, date: str, time: str, notes: str) -> int:
		datetime_iso = combine_to_iso(date, time)

		row = {
			"title": title,
			"date": datetime_iso,  # Convert datetime to string
			"notes": notes
		}

		return self.insert(row)

	# Get logs where the distance is greater than a specified value
	def get_logs_over_distance(self, min_distance: float) -> List[Dict[str, Any]]:
		log = Query()
		logs = self.search(log.distance > min_distance)

		# Deserialize the logs before returning
		return [_deserialize_log(log) for log in logs]

	def delete_log(self, id: int):
		result = self._tinyDatabase.remove(doc_ids=[id])
		return result

	# Retrieve all logs in the database
	def all(self) -> List[Dict[str, Any]]:
		entries = self._tinyDatabase.all()

		# Deserialize all logs
		# return entries
		return [_deserialize_log(entry) for entry in entries]

	def remove_by_id(self, id: int):
		return self._tinyDatabase.remove(doc_ids=[id])

	# new methods:
	def get(self, id: int) -> Tuple[bool, Optional[Dict[str, Any]]]:
		"""
		Retrieve an item from the TinyDB database using its document ID.

		This method queries the TinyDB instance for an entry with the specified
		document ID (doc_id). If the entry is found, it returns a tuple containing
		a success flag (True) and the item's data as a dictionary. If no entry is
		found, it returns a tuple with a failure flag (False) and None.

		:param id: The document ID of the item to retrieve. This should be an integer
				   representing the unique identifier assigned by TinyDB upon insertion.

		:return: A tuple where the first element is a boolean indicating the success
				 of the retrieval operation. The second element is either a dictionary
				 containing the item data if found, or None if no item exists with the
				 given ID. The dictionary will have key-value pairs corresponding to
				 the attributes of the stored item.
		"""

		query_response = self._tinyDatabase.get(doc_id=id)

		if query_response is None:
			return False, None

		return True, query_response

	def update(self, id: int, data) -> bool:
		"""
		Update an item in the TinyDB database using its document ID.

		This method modifies an existing entry in the TinyDB database. It finds the
		entry with the specified document ID and updates it with the provided data.
		The method returns a boolean indicating whether the update was successful.

		:param id: The document ID of the item to update. This should be an integer
				   representing the unique identifier assigned by TinyDB upon insertion.

		:param data: A dictionary containing the new values for the item's fields.
					 This can include one or more fields of the item to be updated,
					 and any field not included will remain unchanged.

		:return: A boolean value indicating the success of the update operation.
				 It returns True if the item was successfully updated (i.e., if the
				 item with the specified ID exists and has been modified), or False
				 if the item does not exist or if no changes were made.
		"""

		query_response: list[int] = self._tinyDatabase.update(data, doc_ids=[id])

		return len(query_response) > 0

	def delete(self, id: int) -> bool:
		"""
		Remove a document from TinyDB by a condition matching the doc_id.

		:param doc_id: The unique document ID in TinyDB.
		:return: True if the document was successfully deleted, False otherwise.
		"""

		try:
			# Check if the item exists
			if self._tinyDatabase.contains(doc_id=id):
				query_response = self._tinyDatabase.remove(doc_ids=[id])
				return len(query_response) > 0  # True if deletion was successful
			else:
				print(f"Item with doc_id {id} does not exist.")
				return False
		except Exception as e:
			print(f"Error while deleting doc_id {id}: {e}")
			return False


test = LogsDatabase("running_logs.json")
test.get(5)
