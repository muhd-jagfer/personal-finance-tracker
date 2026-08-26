from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"

TRANSACTION_TYPES = {
    "I": "Income",
    "E": "Expense"
}


def ask_date(message, default_today=False):
    while True:
        date_text = input(message).strip()

        if default_today and not date_text:
            return datetime.today().strftime(DATE_FORMAT)

        try:
            selected_date = datetime.strptime(
                date_text,
                DATE_FORMAT
            )

            return selected_date.strftime(DATE_FORMAT)

        except ValueError:
            print(
                "\nInvalid date. Please enter it in "
                "DD-MM-YYYY format."
            )


def ask_amount():
    while True:
        try:
            amount_text = input(
                "Enter amount (₹): "
            ).strip()

            amount = float(amount_text)

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return amount

        except ValueError:
            print("Please enter a valid amount.")


def ask_category():
    while True:
        print("\nTransaction Type")
        print("  [I] Income")
        print("  [E] Expense")

        selected_type = input(
            "Choose type: "
        ).strip().upper()

        if selected_type in TRANSACTION_TYPES:
            return TRANSACTION_TYPES[selected_type]

        print("Please choose either I or E.")


def ask_description():
    description = input(
        "Description (optional): "
    ).strip()

    if description:
        return description

    return "No description"
