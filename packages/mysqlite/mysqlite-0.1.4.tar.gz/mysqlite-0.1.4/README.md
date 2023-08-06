# MYSQLITE
___
# About

This library was created to simplify the handling of .db, .sqlite, .sqlite3 files
in small python projects.
For example, if you want to write something quickly without bothering with SQL queries.

This project is still "raw", but I will gradually refine it.
___
# Start
Connecting an existing one or creating a new database file
`db = mysqlite.Database('database_filename.db')`

___
# Create table
Create a new table and fields
```
db.create_table(table_name='table_name', data_fields={
    'field1': 'TEXT',
    'field2': 'INTEGER',
    'field3': 'NULL'
})
```
Database:
| field1 | field2 | field3 |
| -------|--------|--------|

___
# Add new field
`db.add_field(table_name='table_name', field_name='field4', field_type='NULL')`
Database:
| field1 | field2 | field3 | field4 |
| -------|--------|--------|--------|

___
# Add data - insert
```
db.insert('table_name',
          ('field1', 'field2'),
          ('Tom',    '12'),
          ('Jake',   '15'))
```
Database:
| field1 | field2 | field3 | field4 |
| -------|--------|--------|--------|
| Tom    | 12     | NULL   | NULL   |
| jake   | 15     | NULL   | NULL   |

___
# Delete field
`db.delete_field('table_name', field_name='field4')`
Database:
| field1 | field2 | field3 |
| -------|--------|--------|
| Tom    | 12     | NULL   |
| jake   | 15     | NULL   |

___
# Delete where
`db.delete_where('table_name', delete_condition="field2=12")`
Database:
| field1 | field2 | field3 |
| -------|--------|--------|
| jake   | 15     | NULL   |

___
# Get fields
`print(db.get_fields('table_name'))`
Output:
> [(0, 'field1', 'TEXT', 0, None, 0), (1, 'field2', 'INT', 0, None, 0), (2, 'field3', '', 0, None, 0)]

