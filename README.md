# Student Database - PostgreSQL

This 100-mark practical uses Python, `psycopg2`, and PostgreSQL to create a
`students` table, insert a Kaggle-style academic-performance dataset, and
retrieve students whose CGPA is greater than 8.0.

The CSV columns are adapted from the Kaggle **Students Performance in Exams**
dataset. The original dataset provides math, reading, and writing scores; this
practical adds `student_id`, identity/course fields, and a normalized `cgpa`
column so the requested query can be demonstrated directly.

## Setup

1. Create a PostgreSQL database named `student_db` (or set `PGDATABASE` to an
   existing database).
2. Install the Python dependency:

   ```powershell
   py -m pip install -r requirements.txt
   ```

3. Set credentials if they differ from the defaults:

   ```powershell
   $env:PGUSER = "postgres"
   $env:PGPASSWORD = "your_password"
   $env:PGHOST = "localhost"
   $env:PGPORT = "5432"
   $env:PGDATABASE = "student_db"
   ```

4. Run the program:

   ```powershell
   py student_database.py
   ```

The program is repeatable: `ON CONFLICT` updates an existing student instead
of inserting duplicates. It commits the table and data transaction only after
the query has completed, and rolls back on a database error.