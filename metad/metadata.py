import copy
import json
import os

import fastjsonschema

base_directory = os.path.dirname(__file__)
path_to_schema = os.path.join(base_directory, "schema.json")
with open(path_to_schema, "rt") as fin:
    validate = fastjsonschema.compile(json.load(fin))


class MetaData():
    """Read, write, and validate metadata.

    The MetaData object provides methods to help read, write, and validate
    metadata. It uses the JSON schema, which can be found in `schema.json`,
    to validate the structure of the metadata and applies additional logic
    checks internally.
    """

    def __init__(self):
        self.data = {
            "tables": [],
            "foreign_keys": [],
            "constraints": []
        }

    def __str__(self):
        text = ""
        text += "Number of Tables: %s\n" % len(self.data["tables"])
        text += "Number of Foreign Keys: %s\n" % len(self.data["foreign_keys"])
        text += "Number of Constraints: %s\n" % len(self.data["constraints"])
        text += "\n"
        for table in self.data["tables"]:
            primary_keys = []
            if "primary_key" in table:
                primary_keys = table["primary_key"]
                if isinstance(table["primary_key"], str):
                    primary_keys = [table["primary_key"]]

            text += "Table: %s\n" % table["name"]
            for field in table["fields"]:
                if field["name"] in primary_keys:
                    text += "   *%s\n" % field["name"]
                else:
                    text += "    %s\n" % field["name"]
            text += "\n"
        return text

    def to_json(self, path_to_json=None):
        """Export the MetaData object to a JSON file.

        Args:
            path_to_json (str, optional): The path to the JSON file
            which should be created. If set to None, the JSON object
            is returned as a string.
        """
        if path_to_json:
            with open(path_to_json, "wt") as fp:
                json.dump(self.data, fp, indent=2)
        return json.dumps(self.data, indent=2)

    @staticmethod
    def from_json(path_to_json):
        """Load a MetaData object from a JSON file.

        Args:
            path_to_json (str): The path to the JSON file.

        Returns:
            MetaData: An instance of the MetaData object.
        """
        metadata = MetaData()
        with open(path_to_json, "rt") as fp:
            metadata.data = json.load(fp)
        return metadata

    def validate(self):
        """Validate the contents of this metadata object.

        This validates the metadata against the JSON schema. It also performs
        additional logic checks (i.e. that table/field names are unique) to
        ensure that the metadata is valid.

        Raises:
            AssertionError: If the metadata is not valid.
        """
        validate(self.data)

        # Assert that field names are unique
        table_names, field_names = [], []
        for table in self.data["tables"]:
            table_names.append(table["name"])
            for field in table["fields"]:
                field_names.append((table["name"], field["name"]))
        assert len(table_names) == len(set(table_names))
        assert len(field_names) == len(set(field_names))

        # Assert that the foreign key fields exist
        if "foreign_keys" in self.data:
            for key in self.data["foreign_keys"]:
                if isinstance(key["field"], str):
                    assert (key["table"], key["field"]) in field_names
                    assert (key["ref_table"], key["ref_field"]) in field_names
                else:
                    for field in key["field"]:
                        assert (key["table"], field) in field_names
                    for ref_field in key["ref_field"]:
                        assert (key["ref_table"], ref_field) in field_names

        # Assert that the constraint fields exist
        if "constraints" in self.data:
            for constraint in self.data["constraints"]:
                for field in constraint["fields_under_consideration"]:
                    assert (field["table"], field["field"]) in field_names, field
                for field in constraint["related_fields"]:
                    assert (field["table"], field["field"]) in field_names, field

    def add_table(self, table):
        """Add the table object to the metadata.

        The table object must conform the the JSON schema specification.

        Args:
            table (dict): A dictionary representing the table.
        """
        self.data["tables"].append(copy.deepcopy(table))
        self.validate()

    def add_foreign_key(self, foreign_key):
        """Add the foreign key object to the metadata.

        The foreign key object must conform the the JSON schema specification.

        Args:
            foreign_key (dict): A dictionary representing the foreign key relationship.
        """
        if "foreign_keys" not in self.data:
            self.data["foreign_keys"] = []
        self.data["foreign_keys"].append(copy.deepcopy(foreign_key))
        self.validate()

    def add_constraint(self, constraint):
        """Add the constraint object to the metadata.

        The constraint table object must conform the the JSON schema specification.

        Args:
            constraint (dict): A dictionary representing the constraint relationship.
        """
        if "constraints" not in self.data:
            self.data["constraints"] = []
        self.data["constraints"].append(copy.deepcopy(constraint))
        self.validate()

    def set_tables(self, tables):
        for table in tables:
            self.add_table(table)
            self.validate()

    def set_foreign_keys(self, foreign_keys):
        for foreign_key in foreign_keys:
            self.add_foreign_key(foreign_key)
            self.validate()

    def get_tables(self):
        return copy.deepcopy(self.data["tables"])

    def get_table(self, table_name):
        for table in self.data["tables"]:
            if table["name"] == table_name:
                return table

    def get_table_names(self):
        return copy.deepcopy([table["name"] for table in self.data["tables"]])

    def add_field(self, table_name, field):
        for table in self.data["tables"]:
            if table["name"] == table_name:
                table["fields"].append(field)
        self.validate()

    def get_foreign_keys(self, table_name=None):
        if table_name:
            foreign_keys = []
            for foreign_key in self.data["foreign_keys"]:
                if foreign_key["table"] == table_name:
                    foreign_keys.append(foreign_key)
                if foreign_key["ref_table"] == table_name:
                    foreign_keys.append(foreign_key)
            return copy.deepcopy(foreign_keys)
        return copy.deepcopy(self.data["foreign_keys"])
