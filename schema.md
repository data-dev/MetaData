# JSON Schema

The root object of a Metadata.JSON object contains the following fields.

| **Field**    | **Description**                                        |
|--------------|--------------------------------------------------------|
| path         | This is a string representing the path to the dataset. |
| tables       | This is a list of `Table` objects.                     |
| foreign_keys | This is a list of `ForeignKey` objects.                |
| constraints  | This is a list of `Constraint` objects.                |

## Tables

The `Table` object contains the following fields.

| **Field**      | **Description**                                                                                                                    |
|----------------|------------------------------------------------------------------------------------------------------------------------------------|
| path           | This is the path to the CSV file containing the table.                                                                             |
| name           | This is the name of the table.                                                                                                     |
| primary_key    | This can be either (1) a string representing the primary key column or (2) a list of strings representing the primary key columns. |
| time_index     | This string specifies the column that is the time index.                                                                           |
| headers        | This boolean indicates whether the file contains a header row.                                                                     |
| number_of_rows | This contains the number of rows in the table.                                                                                     |
| fields         | This is a list of `Field` objects.                                                                                                 |
| system         | This is the system the table originated from.                                                                                      |
| application    | This is the application the table originated from.                                                                                 |

Each field in the `Table` object is specified by a dictionary containing:

| **Field**    | **Description**                                           |
|--------------|-----------------------------------------------------------|
| name         | This is a string representing the name of the field.      |
| data_type    | This is the data type of the field.                       |
| data_subtype | This is the subtype which is only defined for some types. |

#### Data Types

The `data_type` and `data_subtype` fields can take on the following values:

 - categorical
    - subtypes: categorical, ordinal, boolean
 - text
 - numerical
    - subtypes: integer, float
 - datetime
 - id
 - other

## Foreign Keys

The `ForeignKey` object contains the following fields.

| **Field** | **Description**                                                                                                                    |
|-----------|------------------------------------------------------------------------------------------------------------------------------------|
| table     | This is a string representing the child table.                                                                                     |
| field     | This can be either (1) a string representing the foreign key column or (2) a list of strings representing the foreign key columns. |
| ref_table | This is a string representing the parent table.                                                                                    |
| ref_field | This can be either (1) a string representing the foreign key column or (2) a list of strings representing the foreign key columns. |

## Constraints

The `Constraint` object contains the following fields.

| **Field**                  | **Description**                                                           |
|----------------------------|---------------------------------------------------------------------------|
| constraint_type            | This is the type of `Constraint`.                                         |
| fields_under_consideration | This is the field(s) of interest.                                         |
| related_fields             | This is the related field(s) that contribute to the field(s) of interest. |

### Fields

Each field in the `Contraint` object is specified by a dictionary containing:

| **Field** | **Description**         |
|-----------|-------------------------|
| table     | The name of the table.  |
| field     | The name of the column. |
