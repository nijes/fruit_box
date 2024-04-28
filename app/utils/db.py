import sqlite3
import streamlit as st


def get_db_con(db_path="fruit_box.db"):
    con = sqlite3.connect(db_path)
    return con


def insert_db(table: str, **kwargs):
    execute_query(
        f"INSERT INTO {table} ({', '.join(kwargs.keys())}) VALUES ({','.join(['?']*len(kwargs.keys()))})",
        tuple(kwargs.values()),
    )


def inquire_db(table: str, condition: str = "1=1", sort: str = None, limit: int = None):
    query = f"SELECT * FROM {table} WHERE {condition}{f' ORDER BY {sort}' if sort else ''}{f' LIMIT {str(limit)}' if limit else ''}"
    inquire_result = execute_query(query, fetch_value=True)
    return inquire_result


def execute_query(
    query: str = None, input_data: tuple = None, fetch_value: bool = False
):
    con = get_db_con()
    cursor = con.cursor()
    if input_data is None:
        cursor.execute(query)
    else:
        cursor.execute(query, input_data)
    result = cursor.fetchall()
    con.commit()
    con.close()
    if fetch_value:
        return result


def init_db():
    con = get_db_con()
    cursor = con.cursor()
    cursor.execute("DROP TABLE IF EXISTS user")
    cursor.execute("CREATE TABLE user(user_id text PRIMARY KEY, user_pw text)")
    cursor.execute("DROP TABLE IF EXISTS user_score")
    cursor.execute(
        "CREATE TABLE user_score(score_id integer PRIMARY KEY AUTOINCREMENT, user_id text, correct_box int, incorrect_box int, duration float, score int, date text)"
    )
    # cursor.execute('PRAGMA table_info(user_score)')
    con.commit()
    con.close()
    print("*** DB initializedd ***")


if __name__ == "__main__":
    init_db()
