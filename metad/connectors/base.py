import os

from metad import MetaData


class BaseConnector():

    def __init__(self):
        self.metadata = MetaData()

    def export(self, path_to_output):
        """Export the relational dataset.

        This exports the relational dataset to the output directory. It
        write the metadata to a JSON file and stores the tables as CSV files
        where the name of the file is the table name.

        Args:
            path_to_output (str): The path to the output directory.
        """
        os.makedirs(path_to_output, exist_ok=True)
        self.export_metadata(os.path.join(path_to_output, "metadata.json"))
        self.export_tables(path_to_output)

    def export_metadata(self, path_to_json):
        """Write the metadata to a JSON file.

        Args:
            path_to_json (str): The path to the output JSON.
        """
        raise NotImplementedError()

    def export_tables(self, path_to_output):
        """Write the tables to CSV files.

        Args:
            path_to_output (str): The path to the output directory.
        """
        raise NotImplementedError()
