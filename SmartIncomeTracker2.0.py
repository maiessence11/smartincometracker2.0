
import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

entries = []

def add_income():
    label = label_entry.get()
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid amount.")
        return

    deductions = 0
    try:
        if deduct_20_var.get():
            deductions += amount * 0.2
        if house_fee_entry.get():
            deductions += float(house_fee_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Invalid deduction or house fee.")
        return

    for e in extra_deductions:
        try:
            deductions += float(e.get())
        except ValueError:
            continue

    net = amount - deductions
    total_label.config(text=f"Net Income: ${net:.2f}")
    entries.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Label": label,
        "Gross": amount,
        "Deductions": deductions,
        "Net": net,
        "Notes": notes_entry.get()
    })
    label_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    notes_entry.delete(0, tk.END)

def save_to_csv():
    filename = "income_log.csv"
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Time", "Label", "Gross", "Deductions", "Net", "Notes"])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerows(entries)
    messagebox.showinfo("Saved", f"Data saved to {filename}")
    entries.clear()

root = tk.Tk()
root.title("Smart Income Tracker 2.0")
root.geometry("400x550")

tk.Label(root, text="Income Type (e.g. VIP, Stage, Token):").pack()
label_entry = tk.Entry(root)
label_entry.pack()

tk.Label(root, text="Amount Earned:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

deduct_20_var = tk.BooleanVar()
tk.Checkbutton(root, text="Apply 20% Club/Platform Cut", variable=deduct_20_var).pack()

tk.Label(root, text="House Fee (custom amount):").pack()
house_fee_entry = tk.Entry(root)
house_fee_entry.pack()

tk.Label(root, text="Extra Deductions (tip outs, rides, etc):").pack()
extra_deductions = []
for _ in range(3):
    e = tk.Entry(root)
    e.pack()
    extra_deductions.append(e)

tk.Label(root, text="Shift Notes (outfit, client, convo, etc):").pack()
notes_entry = tk.Entry(root)
notes_entry.pack()

tk.Button(root, text="Add Entry", command=add_income).pack(pady=5)
tk.Button(root, text="Save to Spreadsheet", command=save_to_csv).pack(pady=5)

total_label = tk.Label(root, text="Net Income: $0.00")
total_label.pack(pady=10)

root.mainloop()

