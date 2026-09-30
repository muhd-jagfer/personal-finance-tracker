# PERSONAL FINANCE TRACKER


#### Description:

Personal Finance Tracker is a Python command-line application for recording and reviewing income and expenses.

The program stores all the transactions in a file called `dataset.csv`. Each transaction has a date, amount, category, and description. The user can add a new transaction from the menu and choose whether it is an Income or an Expense.

There are three options in the main menu:

* Add Transaction
* View Transactions
* Exit

When adding a transaction, the program asks for the date, amount, category, and description. Before saving it, it shows a preview so the user can check the details.

The View Transactions option lets the user enter a start date and an end date. The program then finds the transactions between those dates and displays them. It also shows the total income, total expenses, and the balance.

I used Pandas to read and work with the CSV file. I used Matplotlib to make a graph showing income and expenses over time. The graph is saved as `transaction_graph.png`.

I also used a separate `data.py` file for some of the input functions like asking for the amount, category, date, and description, This separates input-related functions from the main program logic and keeps the code organized.

While making this project, I learned more about working with CSV files, Pandas, dates, and graphs in Python. I also had to deal with things like invalid dates, empty data, and making sure the start date is not after the end date.
