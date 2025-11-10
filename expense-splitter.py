import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import matplotlib.pyplot as plt
import csv

class ExpenseSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💖 Expense Splitter App v2")
        self.root.geometry("520x560")
        self.root.config(bg="#fef6fb")

        self.members = []
        self.expenses = []

        # 🧍‍♀️ Members Frame
        member_frame = tk.LabelFrame(root, text="👥 Add Members", bg="#fef6fb", font=("Arial", 10, "bold"))
        member_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(member_frame, text="Names (comma separated):", bg="#fef6fb").pack()
        self.member_entry = tk.Entry(member_frame, width=40)
        self.member_entry.pack(pady=5)
        tk.Button(member_frame, text="Add Members", command=self.add_members, bg="#ffd1dc", font=("Arial", 9, "bold")).pack(pady=5)

        # 💰 Expense Frame
        expense_frame = tk.LabelFrame(root, text="💳 Add Expense", bg="#fef6fb", font=("Arial", 10, "bold"))
        expense_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(expense_frame, text="Who paid?", bg="#fef6fb").pack()
        self.payer_combo = ttk.Combobox(expense_frame, state="readonly", width=30)
        self.payer_combo.pack(pady=5)

        tk.Label(expense_frame, text="Amount (₹):", bg="#fef6fb").pack()
        self.amount_entry = tk.Entry(expense_frame, width=20)
        self.amount_entry.pack(pady=5)

        tk.Label(expense_frame, text="Description:", bg="#fef6fb").pack()
        self.desc_entry = tk.Entry(expense_frame, width=40)
        self.desc_entry.pack(pady=5)

        tk.Button(expense_frame, text="Add Expense", command=self.add_expense, bg="#b9fbc0", font=("Arial", 9, "bold")).pack(pady=5)

        # 📊 Buttons Frame
        button_frame = tk.Frame(root, bg="#fef6fb")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="🧾 Show Summary", command=self.show_summary, bg="#ffecb3", width=15).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="📈 Show Chart", command=self.show_chart, bg="#c1f0f6", width=15).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="💾 Export CSV", command=self.export_csv, bg="#d7bde2", width=15).grid(row=0, column=2, padx=5)

        # 📋 Output
        self.output_text = tk.Text(root, height=15, width=60, bg="#fff7fa")
        self.output_text.pack(pady=10)

    def add_members(self):
        names = self.member_entry.get().strip()
        if not names:
            messagebox.showwarning("Warning", "Please enter at least one name!")
            return
        self.members = [n.strip() for n in names.split(",") if n.strip()]
        self.payer_combo["values"] = self.members
        messagebox.showinfo("Success", f"Members added: {', '.join(self.members)}")

    def add_expense(self):
        payer = self.payer_combo.get()
        amount = self.amount_entry.get()
        desc = self.desc_entry.get()

        if not payer or not amount:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number for amount!")
            return

        self.expenses.append((payer, amount, desc))
        messagebox.showinfo("Added", f"{payer} paid ₹{amount:.2f} for {desc}")
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def show_summary(self):
        if not self.expenses:
            messagebox.showinfo("Info", "No expenses added yet!")
            return

        total = sum(a for _, a, _ in self.expenses)
        per_person = total / len(self.members)
        balances = {m: -per_person for m in self.members}
        for payer, amount, _ in self.expenses:
            balances[payer] += amount

        result = "\n🧾 Expense Summary:\n"
        result += "-----------------------------\n"
        for p, a, d in self.expenses:
            result += f"{p} paid ₹{a:.2f} for {d}\n"

        result += "\n💰 Final Balances:\n"
        for m, b in balances.items():
            if b > 0:
                result += f"{m} should RECEIVE ₹{b:.2f}\n"
            elif b < 0:
                result += f"{m} should PAY ₹{abs(b):.2f}\n"
            else:
                result += f"{m} is SETTLED UP.\n"

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)

    def show_chart(self):
        if not self.expenses:
            messagebox.showwarning("No Data", "Add some expenses first!")
            return

        payer_totals = {}
        for payer, amount, _ in self.expenses:
            payer_totals[payer] = payer_totals.get(payer, 0) + amount

        plt.figure(figsize=(6, 6))
        plt.pie(
            payer_totals.values(),
            labels=payer_totals.keys(),
            autopct="%1.1f%%",
            startangle=90,
            colors=plt.cm.Pastel1.colors
        )
        plt.title("💸 Spending Distribution")
        plt.show()

    def export_csv(self):
        if not self.expenses:
            messagebox.showwarning("No Data", "Nothing to export!")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not filepath:
            return

        with open(filepath, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Payer", "Amount (₹)", "Description"])
            for exp in self.expenses:
                writer.writerow(exp)

        messagebox.showinfo("Exported", f"Data exported successfully to:\n{filepath}")

# -------------------------
# Run the App
# -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseSplitterApp(root)
    root.mainloop()
