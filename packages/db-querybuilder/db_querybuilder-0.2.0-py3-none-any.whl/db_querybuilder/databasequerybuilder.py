import datetime
import json
import sqlite3
from enum import Enum
import typing

from mysql.connector import CMySQLConnection, Error, MySQLConnection, connect


# The above class is an enumeration of database drivers
class DatabaseDrivers(Enum):
    DRIVER_MYSQL = 'MYSQL'
    DRIVER_SQLITE = 'SQLITE'


# It's a class that generates SQL queries for you
class DatabaseQueryBuilder():
    def __init__(self,db_database: str, driver: str | DatabaseDrivers = 'MYSQL') -> None:
        """
        This function is used to connect to a database
        
        :param db_database: str = The name of the database you want to connect to
        :type db_database: str
        :param driver: str | DatabaseDrivers = 'MYSQL', defaults to MYSQL
        :type driver: str | DatabaseDrivers (optional)
        """
        super().__init__()

        self.table = ''
        self._query = ''
        self.db_database = db_database
        self.host = 'localhost'
        self.user = None
        self.password = None
        self.port = None
        self.__cursor = None
        self.db: MySQLConnection | CMySQLConnection | sqlite3.Connection = None
        self.__driver = driver

        try:
            if DatabaseDrivers.DRIVER_MYSQL.value == driver:
                self.db = connect(host=self.host, user=self.user, password=self.password, database=self.db_database, port=self.port)
                self.db.autocommit = False
                self.__cursor = self.db.cursor()
            else:
                self.db = sqlite3.connect(f'{self.db_database}.sqlite')
                self.__cursor = self.db.cursor()
        except Error as e:
            print(e)

    
    def setHost(self, host: str):
        """
        This function sets the host of the object to the host passed in as a parameter
        
        :param host: The hostname of the server
        :type host: str
        """
        self.host = host

        return self

    
    def setUserAndPassword(self, user: str, password: str):
        """
        This function sets the user and password of the object
        
        :param user: The username of the account you want to use to execute database
        :type user: str
        :param password: The password for database
        :type password: str
        """
        self.user = user
        self.password = password

        return self

    
    def setPort(self, port: int):
        """
        This function sets the port number of the server
        
        :param port: The port to listen on
        :type port: int
        """
        self.port = port

        return self

    def getLastId(self):
        return self.__cursor.lastrowid

    def getRowsCount(self):
        return self.__cursor.rowcount

    
    def reset(self):
        """It resets the table and queryResult to empty strings.

        :return: The object itself.
        """
        self.table = ''
        self._query = ''

        return self

    
    def setTable(self, name: str):
        """It sets the table name for the query

        :param name: The name of the table you want to query
        :type name: str
        :return: The object itself.
        """
        self.table = name
        return self

    
    def createTable(self,table: str | None = None, *, columns: list = [], override: bool = False):
        """
        It creates a table in the database with the columns specified in the parameters
        
        :param table: str | None = None, *, columns: list = [], override: bool = False
        :type table: str | None
        :param columns: list = []
        :type columns: list
        :param override: bool = False, defaults to False
        :type override: bool (optional)
        :return: The return value is the instance of the class.
        """
        try: 
            if not columns:
                print('Not found columns in parameters')

            if not table:
                if not self.table:
                    print('No table created')
                    return
                
                table = self.table

            columns.insert(0,'(')
            columns.insert(len(columns),')')
            format = ''
            
            for index, col in enumerate(columns):
                if not index == len(columns) - 2:
                    if col == '(':
                        format += col
                    elif col == ')':
                        format += col
                    else:
                        format += f'{col}, '
                else:
                    format += f'{col}'

            if override:
                self.__cursor.execute(f'DROP TABLE IF EXISTS {table};')
                self._query = f'CREATE TABLE {table} {format};'
            else:
                self._query = f'CREATE TABLE IF NOT EXISTS {table} {format}'
            self.__cursor.execute(self._query)

            return self
        except Exception as e:
            print(e)

    
    def query(self):
        """It returns the query result of the table that was passed in
        :return: The queryResult attribute of the class.
        """
        self._query = f'select * from {self.table}'
        return self


    def select(self, table: str | None = None, *, fields: list = []):
        """
        It takes a table name and a list of fields and returns a query string
        
        :param table: The table name
        :type table: str
        :param fields: list = []
        :type fields: list
        :return: The select method is returning the object itself.
        """
        if not table:
            if not self.table:
                print('No table created')
                return
            
            table = self.table


        if not fields:
            self._query = f'select * from {table}'
            return self
        
        self._query = 'select '
        for index, field in enumerate(fields):
            if not index == len(fields) - 1:
                self._query += f'{field}, '
            else:
                self._query += f'{field} '
        self._query += f'from {table}'

        return self
        
    def from_(self, table: str):
        """It takes a string as an argument and appends it to the queryResult property of the class

        :param table: str
        :type table: str
        :return: The object itself.
        """
        self._query += f'{table}'
        return self

    
    def where(self, clausule: str, parameter: str, parameters_dict: dict = {},*, operator: str = '='):
        """It takes a clausule, a parameter, a parameters_dict and an operator as arguments and returns the queryResult with the where clausule

        Note: In the parameters dictionary it's necessary write the operator in the condition e.g: parameters_dict: {'id =': 1, 'name =': 'John'}

        :param clausule: The column name
        :type clausule: str
        :param parameter: str
        :type parameter: str
        :param parameters_dict: {'id =': 1, 'name =': 'John'}
        :type parameters_dict: dict
        :param operator: The operator to be used in the where clause, defaults to =
        :type operator: str (optional)
        :return: The queryResult string
        """
        try:
            if clausule and parameter:
                if self._query.find('where') == -1:
                    if type(parameter) == str:
                        parameter = f'\'{parameter}\''
                    self._query += f' where {clausule} {operator} {parameter}'
                else:
                    if type(parameter) == str:
                        parameter = f'\'{parameter}\''
                    self._query += f' and {clausule} {operator} {parameter}'
            else:
                self._query += ' where '
                if (len(parameters_dict) == 1):
                    params = list(parameters_dict.items())
                    condition = params[0][0]
                    value = params[0][1]
                    if type(value) == str:
                        value = f'\'{value}\''
                    self._query += f' {condition} {value}'
                else:
                    for index, (condition, value) in enumerate(parameters_dict.items()):
                        if not index == len(parameters_dict) - 1:
                            if type(value) == str:
                                value = f'\'{value}\''
                                self._query += f' {condition} {value} and '
                        else:
                            if type(value) == str:
                                value = f'\'{value}\''
                                self._query += f' {condition} {value} '
            return self
        except Exception as e:
            print(e)


    def results(self, query: str = '') -> list[tuple]:
        """It takes a query as an argument, and if the query is empty, it executes the queryResult
        variable, which is a string, and if the query is not empty, it executes the query

        :param query: str = ''
        :type query: str
        :return: A list of tuples.
        """
        try:
            if not query:
                self.__cursor.execute(self._query)
            else:
                self.__cursor.execute(query)

            self.db.commit()
            return self.__cursor.fetchall()
        except Error as e:
            self.db.rollback()
            print(e)

    
    def toJson(self) -> str:
        """It takes the results of a query and returns a json string
        :return: A list of dictionaries.
        """
        try:
            fields: list[tuple] | list = None
            listFields = []
            toJson = []
            dictionary = {}

            if DatabaseDrivers.DRIVER_MYSQL.value == self.__driver:
            
                query_fields = f'SELECT COLUMN_NAME \'field\' FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = \'{self.db_database}\' AND TABLE_NAME = \'{self.table}\';'

                self.__cursor.execute(query_fields)
                fields = self.__cursor.fetchall()
                self.db.commit()
                query = self.results()
            
            elif DatabaseDrivers.DRIVER_SQLITE.value == self.__driver:
                query_fields = f'select * from {self.table}'

                self.__cursor.execute(query_fields)
                fields = list(map(lambda columns: columns[0], self.__cursor.description))
                self.db.commit()
                query = self.results()


            for field in fields:
                if DatabaseDrivers.DRIVER_MYSQL.value == self.__driver:
                    # Get the first position of tuple => 'id','name',
                    newField: str = field[0]
                else:
                    newField: str = field
                listFields.append(newField)

            for index, qResult in enumerate(query):
                dictionary = {}
                for index, qry in enumerate(qResult):
                    dictionary[listFields[index]] = str(
                        qry) if isinstance(qry, datetime.datetime) else qry
                toJson.append(dictionary)

            # It is used to encode the json strings to utf8
            toJson = json.dumps(toJson, ensure_ascii=False)

            return toJson
        except Error as e:
            self.db.rollback()
            print(e)

    
    def insert(self,table: str | None = None, *, fields: list = [], values: list = [], object: object = object):
        """It takes a table name, a list of fields, a list of values, and an object as parameters,and inserts the values into the table

        :param table: The table name
        :type table: str
        :param fields: list = [], values: list = [], object: object = object
        :type fields: list
        :param values: list = [], object: object = object
        :type values: list
        :param object: object = object
        :type object: object
        :return: The last row id
        """
        try:
            if not table:
                if not self.table:
                    print('No table created')
                    return
                
                table = self.table

            if table and fields and values:
                query = self.__generateInsert(table, fields, values)
            elif fields and values:
                query = self.__generateInsert(self.table, fields, values)
            elif object and table:
                for o in [attr for attr in dir(object) if not attr.startswith('__') and not callable(getattr(object, attr))]:
                    if o != 'id':
                        fields.append(o)
                        values.append(getattr(object, o))
                query = self.__generateInsert(table, fields, values)

            self.__cursor.execute(query)
            self.db.commit()


            return self.__cursor.lastrowid

        except Exception as e:
            self.db.rollback()
            print(e)

    
    def insertMany(self, table: str | None = None, *, fields: list = [], values: list = []):
        """It takes a table name, a list of fields, and a list of values, and inserts them into the database

        :param table: str = ''
        :type table: str
        :param fields: list = ('id', 'name', 'age')
        :type fields: list
        :param values: list = ()
        :type values: list
        :return: The last row id
        """
        try:
            if not table:
                if not self.table:
                    print('No table created')
                    return
                
                table = self.table

            if table and fields and values:
                query = self.__generateInsertMany(table, fields, values)
            else:
                query = self.__generateInsertMany(self.table, fields, values)
            self.__cursor.execute(query)
            self.db.commit()

            return self.__cursor.lastrowid

        except Exception as e:
            self.db.rollback()
            print(e)

    
    def update(self, table: str | None = None, *, fields: list = [], values: list = [], object: object = object, clausule: str, parameter: str, parameters_dict: dict = {}) -> int:
        """It generates an update query based on the parameters passed to it

        :param table: str = ''
        :type table: str
        :param fields: list = [], values: list = [], object: object = object, clausule: str, parameter: str, parameters_dict: dict = {}
        :type fields: list
        :param values: list = []
        :type values: list
        :param object: object = object
        :type object: object
        :param clausule: The condition to be met for the update to be executed
        :type clausule: str
        :param parameter: str = 'id'
        :type parameter: str
        :param parameters_dict: {'id': 1}
        :type parameters_dict: dict
        :return: The number of rows affected by the update.
        """
        try:
            if not table:
                if not self.table:
                    print('No table created')
                    return
                
                table = self.table

            if table and fields and values:
                query = self.__generateUpdate(table, fields, values)
            elif fields and values:
                query = self.__generateUpdate(self.table, fields, values)
            elif object and table:
                for o in [attr for attr in dir(object) if not attr.startswith('__') and not callable(getattr(object, attr))]:
                    if o != 'id':
                        fields.append(o)
                        values.append(getattr(object, o))
                query = self.__generateUpdate(table, fields, values)

            # Add where for update data in the db.
            self.reset().setTable(table if table else self.table).where(
                clausule, parameter, parameters_dict)

            query += self._query

            self.__cursor.execute(query)
            self.db.commit()

            return self.__cursor.rowcount
        except Error as e:
            self.db.rollback()
            print(e)

    
    def delete(self, table: str | None = None, *, clausule: str = '', parameter: str = ''):
        """It deletes a row from a table

        :param table: The table you want to delete from
        :type table: str
        :param clausule: The condition for the deletion
        :type clausule: str
        :param parameter: str = ''
        :type parameter: str
        :return: The number of rows affected by the query.
        """
        try:
            if table:
                self._query = f'delete from {table}'
            else:
                self._query = f'delete from {self.table}'

            self.where(clausule, parameter, {})

            self.__cursor.execute(self._query)
            self.db.commit()

            return self.__cursor.rowcount
        except Error as e:
            self.db.rollback()
            print(e)

    def __generateInsert(self, table: str, fields: list, values: list) -> str:
        """It takes a table name, a list of fields, and a list of values and returns a string that is a valid SQL insert statement

        :param table: the table name
        :param fields: list of fields to insert into
        :type fields: list
        :param values: list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
        '14', '15', '16', '17', '18', '19', '
        :type values: list
        :return: A string
        """
        try:
            insert = f'insert into {table} ('

            for index, field in enumerate(fields):
                if not index == len(fields) - 1:
                    insert += '{},'.format(field)
                else:
                    insert += '{}'.format(field)

            insert += ') values ('

            for index, value in enumerate(values):
                if not index == len(values) - 1:
                    if type(value) == str:
                        value = f'\'{value}\''
                        insert += '{},'.format(value)
                    else:
                        insert += '{},'.format(value)
                else:
                    if type(value) == str:
                        value = f'\'{value}\''
                        insert += '{}'.format(value)
                    else:
                        insert += '{}'.format(value)
            insert += ');'

            return insert
        except Exception as e:
            print(e)

    def __generateInsertMany(self, table: str, fields: list, values: list) -> str:
        """It takes a table name, a list of fields, and a list of values and returns a string that is a valid SQL insert statement

        :param table: the table name
        :param fields: list of fields to insert into
        :type fields: list
        :param values: list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
        '14', '15', '16', '17', '18', '19', '
        :type values: list
        :return: A string
        """
        try:
            insert = f' insert into {table} ('

            for index, field in enumerate(fields):
                if not index == len(fields) - 1:
                    insert += '{},'.format(field)
                else:
                    insert += '{}'.format(field)
                    insert += ') values '

            for index, value in enumerate(values):
                if not index == len(values) - 1:
                    if type(value) == str:
                        value = f'\'{value}\''
                        insert += '({}),'.format(value)
                    else:
                        insert += '({}),'.format(value)
                else:
                    if type(value) == str:
                        value = f'\'{value}\''
                        insert += '({})'.format(value)
                    else:
                        insert += '({})'.format(value)

            return insert
        except Exception as e:
            print(e)

    def __generateUpdate(self, table: str, fields: list, values: list) -> str:
        """It takes a table name, a list of fields, and a list of values, and returns an update statement

        :param table: The table name
        :param fields: ['id', 'name', 'age']
        :param values: a list of tuples, each tuple is a row of data
        :return: The update statement
        """
        try:
            update = f'update {table} set '

            if len(fields) == 1 and len(values) == 1:
                if type(values[0]) == str:
                    values[0] = f'\'{values[0]}\''
                    update += '{} = {}'.format(fields[0], values[0])
                else:
                    update += '{} = {}'.format(fields[0], values[0])
            else:
                for value in values:
                    for index, valueData in enumerate(value):
                        if not index == len(fields) - 1:
                            if type(valueData) == str:
                                valueData = f'\'{valueData}\''
                                update += '{} = {}, '.format(
                                    fields[index], valueData)
                            else:
                                update += '{} = {}, '.format(
                                    fields[index], valueData)
                        else:
                            if type(valueData) == str:
                                valueData = f'\'{valueData}\''
                                update += '{} = {}'.format(
                                    fields[index], valueData)
                            else:
                                update += '{} = {}'.format(
                                    fields[index], valueData)
            return update
        except Exception as e:
            print(e)
