import datetime
import sqlite3
import subprocess
from pathlib import Path


def alert_to_drink_water():
    ALERT_CMD = """
    display alert "Time to Drink Water"
    """

    result = subprocess.run(["osascript", "-e", ALERT_CMD], capture_output=True)
    stdout = result.stdout.decode()
    return "OK" in stdout

def record_in_db():
    DATABASE_PATH = Path(__file__).parent / "personal.db"
    sql_create_water_intake_record_table = """
        CREATE TABLE IF NOT EXISTS water_intake_record (
            id integer PRIMARY KEY,
            datetime TIMESTAMP
        );
    """
    sql_inter_query = """
        INSERT INTO water_intake_record (datetime)
        VALUES (?);
    """


    conn = sqlite3.connect(
        str(DATABASE_PATH),
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )

    conn.execute(sql_create_water_intake_record_table)

    conn.execute(sql_inter_query, (datetime.datetime.now(),))

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM water_intake_record")
    for row in cursor.fetchall():
        print(row[1].day)


def main():
    have_drunk = alert_to_drink_water()
    if have_drunk:
        record_in_db()


if __name__ == "__main__":
    exit(main())
