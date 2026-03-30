import sqlite3
from datetime import datetime
import random
import csv

DB_NAME = "fitness_logger.db"

QUOTES = [
    "Discipline beats motivation every time.",
    "You do not get stronger by staying comfortable.",
    "Progress is built one rep at a time.",
    "Todays pain is tomorrows power.",
    "You either win or you learn.",
    "Strength comes from doing what you said you would do.",
    "No shortcuts. Just work."
]


def db_init():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            category TEXT,
            exercise TEXT,
            message TEXT,
            weight REAL,
            reps INTEGER
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS prs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            exercise TEXT,
            weight REAL,
            reps INTEGER
        )
        """)


def get_lift_input():
    exercise = input("exercise => ").strip().lower()

    while True:
        try:
            weight = float(input("weight lbs => "))
            break
        except ValueError:
            print("enter a valid number")

    while True:
        try:
            reps = int(input("reps => "))
            break
        except ValueError:
            print("enter a valid integer")

    message = input("notes => ").strip().lower()
    category = input("category => ").strip().lower()

    return exercise, weight, reps, message, category


def get_best_pr(exercise):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()

        c.execute("""
        SELECT weight, reps
        FROM logs
        WHERE exercise = ?
        ORDER BY weight DESC, reps DESC
        LIMIT 1
        """, (exercise,))

        return c.fetchone()


def add_entry():
    exercise, weight, reps, message, category = get_lift_input()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    previous = get_best_pr(exercise)

    is_pr = False
    if previous is None:
        is_pr = True
    else:
        prev_weight, prev_reps = previous
        if weight > prev_weight or (weight == prev_weight and reps > prev_reps):
            is_pr = True

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()

        c.execute("""
        INSERT INTO logs (timestamp, category, exercise, message, weight, reps)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, category, exercise, message, weight, reps))

        if is_pr:
            c.execute("""
            INSERT INTO prs (timestamp, exercise, weight, reps)
            VALUES (?, ?, ?, ?)
            """, (timestamp, exercise, weight, reps))

    print("\n[" + timestamp + "] " + exercise + " " + str(weight) + " x " + str(reps))

    if is_pr:
        print("NEW PR")
        print(random.choice(QUOTES))
    else:
        print("logged")


def view_logs(limit=50):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()

        c.execute("""
        SELECT timestamp, exercise, weight, reps, category, message
        FROM logs
        ORDER BY id DESC
        LIMIT ?
        """, (limit,))

        rows = c.fetchall()

    if not rows:
        print("no logs yet")
        return

    for r in rows:
        print("[" + r[0] + "] " + r[1] + " " + str(r[2]) + "x" + str(r[3]) + " (" + r[4] + ") | " + r[5])


def view_prs():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()

        c.execute("""
        SELECT timestamp, exercise, weight, reps
        FROM prs
        ORDER BY id DESC
        """)

        rows = c.fetchall()

    if not rows:
        print("no prs yet")
        return

    for r in rows:
        print("PR [" + r[0] + "] " + r[1] + " " + str(r[2]) + "x" + str(r[3]))


def search_logs(keyword):
    keyword = "%" + keyword.lower() + "%"

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()

        c.execute("""
        SELECT timestamp, exercise, weight, reps, message
        FROM logs
        WHERE LOWER(exercise) LIKE ?
           OR LOWER(message) LIKE ?
        ORDER BY id DESC
        """, (keyword, keyword))

        rows = c.fetchall()

    if not rows:
        print("no matches found")
        return

    print("\nresults\n")
    for r in rows:
        print("[" + r[0] + "] " + r[1] + " " + str(r[2]) + "x" + str(r[3]) + " | " + r[4])


def filter_logs():
    mode = input("filter by category or exercise => ").strip().lower()
    value = input("value => ").strip().lower()

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()

        if mode == "category":
            c.execute("""
            SELECT timestamp, exercise, weight, reps, category, message
            FROM logs
            WHERE LOWER(category) = ?
            ORDER BY id DESC
            """, (value,))
        elif mode == "exercise":
            c.execute("""
            SELECT timestamp, exercise, weight, reps, category, message
            FROM logs
            WHERE LOWER(exercise) = ?
            ORDER BY id DESC
            """, (value,))
        else:
            print("invalid filter type")
            return

        rows = c.fetchall()

    if not rows:
        print("no results")
        return

    print("\nfiltered\n")
    for r in rows:
        print("[" + r[0] + "] " + r[1] + " " + str(r[2]) + "x" + str(r[3]) + " (" + r[4] + ") | " + r[5])


def export_csv():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM logs")
        rows = c.fetchall()

    with open("fitness_logs.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "timestamp", "category", "exercise", "message", "weight", "reps"])
        writer.writerows(rows)

    print("exported to fitness_logs.csv")


def export_txt():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT timestamp, exercise, weight, reps, message FROM logs")
        rows = c.fetchall()

    with open("fitness_logs.txt", "w") as f:
        for r in rows:
            f.write("[" + r[0] + "] " + r[1] + " " + str(r[2]) + "x" + str(r[3]) + " | " + r[4] + "\n")

    print("exported to fitness_logs.txt")


def main():
    db_init()

    while True:
        print("\n===== FITNESS LOGGER =====")
        print("1 add workout")
        print("2 view logs")
        print("3 view prs")
        print("4 search")
        print("5 filter")
        print("6 export csv")
        print("7 export txt")
        print("8 exit")

        choice = input("> ").strip()

        if choice == "1":
            add_entry()

        elif choice == "2":
            try:
                limit = int(input("limit default 50 => ") or "50")
            except ValueError:
                limit = 50
            view_logs(limit)

        elif choice == "3":
            view_prs()

        elif choice == "4":
            search_logs(input("keyword => "))

        elif choice == "5":
            filter_logs()

        elif choice == "6":
            export_csv()

        elif choice == "7":
            export_txt()

        elif choice == "8":
            print("bye")
            break

        else:
            print("invalid option")


if __name__ == "__main__":
    main()
