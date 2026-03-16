import re
import struct

from commands.base_command import BaseCommand
from exceptions import *


class Insert(BaseCommand):
    def __init__(self, db_name, data):
        super().__init__(db_name)
        self.table_name = data[0]
        self.data = data[1]

    def execute(self):
        """
        insert data into DB
        """
        self.data = re.split(r'\)\s*\(', self.data.strip("()"))
        table_columns = self.get_column_names()[0]
        if len(self.data) == 1:
            insert = [value.strip(' ').lower() for value in self.data[0].split(',')]
            if len(insert) != len(table_columns):
                raise InsertDontMatchTableError
        else:
            insert = ['None'] * len(table_columns)
            columns = [value.strip(' ').lower() for value in self.data[0].split(',')]
            values = [value.strip(' ').lower() for value in self.data[1].split(',')]
            for column, value in zip(columns, values):
                if column not in table_columns:
                    raise InsertDontMatchTableError
                insert[table_columns.index(column)] = value
        data = b''
        for value in insert:
            data += struct.pack('H', len(value))
        for value in insert:
            data += bytes(value, 'utf-8')

        with open(f'{self.db_name}/{self.table_name}.txt', 'ab') as f:
            f.write(data)
