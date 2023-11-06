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

    # ============================ INCOMING TABLE ============================
    async def create_table_incoming(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Incoming (
        id SERIAL,
        user_id BIGINT NOT NULL,
        incoming_name VARCHAR(100) NOT NULL,
        summary INT NULL,
        history VARCHAR(4000) NULL DEFAULT '',
        date TIMESTAMP(0) NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        await self.execute(sql, execute=True)

    async def add_incoming(self, user_id, incoming_name, summary):
        sql = """INSERT INTO Incoming (user_id, incoming_name, summary) VALUES($1, $2, $3) returning*"""
        return await self.execute(sql, user_id, incoming_name, summary, fetchrow=True)

    async def get_userall_inc(self, user_id, distinct=False):
        if distinct:
            sql = """SELECT DISTINCT incoming_name FROM Incoming WHERE user_id=$1"""
            return await self.execute(sql, user_id, fetch=True)
        else:
            sql = """SELECT * FROM Incoming WHERE user_id=$1"""
            return await self.execute(sql, user_id, fetch=True)

    async def get_user_inc(self, user_id, incoming_name=None, history=False):
        if history:
            sql = """SELECT history FROM Incoming WHERE user_id=$1 """
            return await self.execute(sql, user_id, fetchrow=True)
        else:
            sql = """SELECT incoming_name, summary, date FROM Incoming WHERE user_id=$1 AND incoming_name=$2"""
            return await self.execute(sql, user_id, incoming_name, fetch=True)

    async def update_inc_name_and_summary(self, incoming_name, summary, user_id):
        sql = f"UPDATE Incoming SET incoming_name='{incoming_name}', summary='{summary}' WHERE user_id='{user_id}'"
        return await self.execute(sql, execute=True)

    async def update_inc_history(self, user_id, history):
        sql = f"UPDATE Incoming SET history=history||'{history}' WHERE user_id='{user_id}'"
        return await self.execute(sql, execute=True)

    async def summary_category_inc(self, user_id, incoming_name):
        sql = f"SELECT SUM(summary) FROM Incoming WHERE user_id=$1 AND incoming_name=$2"
        return await self.execute(sql, user_id, incoming_name, fetchval=True)

    async def summary_all_inc(self, user_id):
        sql = f"SELECT SUM(summary) FROM Incoming WHERE user_id=$1"
        return await self.execute(sql, user_id, fetchval=True)

    async def clear_history_inc(self, user_id):
        sql = f"UPDATE Incoming SET history='' WHERE user_id='{user_id}'"
        return await self.execute(sql, execute=True)

    async def delete_row_inc(self, user_id, incoming_name):
        await self.execute("DELETE FROM Incoming WHERE user_id=$1 AND incoming_name=$2",
                           user_id, incoming_name, execute=True)

    async def drop_table_inc(self):
        await self.execute("DROP TABLE Incoming", execute=True)

    # ============================ OUTGOING TABLE ============================
    async def create_table_outgoing(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Outgoing (
        id SERIAL,
        user_id BIGINT NULL,        
        category_name VARCHAR(50) NULL,
        subcategory_name VARCHAR(50) NULL,             
        summary INT NULL,
        date TIMESTAMP(0) NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        await self.execute(sql, execute=True)

    async def first_add_out(self, category_name, subcategory_name, user_id, summary):
        sql = ("INSERT INTO Outgoing (category_name, subcategory_name, user_id, summary) "
               "VALUES ($1, $2, $3, $4) returning *")
        return await self.execute(sql, category_name, subcategory_name, user_id, summary, fetchrow=True)

    # ==================== SUMMARY ====================
    async def get_sum_all_out(self, user_id):
        sql = f"SELECT SUM(summary) FROM Outgoing WHERE user_id=$1"
        return await self.execute(sql, user_id, fetchval=True)

    async def get_sum_category(self, user_id, category_name):
        sql = f"SELECT SUM(summary) FROM Outgoing WHERE user_id=$1 AND category_name=$2"
        return await self.execute(sql, user_id, category_name, fetchval=True)

    async def get_sum_subcategory(self, user_id, subcategory_name):
        sql = f"SELECT SUM(summary) FROM Outgoing WHERE user_id=$1 AND subcategory_name=$2"
        return await self.execute(sql, user_id, subcategory_name, fetchval=True)

    async def update_productsum_out(self, summary, product_id, user_id):
        sql = f"UPDATE Outgoing SET summary ='{summary}' WHERE id='{product_id}' AND user_id='{user_id}'"
        return await self.execute(sql, execute=True)

    async def update_categoryname_out(self, new_category, old_category, user_id):
        sql = (f"UPDATE Outgoing SET category_name='{new_category}' WHERE category_name='{old_category}' AND "
               f"user_id='{user_id}'")
        return await self.execute(sql, execute=True)

    async def update_subcategoryname_out(self, user_id, old_subcategory, new_subcategory):
        sql = f"""UPDATE Outgoing SET subcategory_name='{new_subcategory}' WHERE subcategory_name='{old_subcategory}' 
        AND user_id='{user_id}'"""
        return await self.execute(sql, execute=True)

    async def update_productname_out(self, new_product, old_product_id, user_id):
        sql = f"UPDATE Outgoing SET productname='{new_product}' WHERE id='{old_product_id}' AND user_id='{user_id}'"
        return await self.execute(sql, execute=True)

    async def get_categories_out(self, user_id, all_data=False):
        if all_data:
            sql = f"SELECT * FROM Outgoing WHERE user_id='{user_id}'"
        else:
            sql = f"SELECT DISTINCT category_name FROM Outgoing WHERE user_id='{user_id}'"
        return await self.execute(sql, fetch=True)

    async def get_subsummary_out(self, category_name, user_id):
        sql = f"SELECT summary FROM Outgoing WHERE category_name='{category_name}' AND user_id='{user_id}'"
        return await self.execute(sql, fetch=True)

    async def get_subdistinct_out(self, category_name, user_id):
        sql = (f"SELECT DISTINCT subcategory_name FROM Outgoing WHERE category_name='{category_name}' AND "
               f"user_id='{user_id}'")
        return await self.execute(sql, fetch=True)

    async def get_subdistinct_(self, category_name, user_id):
        sql = (f"SELECT DISTINCT ON (subcategory_name) subcategory_name, summary FROM Outgoing "
               f"WHERE category_name='{category_name}' AND user_id='{user_id}'")
        return await self.execute(sql, fetch=True)

    async def get_products_out(self, subcategory_name, user_id):
        sql = f"SELECT id FROM Outgoing WHERE subcategory_name='{subcategory_name}' AND user_id='{user_id}'"
        return await self.execute(sql, fetchrow=True)

    async def get_product_out(self, product_id):
        sql = f"SELECT category_name, subcategory_name, summary FROM Outgoing WHERE id={product_id}"
        return await self.execute(sql, fetchrow=True)

    # ================================SELECT DATE================================================================
    async def getdate_subcategory_out(self, user_id, subcategory_name):
        sql = f"SELECT date, summary FROM Outgoing WHERE user_id='{user_id}' AND subcategory_name='{subcategory_name}'"
        return await self.execute(sql, fetch=True)

    async def getdate_category_out(self, user_id, category_name):
        psql = (f"SELECT DISTINCT subcategory_name FROM Outgoing "
                f"WHERE category_name='{category_name}' AND user_id='{user_id}'")
        return await self.execute(psql, fetch=True)

    async def delete_subcategory_out(self, subcategory, user_id):
        await self.execute("DELETE FROM Outgoing WHERE subcategory_name=$1 AND user_id=$2",
                           subcategory, user_id, execute=True)

    async def delete_product_out(self, product_id):
        await self.execute("DELETE FROM Outgoing WHERE id=$1", product_id, execute=True)

    async def drop_table_out(self):
        await self.execute("DROP TABLE Outgoing", execute=True)
