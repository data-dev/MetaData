The meta.json file is a json object consisting of multiple parts. At the highest level of the object, there is information about the path to the dataset and a list of table objects each representing a data table in the dataset. Each table object contains information about its row and other important information. The structure of the meta.json object is described below.

## Meta Object
- **path** - a string representing the path to the dataset.
- **tables** - a list of table objects

## Table Object
- **path** - a string containing the path to the table’s csv file
- **name** - a string representing the name of the table for reference
- **primary_key** - a string containing the name of the primary key
- **time_index** -  a string containing the name of the time index, if one exists
- **secondary_time_index** - a dict mapping names of each secondary time index to columns that were known at the time specified by this field
- **headers** - boolean that is true if the table contains a header row and false otherwise.
- **number_of_rows** - integer representing the number of rows in the table
- **fields** - A list of field objects in the table
- **hard_constraints** - An object containing lists of hard constraints in the table
- **entities_to_normalize** - List of Normalize Entity Objects to use to normalize out additional tables/entities

## Field Object
- **name** - a string representing the name of the field
- **original_name** - a string representing the name of the field in the original file. This field will have its name updated to **name**
- **type** - A string representing the type of the field
- **subtype** - A string representing the subtype. Only some types have subtypes (See Types section)
- **properties** - any special properties that belong to the type. Only applies to certain types (See Types section)
- **uniques** - Integer representing the number of unique values
- **ref** - An object that represents a foreign key, a reference to another table’s primary key
Ref Object
- **table** - A string representing the name of the table that’s primary key is being referenced.
- **field** - A string representing the name of the field that is the primary key being referenced.
- **transformer** - A string representing the class name of the transformer to be used on this field during data preparation. This is an optional parameter.

## Types
The type represents, at a high level, what kind of data is represented in a field. Some types can be broken down into more specific subtypes. Below are the types with each of the subtypes that they have and any other parameters that need to be defined.

- categorical - Data that can falls under a set of different categories.
	- subtype - A string representing the subtypes
		- categorical
		- ordered - The categories can be ordered in some way, like the months of a year
		- boolean - The data can fall into two categories, true or false
- text
	- subtype - A string representing the subtypes
- digital location - any type of digital address
	- subtype - A string representing the subtypes
		- MAC address
		- URL
		- IP address
- number
	- subtype - A string representing the subtypes
		- integer
		- float
- geolocation
	- subtype  - A string representing the subtypes
		- latlong - will treat data as strings of (lat, long)
        - can supply "sep" as well to specify that lat, long are separate by something other than ", "
		- latitude
		- longitude
  - geo_name - A string specifying what the resulting (lat, long) pair column name will be
  - geo_ref - A string specifying the name of the other paired geo column (lat-> long, long->lat)
- datetime
	- properties - any special properties that belong to the type
		- format - A string representing the datetime format
- id
	- subtype - A string representing the subtypes
		- primary
	- properties - any special properties that belong to the type
		- regex - A string representing the regex that defines a valid ID. Regex or regular expressions are special text strings that describe a pattern
- other - any type that doesn’t fit the ones described above



## Sample metadata.json
```
{
    "path": "",
    "tables": [
        {
            "path": "users_demo.csv",
            "name": "users",
            "use": true,
            "headers": true,
            "time_index": "date_account_created",
            "secondary_time_index": {
                "date_first_booking": ["first_booking_name"]
            },
            "fields": [
                {
                    "name": "id",
                    "type": "id",
	             "properties": {
                        "regex": "^.{10}$"
                     },
                    "uniques": 213451
                },
                {
                    "name": "date_account_created",
                    "type": "datetime",
             "properties": {
                        "format": "%Y-%m-%d"
                     },
                    "uniques": 1634
                },
                {
                    "name": "timestamp_first_active",
                    "type": "datetime",
	             "properties": {
                        "format": "%Y%m%d%H%M%S"
                     },
                    "uniques": 213451
                },
                {
                    "name": "date_first_booking",
                    "type": "datetime",
	             "properties": {
		          "format": "%Y-%m-%d"
	             },
                    "uniques": 1977
                },
                {
                    "name": "gender",
                    "type": "categorical",
                    "subtype": "categorical",
                    "uniques": 4
                },
                {
                    "name": "age",
                    "type": "number",
                    "subtype": "integer",
                    "uniques": 128
                },
                {
                    "name": "signup_method",
                    "type": "categorical",
                    "subtype": "categorical",
                    "uniques": 3
                }
                {
                    "name": "latitude",
                    "type": "geolocation",
                    "subtype": "latitude",
                    "geo_name": "latlong1",
                    "geo_ref": "longitude",
                    "uniques": 3
                },
                {
                    "name": "longitude",
                    "type": "geolocation",
                    "subtype": "longitude",
                    "geo_name": "latlong1",
                    "geo_ref": "latitude",
                    "uniques": 3
                },
                {
                    "name": "latlong2",
                    "type": "geolocation",
                    "subtype": "latlong",
                    "uniques": 3
                },
                {
                  "name": "first_booking_name",
                  "type": "categorical"
                }
            ],
            "primary_key": "id",
            "number_of_rows": 213451
        },
        {
            "path": "sessions_demo.csv",
            "name": "sessions",
            "use": true,
            "headers": true,
            "fields": [
                {
                    "name": "user_id",
                    "type": "id",
	             "properties": {
          "regex": "^.{3,10}$"
             },
                    "ref": {
                        "table": "users",
                        "field": "id"
                    },
                    "uniques": 135484
                },
                {
                    "name": "action",
                    "type": "categorical",
                    "subtype": "categorical",
                    "uniques": 360
                }
            ],
            "number_of_rows": 10567737
        }
    ]
}
```

## *Hard Constraint Object (In progress)*
Constraints is list of inequality and equality objects.

### Inequality Object
- expression1 - Either an expression object, list of column objects or list of row objects, representing the lesser expression in the inequality
- expression2 - Either an expression object, list of column objects or list of row objects, representing the greater expression in the inequality
- type - A string representing the type of the variables being compared
sequential - For rows only. A boolean representing if the rows must come one after the other for the given groupby value

### Equality Object
- expression1 - Either a product object, sum object, list of column objects or list of row objects, representing one of the expressions in the equality
- expression2 - Either a product object, sum object, list of column objects or list of row objects, representing one of the expressions in the equality
- type - A string representing the type of the variables being compared

### Column Object
- field - A string representing the name of the field
- table - A string representing the name of the table

### Row Object
- groupby - A list of column names to group the rows by
key - A string representing the column name that the condition is based on. For example, ‘action’ might be the column name that could have values ‘add to cart’ and ‘checkout’ and we want to compare the times of these two rows.
- value - A string representing the value of the key
- comparate - A string representing the column name to compare

### Expression Object
Expression objects must have either a list of columns or rows, but not both. If the list has more than one item, than either the product or sum variable must be true.

- columns - A list of column objects in the expression
- rows - A list of row objects in the expression
- product - A boolean denoting if the row objects or column objects should be multiplied
- sum - A boolean representing if the rows or columns should be added

### Normalize Entity Object
  - **base_entity_id** - Base entity id to normalize from
  - **new_entity_id** - new entity id to create
  - **index** - column to use as the new entity index
  - **additional_variables** - additional columns to pull out of base entity
  - **copy_variables** - additional columns to copy from base entity
  - **make_time_index** - make a time index in the new entity
  - **time_index_reduce** - either "first" or "last", to use the first or last time from duplicate entries in base entity
  - **new_entity_time_index** - name to use as new entity time index
  - **convert_links_to_integers** - create a new column with integers to use as the relationship between the two entities
