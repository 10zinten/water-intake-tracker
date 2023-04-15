from datetime import datetime
import subprocess
from pathlib import Path

from tinydb import TinyDB

# CONSTANTS
WATER_PER_INTAKE = 0.05 # in liters

db_path = Path(__file__).resolve().parent / "water-intake-records.json"
db = TinyDB(db_path)


def ask_to_drink_water():

    applescript = '''
    tell application "System Events"
        display dialog "Please drink a glass of water." with title "💧 Drink Water Reminder" buttons {"OK"} default button 1 giving up after 5

        set userResponse to button returned of (display dialog "Did you drink water?" with title "💧 Confirmation" buttons {"No", "Yes"} default button 1)

        if userResponse is "Yes" then
            display dialog "Great! Stay hydrated! 😀" with title "💧 Success" buttons {"OK"} default button 1 giving up after 5
        else
            display dialog "remember to drink water regularly. 💧💧💧" with title "💧 Reminder" buttons {"OK"} default button 1 giving up after 5
        end if

        return userResponse
    end tell
    '''

    result = subprocess.run(
        ["osascript", "-e", applescript],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    user_response = result.stdout.strip()
    return True if user_response == "Yes" else False

def record_in_db():
    record = {"datetime": str(datetime.now()), "intake": WATER_PER_INTAKE} 
    db.insert(record)


def main():
    have_drunk = ask_to_drink_water()
    if have_drunk:
       record_in_db()


if __name__ == "__main__":
    exit(main())
