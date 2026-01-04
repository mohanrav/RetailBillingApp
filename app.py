import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import datetime
import json
import os
import tempfile
import platform

# -------------------- Auth --------------------
users = {
    "sales": {"password": "sales123", "role": "sales"},
    "manager": {"password": "manager123", "role": "manager"}
}

# -------------------- Storage --------------------
INVENTORY_FILE = "inventory.json"
SALES_FILE = "sales.json"

def load_inventory():
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_inventory(data):
    with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_sales():
    try:
        with open(SALES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_sales(data):
    with open(SALES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# -------------------- Reports UI --------------------
def show_reports_ui():
    for widget in root.winfo_children():
        widget.destroy()

    report_frame = tk.Frame(root)
    report_frame.pack(fill="both", expand=True, padx=12, pady=12)

    tk.Label(report_frame, text="Reports", font=("Arial", 16)).pack(pady=8)

    # Inventory Report
    tk.Label(report_frame, text="Inventory Report", font=("Arial", 12, "bold")).pack(anchor="w")
    inv_text = tk.Text(report_frame, width=100, height=10)
    inv_text.pack(pady=4, fill="x")
    inventory = load_inventory()
    if not inventory:
        inv_text.insert(tk.END, "No inventory items found.\n")
    else:
        for p in inventory:
            exp_status = ""
            if p.get("type") == "fruits" and p.get("expiry_date"):
                try:
                    exp_date = datetime.date.fromisoformat(p["expiry_date"])
                    if exp_date < datetime.date.today():
                        exp_status = " [EXPIRED]"
                except Exception:
                    exp_status = " [INVALID EXPIRY]"
            inv_text.insert(tk.END, f"{p.get('code')} - {p.get('type')} - ${p.get('price'):.2f} - MaxDisc {p.get('max_discount')}% - Expiry: {p.get('expiry_date')}{exp_status}\n")

    # Sales Report
    tk.Label(report_frame, text="Sales Report", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10,0))
    sales_text = tk.Text(report_frame, width=100, height=10)
    sales_text.pack(pady=4, fill="x")
    sales = load_sales()
    if not sales:
        sales_text.insert(tk.END, "No sales recorded yet.\n")
    else:
        for s in sales:
            sales_text.insert(tk.END, f"Date: {s.get('date')} | Items: {len(s.get('items', []))} | Total: ${s.get('total'):.2f}\n")
            for it in s.get("items", []):
                sales_text.insert(tk.END, f"  - {it.get('code')} x{it.get('qty')} = ${it.get('line_total'):.2f} (Disc {it.get('discount_applied')}%)\n")
            sales_text.insert(tk.END, "\n")

    btn_frame = tk.Frame(report_frame)
    btn_frame.pack(pady=8)
    tk.Button(btn_frame, text="Back to Inventory", command=show_inventory_ui).pack(side="left", padx=6)
    tk.Button(btn_frame, text="Back to Sales", command=show_sales_ui).pack(side="left", padx=6)

# -------------------- Inventory UI --------------------
def show_inventory_ui():
    for widget in root.winfo_children():
        widget.destroy()

    inv_frame = tk.Frame(root)
    inv_frame.pack(fill="both", expand=True, padx=12, pady=12)

    tk.Label(inv_frame, text="Inventory Management (Manager Only)", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

    # Product Code
    tk.Label(inv_frame, text="Product Code").grid(row=1, column=0, sticky="w")
    code_entry = tk.Entry(inv_frame)
    code_entry.grid(row=1, column=1, sticky="we")

    # Product Type
    tk.Label(inv_frame, text="Product Type").grid(row=2, column=0, sticky="w")
    type_var = tk.StringVar()
    type_dropdown = ttk.Combobox(inv_frame, textvariable=type_var, values=["tops", "shirt", "pants", "shorts", "shoes", "fruits"], state="readonly")
    type_dropdown.grid(row=2, column=1, sticky="we")

    # Price
    tk.Label(inv_frame, text="Price").grid(row=3, column=0, sticky="w")
    price_entry = tk.Entry(inv_frame)
    price_entry.grid(row=3, column=1, sticky="we")

    # Date Added
    tk.Label(inv_frame, text="Date Added").grid(row=4, column=0, sticky="w")
    date_added = tk.Entry(inv_frame)
    date_added.insert(0, datetime.date.today().isoformat())
    date_added.grid(row=4, column=1, sticky="we")

    # Expiry Date
    tk.Label(inv_frame, text="Expiry Date (for fruits)").grid(row=5, column=0, sticky="w")
    expiry_entry = tk.Entry(inv_frame)
    expiry_entry.grid(row=5, column=1, sticky="we")

    # Max Discount
    tk.Label(inv_frame, text="Max Discount (%)").grid(row=6, column=0, sticky="w")
    discount_entry = tk.Entry(inv_frame)
    discount_entry.grid(row=6, column=1, sticky="we")

    def save_product():
        code = code_entry.get().strip()
        ptype = type_var.get().strip()
        price = price_entry.get().strip()
        date_val = date_added.get().strip()
        expiry = expiry_entry.get().strip()
        discount = discount_entry.get().strip()

        if not code or not ptype or not price or not date_val or not discount:
            messagebox.showerror("Error", "All fields except expiry (non-fruits) are required")
            return

        try:
            price_val = float(price)
            discount_val = int(discount)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and discount must be an integer")
            return

        if ptype == "fruits":
            if not expiry:
                messagebox.showerror("Error", "Expiry date is required for fruits")
                return
            try:
                datetime.date.fromisoformat(expiry)
            except Exception:
                messagebox.showerror("Error", "Expiry date must be in YYYY-MM-DD format")
                return
        else:
            expiry = None

        inventory = load_inventory()
        for item in inventory:
            if item.get("code") == code:
                messagebox.showerror("Error", "Product code already exists")
                return

        product = {
            "code": code,
            "type": ptype,
            "price": price_val,
            "date_added": date_val,
            "expiry_date": expiry,
            "max_discount": discount_val
        }

        inventory.append(product)
        save_inventory(inventory)
        messagebox.showinfo("Success", f"Product {code} added successfully")

        code_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        expiry_entry.delete(0, tk.END)
        discount_entry.delete(0, tk.END)
        type_var.set("")

    tk.Button(inv_frame, text="Save Product", command=save_product).grid(row=7, column=0, columnspan=2, pady=10)
    tk.Button(inv_frame, text="Go to Sales", command=show_sales_ui).grid(row=8, column=0, columnspan=2, pady=4)
    tk.Button(inv_frame, text="View Reports", command=show_reports_ui).grid(row=9, column=0, columnspan=2, pady=4)

# -------------------- Sales UI --------------------
def show_sales_ui():
    for widget in root.winfo_children():
        widget.destroy()

    sales_frame = tk.Frame(root)
    sales_frame.pack(fill="both", expand=True, padx=12, pady=12)

    tk.Label(sales_frame, text="Sales UI", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=10, sticky="w")

    tk.Label(sales_frame, text="Product Code").grid(row=1, column=0, sticky="w")
    code_entry = tk.Entry(sales_frame)
    code_entry.grid(row=1, column=1, sticky="we")

    tk.Label(sales_frame, text="Quantity").grid(row=2, column=0, sticky="w")
    qty_entry = tk.Entry(sales_frame)
    qty_entry.grid(row=2, column=1, sticky="we")

    cart_list = tk.Listbox(sales_frame, width=80, height=10)
    cart_list.grid(row=4, column=0, columnspan=3, pady=10, sticky="we")

    total_label = tk.Label(sales_frame, text="Total: $0.00")
    total_label.grid(row=5, column=0, columnspan=3, sticky="w")

    tk.Label(sales_frame, text="Cash Given").grid(row=6, column=0, sticky="w")
    cash_entry = tk.Entry(sales_frame)
    cash_entry.grid(row=6, column=1, sticky="we")
    change_label = tk.Label(sales_frame, text="Change: $0.00")
    change_label.grid(row=6, column=2, sticky="w")

    cart = []
    total = 0.0

    def recalc_total():
        nonlocal total
        total = sum(item["line_total"] for item in cart)
        total_label.config(text=f"Total: ${total:.2f}")

    def refresh_cart_list():
        cart_list.delete(0, tk.END)
        for item in cart:
            p = item["product"]
            disc_txt = f" (Disc {item['discount_applied']}%)" if item["discount_applied"] else ""
            exp_txt = ""
            if p.get("type") == "fruits" and p.get("expiry_date"):
                try:
                    exp_date = datetime.date.fromisoformat(p["expiry_date"])
                    if exp_date < datetime.date.today():
                        exp_txt = " (Expired)"
                except Exception:
                    exp_txt = " (Invalid expiry)"
            cart_list.insert(tk.END, f"{p.get('code')} - {p.get('type')} x{item.get('qty')} = ${item.get('line_total'):.2f}{disc_txt}{exp_txt}")

    def add_to_cart():
        code = code_entry.get().strip()
        qty_str = qty_entry.get().strip()
        if not code or not qty_str:
            messagebox.showerror("Error", "Product code and quantity required")
            return
        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer")
            return

        inventory = load_inventory()
        product = next((p for p in inventory if p.get("code") == code), None)
        if not product:
            messagebox.showerror("Error", "Product not found")
            return

        # Expiry check for fruits
        if product.get("type") == "fruits" and product.get("expiry_date"):
            try:
                expiry = datetime.date.fromisoformat(product["expiry_date"])
                if expiry < datetime.date.today():
                    cont = messagebox.askyesno("Expired", "Item expired. Continue?")
                    if not cont:
                        return
            except Exception:
                cont = messagebox.askyesno("Expired", "Invalid expiry date format. Continue?")
                if not cont:
                    return

        line_total = float(product.get("price")) * qty
        cart.append({"product": product, "qty": qty, "line_total": line_total, "discount_applied": 0})
        refresh_cart_list()
        recalc_total()

        code_entry.delete(0, tk.END)
        qty_entry.delete(0, tk.END)

    def apply_discount():
        if not cart:
            messagebox.showerror("Error", "Cart is empty")
            return
        try:
            selection = cart_list.curselection()[0]
        except IndexError:
            messagebox.showerror("Error", "Select an item in the cart to apply discount")
            return
        item = cart[selection]
        product = item["product"]
        try:
            max_disc = int(product.get("max_discount", 0))
        except Exception:
            max_disc = 0
        disc = simpledialog.askinteger("Discount", f"Enter discount % (max {max_disc}%)", minvalue=0, maxvalue=max_disc)
        if disc is None:
            return
        discounted_price = float(product.get("price")) * (1 - disc / 100.0)
        item["line_total"] = discounted_price * item["qty"]
        item["discount_applied"] = disc
        refresh_cart_list()
        recalc_total()

    def pay():
        if not cart:
            messagebox.showerror("Error", "Cart is empty")
            return
        cash_str = cash_entry.get().strip()
        try:
            cash = float(cash_str)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid cash amount")
            return
        recalc_total()
        if cash < total:
            messagebox.showerror("Error", "Cash given is less than total")
            return
        change = cash - total
        change_label.config(text=f"Change: ${change:.2f}")
        # Log sale to sales.json
        sale = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": [],
            "total": total,
            "cash": cash,
            "change": change
        }
        for it in cart:
            p = it["product"]
            sale["items"].append({
                "code": p.get("code"),
                "type": p.get("type"),
                "qty": it.get("qty"),
                "price": float(p.get("price")),
                "discount_applied": it.get("discount_applied"),
                "line_total": it.get("line_total")
            })
        sales = load_sales()
        sales.append(sale)
        save_sales(sales)
        messagebox.showinfo("Payment", f"Payment successful.\nChange: ${change:.2f}")

    def manager_override():
        username = simpledialog.askstring("Manager Override", "Manager username:")
        password = simpledialog.askstring("Manager Override", "Manager password:", show="*")
        if not username or not password:
            return
        if username not in users or users[username]["password"] != password or users[username]["role"] != "manager":
            messagebox.showerror("Error", "Invalid manager credentials")
            return
        try:
            selection = cart_list.curselection()[0]
        except IndexError:
            messagebox.showerror("Error", "Select an item to void")
            return
        void_item = cart.pop(selection)
        refresh_cart_list()
        recalc_total()
        messagebox.showinfo("Override", f"Voided item {void_item['product'].get('code')}")

    def print_receipt():
        if not cart:
            messagebox.showerror("Error", "Cart is empty")
            return
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cash_str = cash_entry.get().strip()
        try:
            cash = float(cash_str) if cash_str else 0.0
        except Exception:
            cash = 0.0
        recalc_total()
        change = max(0.0, cash - total)
        lines = []
        lines.append("=== Receipt ===")
        lines.append(f"Date: {now}")
        lines.append("")
        for item in cart:
            p = item["product"]
            qty = item["qty"]
            price = float(p.get("price"))
            disc = item.get("discount_applied", 0)
            line_total = item.get("line_total")
            base = f"{p.get('code')} - {p.get('type')} x{qty} @ ${price:.2f}"
            if disc:
                base += f" (-{disc}%)"
            if p.get("type") == "fruits" and p.get("expiry_date"):
                try:
                    exp_date = datetime.date.fromisoformat(p.get("expiry_date"))
                    if exp_date < datetime.date.today():
                        base += " [Expired]"
                except Exception:
                    base += " [Invalid expiry]"
            base += f" = ${line_total:.2f}"
            lines.append(base)
        lines.append("")
        lines.append(f"Total: ${total:.2f}")
        lines.append(f"Cash: ${cash:.2f}")
        lines.append(f"Change: ${change:.2f}")
        lines.append("")
        lines.append("Thank you for shopping!")
        receipt_text = "\n".join(lines)

        if platform.system() == "Windows":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tmp:
                tmp.write(receipt_text)
                tmp_path = tmp.name
            try:
                os.startfile(tmp_path, "print")
                messagebox.showinfo("Print", "Receipt sent to printer dialog")
            except Exception as e:
                messagebox.showerror("Print Error", f"Failed to print: {e}")
        else:
            top = tk.Toplevel(root)
            top.title("Receipt")
            txt = tk.Text(top, width=80, height=20)
            txt.pack(fill="both", expand=True)
            txt.insert("1.0", receipt_text)

    def new_sale():
        # clear cart and UI
        show_sales_ui()

    def exit_app():
        root.destroy()

    tk.Button(sales_frame, text="Add to Cart", command=add_to_cart).grid(row=3, column=0, columnspan=3, pady=5, sticky="we")
    tk.Button(sales_frame, text="Apply Discount", command=apply_discount).grid(row=7, column=0, pady=5, sticky="we")
    tk.Button(sales_frame, text="Pay", command=pay).grid(row=7, column=1, pady=5, sticky="we")
    tk.Button(sales_frame, text="Manager Override", command=manager_override).grid(row=7, column=2, pady=5, sticky="we")
    tk.Button(sales_frame, text="Print Receipt", command=print_receipt).grid(row=8, column=0, pady=8, sticky="we")
    tk.Button(sales_frame, text="New Sale", command=new_sale).grid(row=8, column=1, pady=8, sticky="we")
    tk.Button(sales_frame, text="Exit", command=exit_app).grid(row=8, column=2, pady=8, sticky="we")
    tk.Button(sales_frame, text="Go to Inventory (Manager)", command=show_inventory_ui).grid(row=9, column=0, columnspan=3, pady=6, sticky="we")

# -------------------- Login --------------------
def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    if username in users and users[username]["password"] == password:
        role = users[username]["role"]
        if role == "manager":
            show_inventory_ui()
        else:
            show_sales_ui()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

# -------------------- Main Window --------------------
root = tk.Tk()
root.title("Retail Billing Demo")
root.geometry("900x640")

login_frame = tk.Frame(root)
login_frame.pack(expand=True)

tk.Label(login_frame, text="Username").pack(pady=5)
username_entry = tk.Entry(login_frame)
username_entry.pack()

tk.Label(login_frame, text="Password").pack(pady=5)
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack()

tk.Button(login_frame, text="Login", command=login).pack(pady=10)

root.mainloop()