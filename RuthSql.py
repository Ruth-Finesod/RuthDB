import os
import re
import struct
from glob import glob


class NoSuchDBError(Exception):
    pass


class TableAlreadyExistsError(Exception):
    pass


class NoSuchTableError(Exception):
    pass


class NoSuchStatementError(Exception):
    pass


class InsertDontMatchTableError(Exception):
    pass


class RuthSql:
    STATEMENTS = {'select': re.compile(r'^\s*select\s+\*\s+from\s+(\w+)\s*$', re.IGNORECASE),
                  'create': re.compile(r'^\s*create\s+table\s+(\w+)\s*\(([\w\s,]+)\)\s*$', re.IGNORECASE),
                  'insert': re.compile(r'^insert\s+into\s+(\w+)\s*((?:\([\w\s,]+\)\s*){1,2}\s*$)', re.IGNORECASE),
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
        match query to sql query and execute it if match
        :param query: sql query
        :return: the return from the function that was executed
        """
        flag = False
        for statement_name, regex in self.STATEMENTS.items():
            if regex.findall(query):
                flag = True
                return getattr(self, statement_name)(regex.findall(query)[0])
        if not flag:
            raise NoSuchStatementError

    def select(self, table_name: str) -> list[list[str]]:
        """
        select from th DB the data of the table
        :param table_name: table name
        :return: list of the rows as list, first one is the columns names
        """
        try:
            with open(f'{self.db_name}/{table_name}.txt', 'rb') as f:
                data = f.read()
        except FileNotFoundError:
            raise NoSuchTableError(table_name)

        select_ls = []
        columns = data.split(b')')[0]
        data = data[len(columns) + 1:]
        columns = [value.decode('utf-8').strip(' ').lower() for value in columns.split(b',')]
        select_ls.append(columns)

        while data:
            lengths = struct.unpack('H' * len(columns), data[:len(columns) * 2])
            data = data[len(columns) * 2:]
            values = data[:sum(lengths)].decode('utf-8')
            data = data[sum(lengths):]
            ls_values = []
            i = 0
            for l in lengths:
                ls_values.append(values[i: l + i])
                i += l
            select_ls.append(ls_values)
        return select_ls

    def insert(self, data: tuple[str, str]):
        """
        insert data into DB
        :param data: the table name and the values to insert, can get also the columns
        """
        table_name, data = data
        data = data.strip("()")
        data = re.split(r'\)\s*\(', data)

        try:
            with open(f'{self.db_name}/{table_name}.txt', 'r') as f:
                table_columns = [value.strip(' ').lower() for value in f.read().split(')')[0].split(',')]
        except FileNotFoundError:
            raise NoSuchTableError(table_name)

        if len(data) == 1:
            insert = [value.strip(' ').lower() for value in data[0].split(',')]
            if len(insert) != len(table_columns):
                raise InsertDontMatchTableError
        else:
            insert = ['None'] * len(table_columns)
            columns = [value.strip(' ').lower() for value in data[0].split(',')]
            values = [value.strip(' ').lower() for value in data[1].split(',')]
            for column, value in zip(columns, values):
                if column not in table_columns:
                    raise InsertDontMatchTableError
                insert[table_columns.index(column)] = value

        data = b''
        for value in insert:
            data += struct.pack('H', len(value))
        for value in insert:
            data += bytes(value, 'utf-8')

        with open(f'{self.db_name}/{table_name}.txt', 'ab') as f:
            f.write(data)

    def create(self, data: tuple[str, str]):
        """
        create table in DB, by creating txt file with columns names
        :param data: the table name and the columns names
        """
        table_name, columns = data
        if table_name + '.txt' in [os.path.basename(f) for f in glob(f'{self.db_name}/*')]:
            raise TableAlreadyExistsError(table_name)
        with open(f'{self.db_name}/{table_name}.txt', 'w') as f:
            f.write(f'{columns})')


def main():
    db = RuthSql('ruthdb.db')


if __name__ == '__main__':
    main()
