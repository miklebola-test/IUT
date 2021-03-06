import sqlite3


class Database1:
    def __init__(self, path_to_dp="data/main1.dp"):
        self.path_to_dp = path_to_dp

    @property
    def coonection(self):
        return sqlite3.connect(self.path_to_dp)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False,
                fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.coonection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()

        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
        id varchar NOT NULL,
        Name varchar NOT NULL,
        PRIMARY KEY (id)
        );

        """
        self.execute(sql, commit=True)

    def add_user(self, id: str, name: str):
        sql = "INSERT INTO Users(id, Name) Values(?, ?)"
        parameters = (id, name)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_users(self):
        sql = "SELECT * FROM Users"
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def select_user(self, **kwargs):

        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE Users WHERE True")


def logger(statement):
    print(f"""
--------------------------------------------------------------
Executing:
{statement}


--------------------------------------------------------------
""")
