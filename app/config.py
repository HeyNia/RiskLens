import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        try:
            value = st.secrets.get(name)
        except FileNotFoundError:
            value = None

    if not value:
        raise ValueError(f"Missing required environment variable: {name}")

    return value


SNOWFLAKE_CONFIG = {
    "account": get_required_env("SNOWFLAKE_ACCOUNT"),
    "user": get_required_env("SNOWFLAKE_USER"),
    "password": get_required_env("SNOWFLAKE_PASSWORD"),
    "warehouse": get_required_env("SNOWFLAKE_WAREHOUSE"),
    "database": get_required_env("SNOWFLAKE_DATABASE"),
    "schema": get_required_env("SNOWFLAKE_SCHEMA"),
    "role": get_required_env("SNOWFLAKE_ROLE"),
}