import sqlite3


def secure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
    """
    def inner(*args, **kwargs):
        with sqlite3.connect('anketa.db') as conn:
            kwargs['conn'] = conn
            result = func(*args, **kwargs)
        return result
    return inner


@ secure_connection
def init_db(conn, force: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их
        Важно: миграции на такие таблицы вы должны производить самостоятельно!
        :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS user_info')

    c.execute('''
        CREATE TABLE IF NOT EXISTS user_info (
            id INTEGER PRIMARI KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            chat_id INTEGER NOT NULL
        )
    ''')
    conn.commit()


@secure_connection
def add_user(conn, username: str, email: str, chat_id: int):
    c = conn.cursor()
    c.execute(
        'INSERT INTO user_info (username, email, chat_id)'
        'VALUES (?, ?, ?)', (username, email, chat_id))
    conn.commit()


@secure_connection
def list_user(conn):
    c = conn.cursor()
    c.execute('SELECT username, email, chat_id FROM user_info')
    return c.fetchall()


@secure_connection
def clear_user(conn):
    c = conn.cursor()
    # c.execute('DROP TABLE IF EXISTS user_info')
    c.execute('DELETE FROM user_info')
