"""Tests for `metad` package."""

from glob import glob
from unittest import TestCase

from parameterized import parameterized

from metad import MetaData


class TestMetaData(TestCase):

    @parameterized.expand(glob("examples/**/metadata.json"))
    def test_validation(self, path_to_example):
        metadata = MetaData.from_json(path_to_example)
        metadata.validate()
        assert str(metadata)

    def test_creation(self):
        metadata = MetaData()
        metadata.add_table({
            "name": "users",
            "fields": [
                {"name": "user_id", "data_type": "id"},
                {"name": "name", "data_type": "text"},
                {"name": "gender", "data_type": "categorical"},
                {"name": "age", "data_type": "numerical"},
                {"name": "birthday", "data_type": "datetime"},
                {"name": "picture", "data_type": "other"}
            ]
        })
        assert len(metadata.get_table_names()) == 1
        assert "users" in metadata.get_table_names()
