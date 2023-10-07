from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def create_table_finance(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Products (
        id SERIAL PRIMARY KEY,        
        category_name VARCHAR(50) NULL,              
        productname VARCHAR(50) NULL,        
        price INT NOT NULL,        
        item INT NULL,
        summary INT NULL,
        date DATE NOT NULL DEFAULT CURRENT_DATE
        );
        """
        await self.execute(sql, execute=True)

    async def add_all(self, category_name, productname, price, item, summary):
        sql = ("INSERT INTO "
               "Products (category_name, productname, price, item, summary)"
               "VALUES($1, $2, $3, $4, $5) returning *")
        return await self.execute(sql, category_name, productname, price, item, summary,
                                  fetchrow=True)

    async def add_date(self, category_name, productname, price, item, summary, date):
        sql = ("INSERT INTO "
               "Products (category_name, productname, price, item, summary, date)"
               "VALUES($1, $2, $3, $4, $5, $6) returning *")
        return await self.execute(sql, category_name, productname, price, item, summary, date,
                                  fetchrow=True)

    # async def update_summary(self, productname):
    #     sql = "UPDATE Products SET summary = price * item;"
    #     return await self.execute(sql, productname, execute=True)

    # async def select_user_products(self, user_id):
    #     sql = "SELECT * FROM Products WHERE user_id=$1"
    #     return await self.execute(sql, user_id, fetch=True)

    async def get_categories(self):
        sql = "SELECT DISTINCT category_name FROM Products"
        return await self.execute(sql, fetch=True)

    async def get_subcategories(self, category_name):
        sql = f"SELECT DISTINCT date FROM Products WHERE category_name='{category_name}'"
        return await self.execute(sql, fetch=True)

    async def get_products(self, category_name, date):
        sql = f"SELECT * FROM Products WHERE category_name='{category_name}' AND date='{date}'"
        return await self.execute(sql, fetch=True)

    async def get_product(self, product_id):
        sql = f"SELECT * FROM Products WHERE id={product_id}"
        return await self.execute(sql, fetchrow=True)

    async def delete_products(self, product_id):
        await self.execute("DELETE FROM Products WHERE id=$1", product_id, execute=True)


    async def drop_products(self):
        await self.execute("DROP TABLE Products", execute=True)
