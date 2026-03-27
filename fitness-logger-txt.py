from datetime import datetime
import os
import sys

# == file setup ==
def create_file(fname):
    if not os.path.exists(fname):
        with open(fname, "w", encoding="utf-8") as f:
            f.write("")
        print(f"Created file, {fname}")

# == add an entry ==
def add_entry(fname):
    category = input("enter a category (gym,mindset,diet) => ").strip().lower()
    message = input("log entry => ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] ({category}) {message}\n" # ensure proper formatting
    with open(fname, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"Wrote entry: {entry}")

# == view entries ==
def view_entry(fname, limit):
    try:
        with open(fname, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines[-limit:]:
            print(line)
    except FileNotFoundError:
        print("File doesn't exist!")

# == search entries ==
def search_entries(fname, keyword):
    keyword = keyword.lower()
    try:
        with open(fname, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if keyword in line.lower():
                print("results: "+str(line))
    except FileNotFoundError:
        print("File doesn't exist!")

# == filter entries ==
def filter_entries(fname, category):
    category = category.lower()
    try:
        with open(fname, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if category in line.lower():
                print("results: "+str(line))
    except FileNotFoundError:
        print("File doesn't exist!")

# main loop
def main():
    if len(sys.argv) < 2:
        print(f"usage: python3 {sys.argv[0]} {sys.argv[1]}")
        sys.exit(1)
    filename = sys.argv[1]
    create_file(filename)
    while True:
        print("\n===== FITNESS LOGGER (TEXT VERSION) =====")
        print("1. Add entry")
        print("2. View entries")
        print("3. Search entries")
        print("4. Filter by category")
        print("5. Exit")

        choice = input("> ").strip()

        if choice == "1":
            add_entry(filename)

        elif choice == "2":
            try:
                limit = int(input("How many entries? (default 50) > ") or "50")
                view_entry(filename, limit)
            except ValueError:
                print("Invalid number.")

        elif choice == "3":
            keyword = input("Search keyword > ").strip()
            search_entries(filename, keyword)

        elif choice == "4":
            category = input("Category > ").strip()
            filter_entries(filename, category)

        elif choice == "5":
            print("Goodbye")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
