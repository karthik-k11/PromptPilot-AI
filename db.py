import sqlite3
from pathlib import Path


DATABASE_FOLDER = Path("database")
DATABASE_FOLDER.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_FOLDER / "prompts.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def create_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prompt_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            original_prompt TEXT NOT NULL,

            optimized_prompt TEXT NOT NULL,

            platform TEXT NOT NULL,

            prompt_type TEXT NOT NULL,

            original_score INTEGER NOT NULL,

            optimized_score INTEGER NOT NULL,

            score_improvement INTEGER NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    connection.commit()

    connection.close()

def save_prompt(
    original_prompt,
    optimized_prompt,
    platform,
    prompt_type,
    original_score,
    optimized_score,
    score_improvement
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO prompt_history (

            original_prompt,
            optimized_prompt,
            platform,
            prompt_type,
            original_score,
            optimized_score,
            score_improvement

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,

        (
            original_prompt,
            optimized_prompt,
            platform,
            prompt_type,
            original_score,
            optimized_score,
            score_improvement
        )

    )

    connection.commit()

    connection.close()

def get_prompt_history():

    connection = get_connection()

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *

        FROM prompt_history

        ORDER BY created_at DESC
        """
    )

    history = cursor.fetchall()

    connection.close()

    return history

def delete_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM prompt_history
        """
    )

    connection.commit()

    connection.close()