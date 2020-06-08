# JSON Schema

The root object of a Metadata.JSON object contains the following fields.

| **Field**      | **Type**           | **Description**                                   |
|----------------|--------------------|---------------------------------------------------|
| `path`         | `String`           | Path to the dataset.                              |
| `tables`       | `List[Table]`      | Tables that compose this dataset.                 |
| `foreign_keys` | `List[ForeignKey]` | Reletionships between the tables of this dataset. |
| `constraints`  | `List[Constraint]` | Constraints of this dataset.                      |

## Tables

The `Table` object contains the following fields.

| **Field**        | **Type**                   | **Description**                                                                    |
|------------------|----------------------------|------------------------------------------------------------------------------------|
| `id`             | `String`                   | Unique id for the table.                                                           |
| `path`           | `String`                   | Path to the CSV file containing the table.                                         |
| `name`           | `String`                   | Name of the table.                                                                 |
| `primary_key`    | `String` or `List[String]` | Name of the column (or list of columns) that compose the primary key of the table. |
| `time_index`     | `String`                   | Name of the time index column.                                                     |
| `headers`        | `Boolean`                  | Whether the CSV file indicated by `path` contains a header row.                    |
| `number_of_rows` | `Integer`                  | Number of rows in the table.                                                       |
| `fields`         | `List[Field]`              |                                                                                    |
| `system`         | `String`                   | System to which this table belongs.                                                |
| `application`    | `String`                   | Application to which this table belongs.                                           |

Each field in the `Table` object is specified by a dictionary containing:

| **Field**      | **Type** | **Description**            |
|----------------|----------|----------------------------|
| `name`         | `String` | Name of the field.         |
| `data_type`    | `String` | Data type of the field.    |
| `data_subtype` | `String` | Data subtype of the field. |

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

The `ForeignKey` object represents a relation between two tables and contains the following fields.

| **Field**   | **Type**                   | **Description**                                                                            |
|-------------|----------------------------|--------------------------------------------------------------------------------------------|
| `table`     | `String`                   | Id of the child table.                                                                     |
| `field`     | `String` or `List[STring]` | Name of the column (or list of columns) from the child table that form this relationship.  |
| `ref_table` | `String`                   | Id of the parent table.                                                                    |
| `ref_field` | `String` or `List[STring]` | Name of the column (or list of columns) from the parent table that form this relationship. |

## Constraints

The `Constraint` object contains the following fields.

| **Field**                    | **Type**                | **Description**                                                 |
|------------------------------|-------------------------|-----------------------------------------------------------------|
| `constraint_type`            | `String`                | Type of `Constraint`.                                           |
| `fields_under_consideration` | `List[ConstraintField]` | Name of the fields of interest.                                 |
| `related_fields`             | `List[ConstraintField]` | Name of the fields that contribute to the field(s) of interest. |

### ConstraintFields

Each field in the `Contraint` object is specified by a dictionary containing:

| **Field** | **Type** | **Description**                             |
|-----------|----------|---------------------------------------------|
| `table`   | `String` | Id of the table to which the field belongs. |
| `field`   | `String` | Name of the field.                          |
