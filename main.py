"""Personal Finance Tracker"""
__author__ = "Ethan Padgett"
# Description: A simple personal finance tracker that allows users to record income and expenses and calculate balance and estimated tax.
# The program saves data to a JSON file and pie chart (png) and checks for existing data before prompting for new input.

import os
import json
import matplotlib.pyplot as plt

# (-) Subtracts threshold to get amount taxable amount
# (+) Adds base tax and extra tax
# (*) Multiplies by tax rate
def estimate_tax(income: float) -> float:
    if income <= 10000:
        return (income * 0.10)
    
    if income <= 40000:
        return (1000 + (income - 10000) * 0.15)
    
    if income <= 85000:
        return (5500 + (income - 40000) * 0.20)
    
    return (15500 + (income - 85000) * 0.25)

def check_for_old_data() -> bool:
    if not os.path.exists("financial_data.json"):
        with open("financial_data.json", "w") as file:
            file.write("")
        return False

    with open("financial_data.json", "r") as file:
        return bool(file.read().strip())
    
def simulate_savings(data: dict, months: int, growth_rate: float = 0.05) -> None:
    if months < 0:
        print("Number of months must greater than zero.")
        return

    print("\n--- Savings Simulation ---")

    balance = data["balance"]
    income = data["income"]
    total_expenses = data["total_expenses"]

    # Loop through each month and simulate
    for month in range(1, months + 1):
        # Add income and subtract expenses
        balance += income
        balance -= total_expenses

        # Apply growth rate if positive balance
        if balance > 0 and growth_rate > 0:
            balance += balance * growth_rate  # shortcut operator

        # Boolean logic
        if balance < 0:
            status = "Deficit"
        elif balance == 0:
            status = "Even"
        else:
            status = "Surplus"

        print(f"Month {month}: Balance = ${balance:.2f} ({status})")

    print("\nSimulation complete!")

def get_valid_float(prompt: str, allow_zero=True) -> float:
    value = None
    while value is None:
        try:
            value = float(input(prompt))
            if value < 0 or (not allow_zero and value == 0):
                raise ValueError
            
        except ValueError:
            value = None
            print("Please enter a valid number.\n")

    return value

def generate_expense_pie_chart(expenses: dict) -> None:
    # Convert the dict_values objects to lists so matplotlib can treat them array-like
    labels = list(expenses.keys())
    sizes = list(expenses.values())

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)

    # Equal aspect ratio so chart is a circle 
    # (https://matplotlib.org/stable/gallery/subplots_axes_and_figures/axis_equal_demo.html)
    plt.axis('equal')

    plt.savefig("expenses_chart.png")
    print("\nExpense pie chart saved as expenses_chart.png")

    plt.show()

def main():
    # Checks for existing data file
    if not check_for_old_data():
        print("Welcome to the Personal Finance Tracker!\nThis program helps you record your income and expenses.")

        # Prompts user for financial data with input validation
        income = get_valid_float("Enter your monthly income: ")
        rent =  get_valid_float("Enter your monthly rent: ")
        groceries =  get_valid_float("Enter your monthly groceries cost: ")
        entertainment =  get_valid_float("Enter your monthly entertainment cost: ")
        other =  get_valid_float("Enter your other costs: ")

        # Adds all expenses together into a new variable
        total_expenses = (rent + groceries + entertainment + other)
    
        # Subtracts all expenses from income into a new variable
        balance = (income - total_expenses)
    
        # Calculates estimated tax based on income into a new variable
        estimated_tax = estimate_tax(income)

        # Stores all financial data in a dictionary
        new_data = {
            "income": income,
            "expenses": {
                "rent": rent,
                "groceries": groceries,
                "entertainment": entertainment,
                "other": other
            },
            "total_expenses": round(total_expenses, 2),
            "balance": round(balance, 2),
            "estimated_tax": round(estimated_tax, 2)
        }
        
        with open("financial_data.json", "w") as file:
            json.dump(new_data, file, indent=4) 

        print("\nData saved to financial_data.json")

    chart = input("\nWould you like to generate and save an expense pie chart? (y/n): ").strip().lower()

    if chart == 'y':
        with open("financial_data.json", "r") as file:
            data = json.load(file)
        generate_expense_pie_chart(data["expenses"])

    months = int(input("\nWould you like to simulate your savings over x amount of months? (0 to skip)\n"))

    if months != 0:
        with open("financial_data.json", "r") as file:
            data = json.load(file)
        simulate_savings(data, months)

if __name__ == "__main__":
    main()