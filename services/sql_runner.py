from sqlalchemy import text
from databases.database import engine
from sqlalchemy.exc import SQLAlchemyError

def run_sql_file(file_path: str):
    with engine.connect() as connection:
        try:
            with open(file_path, "r") as file:
                sql_script = file.read()

                # Split and execute each statement
                for statement in sql_script.split(';'):
                    statement = statement.strip()
                    if statement:
                        connection.execute(text(statement))
            print(f"Executed SQL file: {file_path}")
        except SQLAlchemyError as e:
            print(f"Error executing SQL file {file_path}: {e}")
