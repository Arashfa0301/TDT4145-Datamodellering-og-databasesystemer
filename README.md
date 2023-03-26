# DB2: Train database implementaiton in python

## Prerequisite

In order to use the program you'll need to use `pip install PrettyTable` before running, as that is what is used for printing.
See source here: https://pypi.org/project/prettytable/

The main program is located in `program.py` and requires a `trainstatonDB.db`-file. To create this file you can run `cleanDatabase.py`, which will create the database with the correct tabels and populate it with some example data.

## Usage

When running program.py you'll be prompted with two options, _login_ or _register_. We have made an example user with the following credentials:

```
+------+---------------+----------------------------------+------------------+
| Name |     Email     |             Address              | Telephone Number |
+------+---------------+----------------------------------+------------------+
| Per  | per@gmail.com | Høgskoleringen 1, 7034 Trondheim |     88888888     |
+------+---------------+----------------------------------+------------------+
```

After you've successfully logged inn you'll be presented with the following options:

```
 - Type 1 to list all the avaiable train routes at a given weekday and train station

 - Type 2 to list all the available train routes that pass through given start and end stations at a given day and time

 - Type 3 to list all your tickets

 - Type 9 to see user information
```
