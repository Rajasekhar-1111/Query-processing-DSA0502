"""Create, populate, and query a PostgreSQL student database."""

from __future__ import annotations

import csv
import os
from pathlib import Path

import psycopg2
from psycopg2 import Error
from psycopg2 import sql
from psycopg2.extras import execute_values


DATA_FILE = Path(__file__).parent / "data" / "students.csv"
TABLE_NAME = "students"


def database_config() -> dict[str, object]:
    """Read PostgreSQL connection settings from environment variables."""
    return {
        "host": os.getenv("PGHOST", "localhost"),
        "port": int(os.getenv("PGPORT", "5432")),
        "dbname": os.getenv("PGDATABASE", "student_db"),
        "user": os.getenv("PGUSER", "postgres"),
        "password": os.getenv("PGPASSWORD", "postgres"),
    }


def load_students() -> list[tuple[object, ...]]:
    """Load and convert the Kaggle-derived CSV rows to database values."""
    students: list[tuple[object, ...]] = []
    with DATA_FILE.open(newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            students.append(
                (
                    int(row["student_id"]),
                    row["name"],
                    int(row["age"]),
                    row["gender"],
                    row["course"],
                    float(row["math_score"]),
                    float(row["reading_score"]),
                    float(row["writing_score"]),
                    float(row["cgpa"]),
                )
            )
    return students


def create_database_if_missing(config: dict[str, object]) -> None:
    """Create the target database once, using PostgreSQL's default database."""
    target_database = str(config["dbname"])
    admin_config = {**config, "dbname": "postgres"}
    connection = psycopg2.connect(**admin_config)
    connection.autocommit = True
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (target_database,),
            )
            if cursor.fetchone() is None:
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(target_database)
                    )
                )
                print(f"Created PostgreSQL database '{target_database}'.")
    finally:
        connection.close()


def main() -> None:
    students = load_students()
    config = database_config()
    connection = None
    try:
        create_database_if_missing(config)
        connection = psycopg2.connect(**config)
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    student_id INTEGER PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INTEGER CHECK (age BETWEEN 16 AND 100),
                    gender VARCHAR(20),
                    course VARCHAR(100) NOT NULL,
                    math_score NUMERIC(5, 2) CHECK (math_score BETWEEN 0 AND 100),
                    reading_score NUMERIC(5, 2) CHECK (reading_score BETWEEN 0 AND 100),
                    writing_score NUMERIC(5, 2) CHECK (writing_score BETWEEN 0 AND 100),
                    cgpa NUMERIC(4, 2) CHECK (cgpa BETWEEN 0 AND 10)
                )
                """
            )
            execute_values(
                cursor,
                f"""
                INSERT INTO {TABLE_NAME}
                    (student_id, name, age, gender, course, math_score,
                     reading_score, writing_score, cgpa)
                VALUES %s
                ON CONFLICT (student_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    age = EXCLUDED.age,
                    gender = EXCLUDED.gender,
                    course = EXCLUDED.course,
                    math_score = EXCLUDED.math_score,
                    reading_score = EXCLUDED.reading_score,
                    writing_score = EXCLUDED.writing_score,
                    cgpa = EXCLUDED.cgpa
                """,
                students,
            )
            cursor.execute(
                f"""
                SELECT student_id, name, course, cgpa
                FROM {TABLE_NAME}
                WHERE cgpa > %s
                ORDER BY cgpa DESC, student_id
                """,
                (8.0,),
            )
            high_cgpa_students = cursor.fetchall()
        connection.commit()

        print(f"Inserted or updated {len(students)} students in '{TABLE_NAME}'.")
        print("\nStudents with CGPA above 8.0")
        print("-" * 48)
        for student_id, name, course, cgpa in high_cgpa_students:
            print(f"{student_id:>3} | {name:<20} | {course:<18} | {cgpa:.2f}")
        print(f"\nFound {len(high_cgpa_students)} students.")
    except Error as error:
        if connection is not None:
            connection.rollback()
        print(f"Database error: {error}")
        raise SystemExit(1) from error
    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    main()