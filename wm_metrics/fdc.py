# -*- coding: utf-8 -*-

"""FDC module dealing with quarter."""

import time

class Round:
	"""
	FDC Round allows to compute accurate timestamps for start and end of each quarter of the round.
	"""

	QUARTER = [
		{'start' : "0101000000", 'end' : "0331235959"},
		{'start' : "0401000000", 'end' : "0630235959"},
		{'start' : "0701000000", 'end' : "0930235959"},
		{'start' : "1001000000", 'end' : "1231235959"}
	]

	def __init__(self, year1, year2, round_number):
		"""Constructor.

		Args:
			year1 (int): Year of request of round 1
			year2 (int): Year of request of round 2
			round_number (int): FDC round number,
				either 1 for round 1 and 2 for round 2

		Raises:
			ValueError: if round is not 1 or 2
		"""
		self.year1 = year1
		self.year2 = year2
		if round_number in [1, 2]:
			self.round = round_number
		else:
			raise ValueError("Round number should be either 1 or 2 but is %d" % round_number)

	def quarter(self, quarter):
		"""Returns the timestamp of start and end of the quarter.

		Args:
			quarter (int): Number of the quarter (values are between 1 and 4)

		Returns:
			both timestamp of start and end of the quarter as {'start': "XXX", 'end': "YYY"}

		Raises:
			ValueError: if quarter is not in 1..4
		"""
		year = self.year2
		index= quarter-1
		if not quarter in range(1, 5):
			raise ValueError("quarter should be between 1 and 4 but is %d" % quarter)
		if self.round==2:
			index = (quarter+1)%4
			if quarter >=3:
				year = self.year2+1
		return {
			'start' : str(year) + Round.QUARTER[index]['start'],
			'end' : str(year) + Round.QUARTER[index]['end'] }

	def _today(self):
		"""Returns timestamp of today 0000Z"""
		return time.strftime("%Y%m%d000000", time.gmtime())

class Indicator:
	"""Indicator for FDC reports have values for Q1, Q2, Q3, Q4 or/and a value.
	it allows to follow the evolution of an indicator during the quarters and have its final value
	or to follow an indicator with only a single value.
	"""

	def __init__(self, name, q1=None, q2=None, q3=None, q4=None, value=None):
		"""Constructor returns an indicator.
		it can be initilized with values for q1, q2, q3, q4 and another value (cumulative)

		Args:
			name (str): Unique name (can be used to refer to the indicator)
			q1 (float): Value at first quarter (optional)
			q2 (float): Value at second quarter (optional)
			q3 (float): Value at third quarter (optional)
			q4 (float): Value at fourth quarter (optional)
			value (float): A value of the indicator that has no relation to a quarter: cumulative value, fixed value, whatever (optional)
		"""
		self.name = name
		self.values = dict()
		self.values["q1"] = q1
		self.values["q2"] = q2
		self.values["q3"] = q3
		self.values["q4"] = q4
		self.values["value"] = value
