import snowflake.connector

from app.config import SNOWFLAKE_CONFIG


def get_connection():
    return snowflake.connector.connect(**SNOWFLAKE_CONFIG)


def test_connection() -> None:
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT CURRENT_USER(), CURRENT_DATABASE(), CURRENT_SCHEMA()"
        )

        result = cursor.fetchone()

        print("Snowflake connection successful.")
        print(f"User: {result[0]}")
        print(f"Database: {result[1]}")
        print(f"Schema: {result[2]}")

    finally:
        cursor.close()
        connection.close()