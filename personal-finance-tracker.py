import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import csv
from datetime import datetime

class FinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("💖 Personal Finance Tracker")
        self.root.geometry("600x600")
        self.root.config(bg="#fff7fa")

        self.transactions = []  # (type, category, amount, date)

        # 🌸 Title
        tk.Label(root, text="💸 Personal Finance Tracker", font=("Arial", 18, "bold"), bg="#fff7fa", fg="#e75480").pack(pady=10)

        # 🧾 Frame for adding transactions
        frame = tk.LabelFrame(root, text="Add Transaction", font=("Arial", 12, "bold"), bg="#fff7fa", fg="#d63384")
        frame.pack(pady=10, padx=10, fill="x")

        tk.Label(frame, text="Type:", bg="#fff7fa").grid(row=0, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar(value="Income")
        ttk.Combobox(frame, textvariable=self.type_var, values=["Income", "Expense"], state="readonly", width=15).grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Category:", bg="#fff7fa").grid(row=0, column=2, padx=5)
        self.category_entry = tk.Entry(frame, width=15)
        self.category_entry.grid(row=0, column=3, padx=5)

        tk.Label(frame, text="Amount (₹):", bg="#fff7fa").grid(row=1, column=0, padx=5)
        self.amount_entry = tk.Entry(frame, width=15)
        self.amount_entry.grid(row=1, column=1, padx=5)

        tk.Button(frame, text="➕ Add", bg="#b9fbc0", command=self.add_transaction).grid(row=1, column=3, padx=5)

        # 📋 Transaction List
        columns = ("Type", "Category", "Amount", "Date")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        # 📊 Buttons Frame
        btn_frame = tk.Frame(root, bg="#fff7fa")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="📈 Show Chart", command=self.show_chart, bg="#c1f0f6", width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="💾 Export CSV", command=self.export_csv, bg="#d7bde2", width=15).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="📊 Summary", command=self.show_summary, bg="#ffecb3", width=15).grid(row=0, column=2, padx=5)

        # 💰 Summary Label
        self.summary_label = tk.Label(root, text="", bg="#fff7fa", font=("Arial", 11, "bold"))
        self.summary_label.pack(pady=10)

    def add_transaction(self):
        t_type = self.type_var.get()
        category = self.category_entry.get().strip()
        amount = self.amount_entry.get().strip()

        if not category or not amount:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered!")
            return

        date = datetime.now().strftime("%d-%m-%Y")
        self.transactions.append((t_type, category, amount, date))
        self.tree.insert("", "end", values=(t_type, category, f"₹{amount:.2f}", date))

        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.update_summary()

    def update_summary(self):
        income = sum(a for t, _, a, _ in self.transactions if t == "Income")
        expense = sum(a for t, _, a, _ in self.transactions if t == "Expense")
        balance = income - expense
        self.summary_label.config(
            text=f"Total Income: ₹{income:.2f} | Total Expense: ₹{expense:.2f} | Balance: ₹{balance:.2f}"
        )

    def show_chart(self):
        if not self.transactions:
            messagebox.showinfo("Info", "No transactions yet!")
            return

        income_by_cat = {}
        expense_by_cat = {}

        for t_type, cat, amt, _ in self.transactions:
            if t_type == "Income":
                income_by_cat[cat] = income_by_cat.get(cat, 0) + amt
            else:
                expense_by_cat[cat] = expense_by_cat.get(cat, 0) + amt

        plt.figure(figsize=(6, 5))
        plt.subplot(1, 2, 1)
        plt.title("Income by Category")
        plt.pie(income_by_cat.values(), labels=income_by_cat.keys(), autopct="%1.1f%%", colors=plt.cm.Pastel1.colors)

        plt.subplot(1, 2, 2)
        plt.title("Expense by Category")
        plt.pie(expense_by_cat.values(), labels=expense_by_cat.keys(), autopct="%1.1f%%", colors=plt.cm.Pastel2.colors)

        plt.tight_layout()
        plt.show()

    def export_csv(self):
        if not self.transactions:
            messagebox.showwarning("No Data", "Nothing to export!")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not filepath:
            return
        with open(filepath, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Category", "Amount (₹)", "Date"])
            for row in self.transactions:
                writer.writerow(row)
        messagebox.showinfo("Exported", f"Transactions saved to:\n{filepath}")

    def show_summary(self):
        if not self.transactions:
            messagebox.showinfo("Info", "No transactions added yet!")
            return

        income = sum(a for t, _, a, _ in self.transactions if t == "Income")
        expense = sum(a for t, _, a, _ in self.transactions if t == "Expense")
        balance = income - expense

        messagebox.showinfo("💰 Finance Summary", f"Total Income: ₹{income:.2f}\nTotal Expense: ₹{expense:.2f}\nBalance: ₹{balance:.2f}")

# -------------------------
# Run the App
# -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTracker(root)
    root.mainloop()
