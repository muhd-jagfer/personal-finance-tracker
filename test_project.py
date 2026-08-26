import pandas as pd

from project import (
    print_header,
    display_summary,
    show_menu,
    create_transaction_graph
)


def test_print_header(capsys):
    result = print_header("TEST HEADER")

    output = capsys.readouterr().out

    assert result is None
    assert "TEST HEADER" in output


def test_display_summary(capsys):
    data = pd.DataFrame({
        "date": ["14-08-2026", "14-08-2026"],
        "amount": [1000, 300],
        "category": ["Income", "Expense"],
        "description": ["Salary", "Food"]
    })

    result = display_summary(data)

    output = capsys.readouterr().out

    assert result is None
    assert "₹1,000.00" in output
    assert "₹300.00" in output
    assert "₹700.00" in output


def test_show_menu(capsys):
    result = show_menu()

    output = capsys.readouterr().out

    assert result is None
    assert "PERSONAL FINANCE TRACKER" in output
    assert "1. Add Transaction" in output
    assert "2. View Transactions" in output
    assert "3. Exit" in output


def test_create_transaction_graph(monkeypatch):
    data = pd.DataFrame({
        "date": ["14-08-2026", "14-08-2026"],
        "amount": [1000, 300],
        "category": ["Income", "Expense"],
        "description": ["Salary", "Food"]
    })

    monkeypatch.setattr(
        "project.plt.show",
        lambda block=True: None
    )
    monkeypatch.setattr(
        "project.plt.savefig",
        lambda filename: None
    )

    result = create_transaction_graph(data)

    assert result is None
