from dataclasses import fields
import random
from typing import *
import os
import json


def fields_names(table):
    return map(lambda field: field.name, fields(table))


def load_config(table, fp):
    if fp in os.listdir():
        with open(fp, "r") as conf:
            apply_changes(table, json.load(conf))


def apply_changes(table, changes: dict):
    for field_name in changes:
        setattr(table, field_name, getattr(table, field_name).apply_changes(changes.get(field_name, {})))


def generate(table):
    """
    Generates random row in table
    :param table:
    :return:
    """
    return {name: getattr(table, name).get() for name in fields_names(table)}


def generate_paired(table1, table2, keys: List[str]):
    """
    Generates random row in two tables that paired by keys
    :param table1:
    :param table2:
    :param keys:
    :return:
    """
    assert len(keys) > 0
    assert all(map(lambda key: key in fields_names(table1), keys))
    assert all(map(lambda key: key in fields_names(table2), keys))
    intersect_data = {}
    for key in keys:
        intersect_generator = getattr(table1, key).intersect(getattr(table2, key))
        val = None
        if not (intersect_generator is None):
            val = intersect_generator.get()
        intersect_data[key] = val
    first = {i: getattr(table1, i).get() for i in fields_names(table1) if i not in keys}
    second = {i: getattr(table2, i).get() for i in fields_names(table2) if i not in keys}
    first = {**first, **intersect_data}
    second = {**second, **intersect_data}
    assert all(map(lambda key: first.get(key) == second.get(key), keys))
    return first, second


class SparkField:
    def intersect(self, other):
        """
        :param other:
        :return:
        new SparkField which generates data that satisfies both conditions
        """
        return None

    def apply_changes(self, changes: dict):
        """
        applies config to field
        :param changes:
        :return:
        """
        pass


class Range(SparkField):
    def __init__(self, data_type, a, b):
        self.data_type = data_type
        assert a <= b
        self.a = None
        self.b = None
        self.set_range(a, b)

    def set_range(self, a, b) -> SparkField:
        assert a <= b
        self.a = a
        self.b = b
        return self

    def create_new(self, *args, **kwargs) -> SparkField:
        pass

    def get(self) -> Union[int, float]:
        pass

    def intersect(self, other) -> Optional[SparkField]:
        if isinstance(other, Range):
            if self.b < other.a or other.b < self.a or not (self.data_type is other.data_type):
                return None
            return self.create_new(max(self.a, other.a), min(self.b, other.b))
        return super().intersect(other)

    def apply_changes(self, changes: dict) -> SparkField:
        new_a, new_b = changes.get("a", self.a), changes.get("b", self.b)
        if new_a > new_b:
            return self
        return self.create_new(new_a, new_b)


class IntegerRange(Range):
    """
    Generates random integer from a to b
    """

    def __init__(self, a, b):
        super().__init__(int, a, b)

    @staticmethod
    def create_new(*args, **kwargs):
        return IntegerRange(*args, **kwargs)

    def get(self) -> int:
        return random.randint(self.a, self.b)


class FloatRange(Range):
    """
    Generates random float from a to b
    """

    def __init__(self, a, b):
        super().__init__(float, a, b)

    @staticmethod
    def create_new(*args, **kwargs):
        return FloatRange(*args, **kwargs)

    def get(self) -> int:
        return random.random() * (self.b - self.a) + self.a
