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
