import MySQLdb
import pandas as pd
from typing import List, Tuple
from .configuration import MySqlConfiguration
from .exceptions import (
    DatabaseConnectionError, DatabaseInsertionError,
    DatabaseQueryError
)


class MySqlClient:

    def __init__(self, configuration: MySqlConfiguration):
        if (isinstance(configuration, MySqlConfiguration)):
            self._configuration = configuration
        else:
            raise TypeError('Invalid MySQL configuration.')

        self._connection = None

    def connect(self):
        try:
            self._connection = MySQLdb.connect(
                host=self._configuration.address,
                user=self._configuration.user,
                passwd=self._configuration.password,
                db=self._configuration.database
            )
        except MySQLdb.Error as error:
            raise DatabaseConnectionError('Could not connect to database') from error

    def close(self):
        try:
            self._connection.commit()
            self._connection.cursor.close()
            self._connection.close()
            self._connection = None
        except:
            pass
    
    def insert(self, query: str, data: tuple) -> None:
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, data)
        except MySQLdb.Error as error:
            raise DatabaseInsertionError(
                'An error occured while inserting data.'
            ) from error

    def insert_multiple(self, query: str, data: List[Tuple]) -> None:
        try:
            cursor = self._connection.cursor()
            cursor.executemany(query, data)
        except MySQLdb.Error as error:
            raise DatabaseInsertionError(
                'An error occured while inserting multiple rows.'
            ) from error

    def get_dataframe(self, query: str, index_column: str) -> pd.DataFrame:
        try:
            df = pd.read_sql(query, self._connection, index_col=[index_column])
        except Exception as error:
            raise DatabaseQueryError(
                'An error occured while querying data using pandas lib.'
            ) from error
        else:
            return df
