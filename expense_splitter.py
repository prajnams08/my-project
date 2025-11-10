# expense_splitter.py

class ExpenseSplitter:
    def __init__(self, members):  # ✅ Fixed: double underscores
        self.members = members  # list of member names
        self.expenses = []      # list of (payer, amount, description)

    def add_expense(self, payer, amount, description=""):
        if payer not in self.members:
            print(f"⚠ {payer} is not in the group!")
            return
        self.expenses.append((payer, amount, description))
        print(f"✅ Added expense: {payer} paid ₹{amount} for {description}")

    def calculate_balances(self):
        total = sum(amount for _, amount, _ in self.expenses)
        per_person = total / len(self.members)
        balances = {member: -per_person for member in self.members}

        for payer, amount, _ in self.expenses:
            balances[payer] += amount
        return balances

    def show_summary(self):
        print("\n🧾 Expense Summary:")
        print("-----------------------------")
        for payer, amount, desc in self.expenses:
            print(f"{payer} paid ₹{amount:.2f} for {desc}")
        print("-----------------------------")

        balances = self.calculate_balances()
        print("\n💰 Final Balances:")
        for member, balance in balances.items():
            if balance > 0:
                print(f"{member} should RECEIVE ₹{balance:.2f}")
            elif balance < 0:
                print(f"{member} should PAY ₹{abs(balance):.2f}")
            else:
                print(f"{member} is SETTLED UP.")

        print("-----------------------------")
        self.show_settlements(balances)

    def show_settlements(self, balances):
        print("\n🤝 Suggested Settlements:")
        debtors = [(m, -b) for m, b in balances.items() if b < 0]
        creditors = [(m, b) for m, b in balances.items() if b > 0]

        i, j = 0, 0
        while i < len(debtors) and j < len(creditors):
            debtor, debt = debtors[i]
            creditor, credit = creditors[j]
            settled_amount = min(debt, credit)

            print(f"{debtor} → {creditor}: ₹{settled_amount:.2f}")

            debt -= settled_amount
            credit -= settled_amount

            if debt == 0:
                i += 1
            else:
                debtors[i] = (debtor, debt)
            if credit == 0:
                j += 1
            else:
                creditors[j] = (creditor, credit)


# -------------------------
# Example Run
# -------------------------
if __name__ == "__main__":  # ✅ Fixed: double underscores
    print("🏖  Welcome to Expense Splitter App")
    members = input("Enter names separated by commas: ").strip().split(",")
    members = [m.strip() for m in members]
    app = ExpenseSplitter(members)

    while True:
        print("\n1️⃣  Add Expense")
        print("2️⃣  Show Summary")
        print("3️⃣  Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            payer = input("Who paid? ")
            amount = float(input("Amount: ₹"))
            desc = input("Description: ")
            app.add_expense(payer, amount, desc)
        elif choice == "2":
            app.show_summary()
        elif choice == "3":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice, try again!")
