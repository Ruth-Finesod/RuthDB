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

