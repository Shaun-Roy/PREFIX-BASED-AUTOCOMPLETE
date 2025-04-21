import os
import sqlite3

DB_NAME = "autocomplete.db"

def delete_database():
    """Deletes the SQLite database file entirely."""
    
    # Close the connection if it's open
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)  # Deletes the entire database file
        print(f"The database '{DB_NAME}' has been deleted.")
    else:
        print(f"{DB_NAME} does not exist.")
    
def create_new_database():
    """Creates a new SQLite database with the necessary table."""
    # Create a new database connection
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create the autocomplete table with new columns: ngrams and score
    cursor.execute("""
        CREATE TABLE ngrams (
            ngrams TEXT ,
            count INTEGER DEFAULT 0
        )
    """)

    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"{DB_NAME} has been recreated and set up with the ngrams and score columns.")

if __name__ == "__main__":
    delete_database()  # Deletes the existing database
    create_new_database()  # Creates a new empty database with the required table
