import tkinter as tk
from tkinter import messagebox


# Function to evaluate the expression
def click(event):
    current = entry.get()
    text = event.widget.cget("text")

    if text == "=":
        try:
            result = eval(current)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("Error", "Invalid Expression")
            entry.delete(0, tk.END)
    elif text == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, text)


# Create the main window
root = tk.Tk()
root.geometry("300x400")
root.title("Sweet Calculator 💖")

# Entry field
entry = tk.Entry(root, font="Arial 20")
entry.pack(fill=tk.BOTH, ipadx=8, pady=10, padx=10)

# Frame for buttons
frame = tk.Frame(root)
frame.pack()

# Button layout
buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', 'C', '=', '+']
]

# Create and place buttons
for row in buttons:
    row_frame = tk.Frame(frame)
    row_frame.pack()
    for btn_text in row:
        btn = tk.Button(row_frame, text=btn_text, font="Arial 18", padx=20, pady=20)
        btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        btn.bind("<Button-1>", click)

# Run the application
root.mainloop()