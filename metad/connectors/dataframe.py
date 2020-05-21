import copy
import os

from metad.connectors.base import BaseConnector


class DataFrameConnector(BaseConnector):
    """Import data from pandas DataFrames.

    The DataFrameConnector allows you to import data from pandas
    DataFrames. It automatically populates the tables and fields; it also
    infers the data types from the data.
    """

    _FIELD_TEMPLATES = {
        'i': {
            'data_type': 'numerical',
            'data_subtype': 'integer',
        },
        'f': {
            'data_type': 'numerical',
            'data_subtype': 'float',
        },
        'O': {
            'data_type': 'categorical',
        },
        'b': {
            'data_type': 'boolean',
        },
        'M': {
            'data_type': 'datetime',
        }
    }

    def __init__(self, tables):
        """Create a new DataFrameConnector.

        Args:
            tables (dict): A dictionary mapping from table names to pandas
            DataFrames.
        """
        super().__init__()
        self.tables = tables
        self.metadata.set_tables(self._analyze_tables())

    def export_metadata(self, path_to_json):
        self.metadata.to_json(path_to_json)

    def export_tables(self, path_to_output):
        for table_name, dataframe in self.tables.items():
            dataframe.to_csv(
                os.path.join(
                    path_to_output,
                    "%s.csv" %
                    table_name), index=False)

    def _analyze_tables(self):
        table_metadata = []
        for table_name, dataframe in self.tables.items():
            table_metadata.append({
                "name": table_name,
                "fields": self._analyze_fields(dataframe)
            })
        return table_metadata

    def _analyze_fields(self, dataframe):
        fields = []
        for field in dataframe.columns:
            dtype = dataframe[field].dtype
            field_metadata = self._FIELD_TEMPLATES.get(dtype.kind)
            field_metadata = copy.deepcopy(field_metadata)
            field_metadata["name"] = field
            fields.append(field_metadata)
        return fields
