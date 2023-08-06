from enum import Enum
from re import Pattern
from typing import Callable, Any


class ValidatorError(Enum):
	MISSING_KEY = 1
	INVALID_TYPE = 2
	INVALID_VALUE = 3
	NUMBER_NOT_IN_RANGE = 4
	LENGTH_NOT_IN_RANGE = 5
	INVALID_SCHEMA = 6


class Validator:
	def __init__(self, data: dict | list | None = None, exact_keys: bool = False):
		self._exact_keys = exact_keys
		self._schema = {}
		for key, val in self.__class__.__dict__.items():
			if key[0] == "_":
				continue
			if type(val) == Rule:
				self._schema[key] = val
		if data is not None:
			self._init_validation_result = self.__call__(data)

	def __iter__(self):
		for key, val in self._schema.items():
			yield (key, val)

	def __repr__(self) -> str:
		# TODO: output swagger format
		return ""

	def __call__(self, data, *args, **kwargs) -> tuple[bool, Any, str]:
		if self._exact_keys:
			for key in data:
				if key not in self._schema.keys():
					return False, ValidatorError.INVALID_SCHEMA, ""
		for key, rule in self._schema.items():
			if key not in data:
				if rule.optional:
					self.__dict__[key] = None
					continue
				else:
					return False, ValidatorError.MISSING_KEY, key
			result = rule.check(data[key])
			if not result[0]:
				return (
					False,
					result[1],
					"%s%s%s" % (key, "->" if len(result[-1]) else "", result[-1])
				)
			self.__dict__[key] = data[key]
		return self._validate(data)

	def _validate(self, data) -> tuple[bool, Any | None, str]:
		return True, None, ""


class Rule:
	def __init__(
		self,
		data_type: type,
		optional: bool = False,
		min: int | float | None = None,
		max: int | float | None = None,
		length: int | None = None,
		min_length: int | None = None,
		max_length: int | None = None,
		regex: Pattern | None = None,
		check_method: Callable = lambda x, *a: True,
		validator: Validator | None = None
	):
		if (min is not None or max is not None) and data_type not in (int, float):
			raise NotImplementedError(
				"Parameters `min` and `max` can be used only with `int` or `float` type"
			)
		if (
			(length is not None or min_length is not None or max_length is not None) and
			data_type not in (str, list)
		):
			raise NotImplementedError(
				"Parameters `length`, `min_length` and `max_lenght` can be used only with "
				"`str` or `list` type"
			)
		if regex and data_type not in (str, bytes):
			raise NotImplementedError(
				"Parameter `regex` can be used only with `str` or `bytes` type"
			)
		if validator and data_type not in (list, dict):
			raise NotImplementedError(
				"Parameter `validator` can be used only with `list` or `dict` type"
			)
		self.__type = data_type
		self.__optional = optional
		self.__min = min
		self.__max = max
		self.__regex = regex
		self.__check_method = check_method
		self.__validator = validator

	def __iter__(self):
		out = {
			"type": self.__type,
			"optional": self.__optional,
			"check_method": self._check_method,
		}
		if self.__type in (str, bytes):
			out["regex"] = self.__regex
		if self.__type in (list, dict):
			out["validator"] = self.__validator
		for key, val in out.items():
			yield (key, val)

	def __repr__(self) -> str:
		# TODO: output swagger format
		return ""

	def check(self, value) -> tuple[bool, ValidatorError | None, str]:
		if type(value) != self.__type:
			return False, ValidatorError.INVALID_TYPE, ""
		elif (
			(self.__min is not None and self.__min > value) or  # type: ignore
			(self.__max is not None and self.__max < value)  # type: ignore
		):
			return False, ValidatorError.NUMBER_NOT_IN_RANGE, ""
		elif (
			(self.__length is not None and self.__lenght > len(value)) or  # type: ignore
			(self.__min_length is not None and self.__min_length > len(value)) or  # type: ignore
			(self.__max_length is not None and self.__max_length > len(value))  # type: ignore
		):
			return False, ValidatorError.NUMBER_NOT_IN_RANGE, ""
		elif self.__regex and self.__regex.match(value) or self.__check_method(value):  # type: ignore
			return False, ValidatorError.INVALID_VALUE, ""
		elif self.__validator:
			self.__validator.check(value)  # type: ignore
		return True, None, ""

	@property
	def type(self) -> type:
		return self.__type

	@property
	def optional(self) -> bool:
		return self.__optional

	@property
	def min(self) -> int | float | None:
		if self.__type not in (int, float):
			raise NotImplementedError(
				"Property `min` works with `int` or `float` type"
			)
		return self.__min

	@property
	def max(self) -> int | float | None:
		if self.__type not in (int, float):
			raise NotImplementedError(
				"Property `max` works with `int` or `float` type"
			)
		return self.__max

	@property
	def regex(self) -> Pattern | None:
		if self.__type not in (str, bytes):
			raise NotImplementedError("Property `regex` works only with `str` or `bytes` type")
		else:
			return self.__regex

	@property
	def check_method(self):
		self.__check_method

	@property
	def validator(self):
		if self.__type not in (list, dict):
			raise NotImplementedError("Property `validator` works only with `list` or `dict` type")
		else:
			return self.__validator


class RequestValidator(Validator):
	def __init__(self, exact_keys: bool = False):
		super().__call__(exact_keys)

	def __call__(self, method, *args, **kwargs):
		async def wrapper(req, resp, *args, **kwargs):
			result = super().__call__(req.data)
			if result[0]:
				return await method(req, resp, *args, data=self, **kwargs)
			else:
				await resp.abort(400, {
					"status": False,
					"code": 401,
					"message": "BAD_REQUEST",
					"additional_info": [result[1], result[2]]
				})
		return wrapper
