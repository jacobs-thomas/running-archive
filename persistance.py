import logging
import os

from flask import jsonify
from tinydb import TinyDB, Query
from typing import List, Dict, Any, Tuple, Optional
import datetime


class Event:
	# Initializer:
	def __init__(self, id: int, name: str, date: str, description: str):
		# Instance attributes:
		self.__id: int = id
		self.name: str = name
		self.description: str = description

		try:
			self.__date = datetime.datetime.fromisoformat(date)
		except Exception as exception:
			self.__date = datetime.datetime.now()

	# Properties:
	@property
	def id(self) -> int:
		return self.__id

	@property
	def date(self) -> str:
		return self.__date.isoformat()

	@date.setter
	def date(self, value: datetime.datetime) -> None:
		try:
			self.__date = value
		except Exception as exception:
			self.__date = datetime.datetime.now()

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
	def get_all(self) -> List[Event]:
		try:
			events = self._tinyDatabase.all()
			return [Event(event.doc_id, event.get("title"), event.get("date"), event.get("notes")) for event in events]

		except Exception as exception:
			logging.exception(exception)

	def get(self, id: int) -> Tuple[bool, Optional[Event]]:

		try:
			query_response = self._tinyDatabase.get(doc_id=id)

			if query_response is None:
				return False, None

			return True, Event(query_response.doc_id, query_response.get("title"), query_response.get("date"), query_response.get("notes"))

		except Exception as exception:
			logging.exception(exception)
			return False, None

	def update(self, event: Event) -> bool:

		try:
			query_response: list[int] = self._tinyDatabase.update(event.to_dictionary(), doc_ids=[event.id])

			return len(query_response) > 0

		except Exception as exception:
			logging.exception(exception)
			return False

	def delete(self, id: int) -> bool:
		try:
			# Check if the item exists
			if self._tinyDatabase.contains(doc_id=id):
				query_response = self._tinyDatabase.remove(doc_ids=[id])
				return len(query_response) > 0  # True if deletion was successful
			else:
				logging.log(f"Event with id: {id} does not exist.")
				return False
		except Exception as exception:
			logging.exception(exception)
			return False


test = LogsDatabase("running_logs.json")
result, event_object = test.get(5)
all = test.get_all()

if result:
	event_object.name = "Ipswich parkrun"
	test.update(event_object)
