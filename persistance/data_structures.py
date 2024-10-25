import datetime
from typing import Dict


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

	def to_dictionary_with_id(self) -> Dict[str, str]:
		return {
			"id": self.id,
			"title": self.name,
			"date": self.__date.isoformat(),
			"notes": self.description
		}
