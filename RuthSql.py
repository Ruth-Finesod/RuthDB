import os
import re

from commands.create import Create
from commands.insert import Insert
from commands.select import Select
from exceptions import *


class RuthSql:
    STATEMENTS = {'select': [re.compile(r'^\s*select\s+\*\s+from\s+(\w+)\s*$', re.IGNORECASE), Select],
                  'create': [re.compile(r'^\s*create\s+table\s+(\w+)\s*\(([\w\s,]+)\)\s*$', re.IGNORECASE), Create],
                  'insert': [re.compile(r'^insert\s+into\s+(\w+)\s*((?:\([\w\s,]+\)\s*){1,2}\s*$)', re.IGNORECASE),
                             Insert],
                  }

    def __init__(self, db_name: str):
        self.db_name = self.valid_db(db_name)

    @staticmethod
    def valid_db(db_name: str) -> str:
        """
        validate that db exists, by looking for dir with db_name name
        :param db_name: the name of the database
        """
        if os.path.isdir(db_name):
            return db_name
        else:
            raise NoSuchDBError(db_name)

    def execute(self, query: str):
        """
        match query to SQL query and execute it if match
        :param query: SQL query
        :return: the return from the function that was executed
        """
        for statement_name, regex in self.STATEMENTS.items():
            if regex[0].findall(query):
                return self.STATEMENTS[statement_name][1](self.db_name, regex[0].findall(query)[0]).execute()
        raise NoSuchStatementError
