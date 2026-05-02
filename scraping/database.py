from getpass import getpass
from mysql.connector import connect, Error

def create_letterboxd_database():
    try:
        with connect(
            host="127.0.0.1",
            user="root",
            password=getpass("Enter password: "),
        ) as connection:
            create_db_query = "CREATE DATABASE letterboxd_proj_db"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
    except Error as e:
        print(e)

def get_databases():
    with connect(
            host="127.0.0.1",
            user="root",
            password=getpass("Enter password: "),
        ) as connection:
            show_db_query = "SHOW DATABASES"
            with connection.cursor() as cursor:
                cursor.execute(show_db_query)
                for db in cursor:
                    print(db)

def get_tables():
    try:
        with connect(
            host="127.0.0.1",
            user="root",
            password="19MySQL!99",
            database="letterboxd_proj_db",
        ) as connection:
            show_tables_query = "SHOW TABLES LIKE 'tag_%'"
            with connection.cursor() as cursor:
                cursor.execute(show_tables_query)
                for table in cursor:
                    print(table)
    except Error as e:
        print(e)



def connect_to_database():
    try:
        with connect(
            host="127.0.0.1",
            user="root",
            password=getpass("Enter password: "),
            database="letterboxd_proj_db",
        ) as connection:
            print(connection)
    except Error as e:
        print(e)

def drop_table(table_name):
    try:
        with connect(
            host="127.0.0.1",
            user="root",
            password="19MySQL!99",
            database="letterboxd_proj_db",
        ) as connection:
            drop_table_query = f"DROP TABLE {table_name}"
            with connection.cursor() as cursor:
                cursor.execute(drop_table_query)

    except Error as e:
        print(e)

def create_diary_entries_table():
    try:
        with connect(
            host="127.0.0.1",
            user="root",
            password="19MySQL!99",
            database="letterboxd_proj_db",
        ) as connection:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS diary_entries(
                id INT AUTO_INCREMENT PRIMARY KEY,
                film_title VARCHAR(100),
                film_year YEAR(4),
                rating INT,
                liked BOOL,
                date DATE
            )
            """

            with connection.cursor() as cursor:
                cursor.execute(create_table_query)
                connection.commit()

    except Error as e:
        print(e)

def create_tags_table():
    try:
        with connect(
            host="127.0.0.1",
            user="root",
            password="19MySQL!99",
            database="letterboxd_proj_db",
        ) as connection:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS tags(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL
            )
            """

            with connection.cursor() as cursor:
                cursor.execute(create_table_query)
                connection.commit()

    except Error as e:
        print(e)

def create_diary_entry_tags_table():
    try:
        with connect(
            host="127.0.0.1",
            user="root",
            password="19MySQL!99",
            database="letterboxd_proj_db",
        ) as connection:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS diary_entry_tags(
                diary_entry_id INT NOT NULL,
                tag_id INT NOT NULL,
                PRIMARY KEY (diary_entry_id, tag_id),
                FOREIGN KEY (diary_entry_id) REFERENCES diary_entries(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            )
            """

            with connection.cursor() as cursor:
                cursor.execute(create_table_query)
                connection.commit()

    except Error as e:
        print(e)


def add_to_diary_entries_table(reviews):
    try:
        with connect(
            host="127.0.0.1",
            user="root",
            password="19MySQL!99",
            database="letterboxd_proj_db",
        ) as connection:
            insert_review_query = """
            INSERT INTO diary_entries
            (film_title, film_year, rating, liked, date)
            VALUES ( %s, %s, %s, %s, %s)
            """
            review_record = [list(review.values()) for review in reviews]
            with connection.cursor() as cursor:
                cursor.executemany(insert_review_query, review_record)
                connection.commit()
    except Error as e:
        print(e)

def insert_tag(tag_name):
    try:
        with connect(
            host="127.0.0.1",
            user="root",
            password="19MySQL!99",
            database="letterboxd_proj_db",
        ) as connection:
            insert_query = """
            INSERT IGNORE INTO tags (name) VALUES (%s)
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_query, (tag_name,))
                connection.commit()
                # Get the id
                cursor.execute("SELECT id FROM tags WHERE name = %s", (tag_name,))
                result = cursor.fetchone()
                return result[0] if result else None
    except Error as e:
        print(e)
        return None

def get_diary_entry_id(film_title, film_year, date_watched):
    try:
        with connect(
            host="127.0.0.1",
            user="root",
            password="19MySQL!99",
            database="letterboxd_proj_db",
        ) as connection:
            select_query = """
            SELECT id FROM diary_entries
            WHERE film_title = %s AND film_year = %s AND date = %s
            """
            with connection.cursor() as cursor:
                cursor.execute(select_query, (film_title, film_year, date_watched))
                result = cursor.fetchone()
                return result[0] if result else None
    except Error as e:
        print(e)
        return None

def insert_diary_entry_tag(diary_entry_id, tag_id):
    try:
        with connect(
            host="127.0.0.1",
            user="root",
            password="19MySQL!99",
            database="letterboxd_proj_db",
        ) as connection:
            insert_query = """
            INSERT IGNORE INTO diary_entry_tags (diary_entry_id, tag_id)
            VALUES (%s, %s)
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_query, (diary_entry_id, tag_id))
                connection.commit()
    except Error as e:
        print(e)

def select_from_table(table_name):
    try:
        with connect(
            host="127.0.0.1",
            user="root",
            password="19MySQL!99",
            database="letterboxd_proj_db",
        ) as connection:
            select_movies_query = f"SELECT * FROM `{table_name}` LIMIT 5"
            with connection.cursor() as cursor:
                cursor.execute(select_movies_query)
                result = cursor.fetchall()
                for row in result:
                    print(row)

    except Error as e:
        print(e)

if __name__ == '__main__':
    get_tables()