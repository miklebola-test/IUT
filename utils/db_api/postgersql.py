import asyncpg
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self, pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(
            user=config.PGUSER,
            password=config.PGPASSWORD,
            host=config.ip
        )
        return cls(pool)

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users:
        id INT NOT NULL,
        Name VARCHAR(255) NOT NULL,
        PRIMARY KEY(id))
        """
        await self.pool.execute(sql)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, id: int, name: str):
        sql = "INSERT INTO Users (id, name) VALUES ($1, $2, $3)"
        await self.pool.execute(sql, id, name)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.pool.fetch(sql)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE"
        sql, parameters = self.format_args(sql, kwargs)
        return await self.pool.fetchrow(self, *parameters)

    async def count_users(self):
        return await self.pool.fetchval("SELECT(*) FROM Users")

    async def delete_users(self):
        await self.pool.execute("DELETE FROM Users WHERE True")
