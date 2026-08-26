import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt

from data import ask_amount, ask_category, ask_date, ask_description


class TransactionFile:

    FILE_NAME = "dataset.csv"
    HEADERS = ["date", "amount", "category", "description"]
    DATE_FORMAT = "%d-%m-%Y"

    @classmethod
    def create_file(cls):
        try:
            pd.read_csv(cls.FILE_NAME)
        except FileNotFoundError:
            data = pd.DataFrame(columns=cls.HEADERS)
            data.to_csv(cls.FILE_NAME, index=False)

    @classmethod
    def save_transaction(cls, transaction_date, transaction_amount,
                         transaction_type, transaction_note):

        transaction = {
            "date": transaction_date,
            "amount": transaction_amount,
            "category": transaction_type,
            "description": transaction_note
        }

        with open(cls.FILE_NAME, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=cls.HEADERS)
            writer.writerow(transaction)

    @classmethod
    def load_transactions(cls, first_date, last_date):

        try:
            data = pd.read_csv(cls.FILE_NAME)
        except FileNotFoundError:
            return pd.DataFrame(columns=cls.HEADERS)

        if data.empty:
            return data

        data["date"] = pd.to_datetime(
            data["date"],
            format=cls.DATE_FORMAT,
            errors="coerce"
        )

        data["amount"] = pd.to_numeric(
            data["amount"],
            errors="coerce"
        )

        data = data.dropna(subset=["date", "amount"])

        first_date = datetime.strptime(first_date, cls.DATE_FORMAT)
        last_date = datetime.strptime(last_date, cls.DATE_FORMAT)

        result = (
            (data["date"] >= first_date) &
            (data["date"] <= last_date)
        )

        return data.loc[result].copy()


def print_header(title):
    print("\n")
    print("=" * 60)
    print(f"{title:^60}")
    print("=" * 60)


def record_transaction():

    print_header("ADD NEW TRANSACTION")

    transaction_date = ask_date(
        "Date (DD-MM-YYYY) [Press Enter for today]: ",
        default_today=True
    )

    transaction_amount = ask_amount()
    transaction_type = ask_category()
    transaction_note = ask_description()

    print("\n" + "-" * 60)
    print("TRANSACTION PREVIEW")
    print("-" * 60)

    print(f"Date        : {transaction_date}")
    print(f"Amount      : ₹{transaction_amount:,.2f}")
    print(f"Type        : {transaction_type}")
    print(f"Description : {transaction_note}")

    print("-" * 60)

    choice = input("Save transaction? [Y/N]: ").strip().upper()

    if choice == "Y":
        TransactionFile.save_transaction(
            transaction_date,
            transaction_amount,
            transaction_type,
            transaction_note
        )
        print("\nTransaction saved successfully.")
    else:
        print("\nTransaction discarded.")


def display_summary(data):

    income = data[data["category"] == "Income"]["amount"].sum()
    expense = data[data["category"] == "Expense"]["amount"].sum()
    balance = income - expense

    print("\n")
    print("-" * 60)
    print("FINANCIAL SUMMARY")
    print("-" * 60)

    print(f"Income       : ₹{income:,.2f}")
    print(f"Expenses     : ₹{expense:,.2f}")
    print(f"Balance      : ₹{balance:,.2f}")

    if balance > 0:
        print("\nStatus       : Positive balance")
    elif balance < 0:
        print("\nStatus       : Expenses are higher than income")
    else:
        print("\nStatus       : Break even")

    print("-" * 60)


def display_transactions():

    print_header("VIEW TRANSACTIONS")

    first_date = ask_date("Start date (DD-MM-YYYY): ")
    last_date = ask_date("End date   (DD-MM-YYYY): ")

    first_datetime = datetime.strptime(
        first_date, TransactionFile.DATE_FORMAT
    )
    last_datetime = datetime.strptime(
        last_date, TransactionFile.DATE_FORMAT
    )

    if first_datetime > last_datetime:
        print("\nStart date cannot be after end date.")
        return

    data = TransactionFile.load_transactions(
        first_date,
        last_date
    )

    if data.empty:
        print(f"\nNo transactions found between {first_date} and {last_date}.")
        return

    table = data.copy()

    table["date"] = table["date"].dt.strftime(
        TransactionFile.DATE_FORMAT
    )

    table["amount"] = table["amount"].apply(
        lambda x: f"₹{x:,.2f}"
    )

    print(f"\nTransactions: {first_date} → {last_date}")
    print("-" * 75)
    print(table.to_string(index=False))

    display_summary(data)

    choice = input(
        "\nShow income and expense graph? [Y/N]: "
    ).strip().upper()

    if choice == "Y":
        create_transaction_graph(data)


def create_transaction_graph(data):

    if data.empty:
        print("\nThere is no data available for the graph.")
        return

    graph_data = data.copy()

    graph_data["date"] = pd.to_datetime(
        graph_data["date"],
        format=TransactionFile.DATE_FORMAT
    )

    graph_data.set_index("date", inplace=True)
    graph_data.sort_index(inplace=True)

    dates = pd.date_range(
        graph_data.index.min(),
        graph_data.index.max(),
        freq="D"
    )

    income = (
        graph_data[graph_data["category"] == "Income"]["amount"]
        .resample("D")
        .sum()
        .reindex(dates, fill_value=0)
    )

    expense = (
        graph_data[graph_data["category"] == "Expense"]["amount"]
        .resample("D")
        .sum()
        .reindex(dates, fill_value=0)
    )

    plt.figure(figsize=(11, 5))

    plt.plot(
        income.index,
        income.values,
        color="green",
        marker="o",
        label="Income"
    )

    plt.plot(
        expense.index,
        expense.values,
        color="red",
        marker="o",
        label="Expense"
    )

    plt.xlabel("Date")
    plt.ylabel("Amount (₹)")
    plt.title("Income vs Expense")

    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig("transaction_graph.png")

    print("\nGraph saved as transaction_graph.png")

    plt.show(block=True)


def show_menu():

    print("\n")
    print("=" * 60)
    print("              PERSONAL FINANCE TRACKER")
    print("=" * 60)
    print("  1. Add Transaction")
    print("  2. View Transactions")
    print("  3. Exit")
    print("=" * 60)


def main():

    TransactionFile.create_file()

    while True:

        show_menu()

        choice = input("Select an option [1-3]: ").strip()

        if choice == "1":
            record_transaction()

        elif choice == "2":
            display_transactions()

        elif choice == "3":
            print("\nThank you for using Personal Finance Tracker.")
            print("Program closed.")
            break

        else:
            print("\nInvalid option. Please select 1, 2 or 3.")


if __name__ == "__main__":
    main()
