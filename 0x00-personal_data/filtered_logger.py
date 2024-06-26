#!/usr/bin/env python3
"""Write a function called filter_datum that
returns the log message obfuscated:

Arguments:
fields: a list of strings representing
all fields to obfuscate
redaction: a string representing by what the
field will be obfuscated
message: a string representing the log line
separator: a string representing by which character
is separating all fields in the log line (message)
The function should use a regex to replace
occurrences of certain field values.
filter_datum should be less than 5 lines long and
use re.sub to perform the substitution with a
single regex.
"""

import re
from typing import List
import logging
import os
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Return the log message obfuscated using Regex."""
        org = super().format(record)
        return filter_datum(self.fields, self.REDACTION, org, self.SEPARATOR)


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Replaces sensitive information in a message with a redacted value
    based on the list of fields to redact

    Args:
        fields: list of fields to redact
        redaction: the value to use for redaction
        message: the string message to filter
        separator: the separator to use between fields

    Returns:
        The filtered string message with redacted values
    """
    for field in fields:
        regex = f"{field}=[^{separator}]*"
        message = re.sub(regex, f"{field}={redaction}", message)
    return message


# PII fileds to be redacted
PII_FIELDS = ("name", "phone", "ssn", "password", "ip")


def get_logger() -> logging.Logger:
    """
    Returns a Logger object for handling Personal Data

    Returns:
        A Logger object with INFO log level and RedactingFormatter
        formatter for filtering PII fields
    """

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a MySQLConnection object for accessing Personal Data database

    Returns:
        A MySQLConnection object using connection details from
        environment variables
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username, password=password, host=host, database=db_name
    )


def main() -> None:
    """Main function to retrieve user data from
    database and log to console.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    field_names = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = "".join(f"{f}={str(r)}; " for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
