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
    tk.Label(
        report_frame,
        text="Inventory Report",
        font=("Arial", 12, "bold")
    ).pack(anchor="w")

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
            inv_text.insert(
                tk.END,
                f"{p.get('code')} - {p.get('type')} - "
                f"${p.get('price'):.2f} - MaxDisc {p.get('max_discount')}% - "
                f"Expiry: {p.get('expiry_date')}{exp_status}\n"
            )

    # Sales / Returns Report
    tk.Label(
        report_frame,
        text="Sales & Returns Report",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", pady=(10, 0))

    sales_text = tk.Text(report_frame, width=100, height=10)
    sales_text.pack(pady=4, fill="x")

    sales = load_sales()
    if not sales:
        sales_text.insert(tk.END, "No sales recorded yet.\n")
    else:
        for s in sales:
            entry_type = s.get("type", "sale")
            if entry_type == "sale":
                sale_id = s.get("sale_id", "N/A")
                tender = s.get("tender", {})
                method = tender.get("method", "cash")
                last4 = tender.get("last4", "")
                tender_desc = method
                if method == "card" and last4:
                    tender_desc += f" (****{last4})"
                sales_text.insert(
                    tk.END,
                    f"[SALE] ID: {sale_id} | Date: {s.get('date')} | "
                    f"Items: {len(s.get('items', []))} | "
                    f"Total: ${s.get('total', 0.0):.2f} | Tender: {tender_desc}\n"
                )
                for it in s.get("items", []):
                    sales_text.insert(
                        tk.END,
                        f"  - {it.get('code')} x{it.get('qty')} = "
                        f"${it.get('line_total', 0.0):.2f} "
                        f"(Disc {it.get('discount_applied', 0)}%)\n"
                    )
                sales_text.insert(tk.END, "\n")

            elif entry_type == "return":
                return_id = s.get("return_id", "N/A")
                original_id = s.get("original_sale_id", "N/A")
                total_refund = s.get("total_refund", 0.0)
                sales_text.insert(
                    tk.END,
                    f"[RETURN] ID: {return_id} | Orig Sale: {original_id} | "
                    f"Date: {s.get('date')} | Refund: ${total_refund:.2f}\n"
                )
                for it in s.get("items", []):
                    sales_text.insert(
                        tk.END,
                        f"  - {it.get('code')} x{it.get('qty')} -> "
                        f"Refund ${it.get('refund_amount', 0.0):.2f}\n"
                    )
                sales_text.insert(tk.END, "\n")

    btn_frame = tk.Frame(report_frame)
    btn_frame.pack(pady=8)
    tk.Button(btn_frame, text="Back to Inventory", command=show_inventory_ui).pack(
        side="left", padx=6
    )
    tk.Button(btn_frame, text="Back to Sales", command=show_sales_ui).pack(
        side="left", padx=6
    )


# -------------------- Inventory UI --------------------
def show_inventory_ui():
    for widget in root.winfo_children():
        widget.destroy()

    inv_frame = tk.Frame(root)
    inv_frame.pack(fill="both", expand=True, padx=12, pady=12)

    tk.Label(
        inv_frame,
        text="Inventory Management (Manager Only)",
        font=("Arial", 14)
    ).grid(row=0, column=0, columnspan=2, pady=10)

    # Product Code
    tk.Label(inv_frame, text="Product Code").grid(row=1, column=0, sticky="w")
    code_entry = tk.Entry(inv_frame)
    code_entry.grid(row=1, column=1, sticky="we")

    # Product Type
    tk.Label(inv_frame, text="Product Type").grid(row=2, column=0, sticky="w")
    type_var = tk.StringVar()
    type_dropdown = ttk.Combobox(
        inv_frame,
        textvariable=type_var,
        values=["tops", "shirt", "pants", "shorts", "shoes", "fruits"],
        state="readonly"
    )
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
            messagebox.showerror(
                "Error",
                "All fields except expiry (non-fruits) are required"
            )
            return

        try:
            price_val = float(price)
            discount_val = int(discount)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Price must be a number and discount must be an integer"
            )
            return

        if ptype == "fruits":
            if not expiry:
                messagebox.showerror(
                    "Error",
                    "Expiry date is required for fruits"
                )
                return
            try:
                datetime.date.fromisoformat(expiry)
            except Exception:
                messagebox.showerror(
                    "Error",
                    "Expiry date must be in YYYY-MM-DD format"
                )
                return
        else:
            expiry = None

        inventory = load_inventory()
        for item in inventory:
            if item.get("code") == code:
                messagebox.showerror(
                    "Error",
                    "Product code already exists"
                )
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

    tk.Button(inv_frame, text="Save Product", command=save_product).grid(
        row=7, column=0, columnspan=2, pady=10
    )
    tk.Button(inv_frame, text="Go to Sales", command=show_sales_ui).grid(
        row=8, column=0, columnspan=2, pady=4
    )
    tk.Button(inv_frame, text="View Reports", command=show_reports_ui).grid(
        row=9, column=0, columnspan=2, pady=4
    )


# -------------------- Sales UI --------------------
def show_sales_ui():
    for widget in root.winfo_children():
        widget.destroy()

    sales_frame = tk.Frame(root)
    sales_frame.pack(fill="both", expand=True, padx=12, pady=12)

    tk.Label(sales_frame, text="Sales UI", font=("Arial", 14)).grid(
        row=0, column=0, columnspan=3, pady=10, sticky="w"
    )

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

    # Payment method
    tk.Label(sales_frame, text="Payment Method").grid(row=7, column=0, sticky="w")
    payment_var = tk.StringVar(value="cash")
    payment_dropdown = ttk.Combobox(
        sales_frame,
        textvariable=payment_var,
        values=["cash", "card"],
        state="readonly"
    )
    payment_dropdown.grid(row=7, column=1, sticky="we")

    # Card last 4 digits
    tk.Label(sales_frame, text="Card Last 4 (if card)").grid(row=8, column=0, sticky="w")
    card_entry = tk.Entry(sales_frame)
    card_entry.grid(row=8, column=1, sticky="we")

    cart = []
    total = 0.0
        # ---------------------------------------------------------
    # RIGHT-SIDE PRODUCT REFERENCE TABLE
    # ---------------------------------------------------------
    right_frame = tk.Frame(sales_frame)
    right_frame.grid(row=0, column=4, rowspan=20, padx=20, sticky="ns")

    tk.Label(right_frame, text="Product Reference", font=("Arial", 12, "bold")).pack(pady=5)

    ref_table = ttk.Treeview(right_frame, columns=("code", "type"), show="headings", height=20)
    ref_table.heading("code", text="Code")
    ref_table.heading("type", text="Type")
    ref_table.column("code", width=80, anchor="center")
    ref_table.column("type", width=120, anchor="center")
    ref_table.pack(fill="y", expand=True)

    # Load inventory and populate table
    inventory = load_inventory()
    for item in inventory:
        ref_table.insert("", tk.END, values=(item.get("code"), item.get("type")))
    def recalc_total():
        nonlocal total
        total = sum(item["line_total"] for item in cart)
        total_label.config(text=f"Total: ${total:.2f}")

    def refresh_cart_list():
        cart_list.delete(0, tk.END)
        for item in cart:
            p = item["product"]
            disc_txt = (
                f" (Disc {item['discount_applied']}%)"
                if item["discount_applied"] else ""
            )
            exp_txt = ""
            if p.get("type") == "fruits" and p.get("expiry_date"):
                try:
                    exp_date = datetime.date.fromisoformat(p["expiry_date"])
                    if exp_date < datetime.date.today():
                        exp_txt = " (Expired)"
                except Exception:
                    exp_txt = " (Invalid expiry)"
            cart_list.insert(
                tk.END,
                f"{p.get('code')} - {p.get('type')} "
                f"x{item.get('qty')} = ${item.get('line_total'):.2f}"
                f"{disc_txt}{exp_txt}"
            )

    def add_to_cart():
        code = code_entry.get().strip()
        qty_str = qty_entry.get().strip()

        if not code or not qty_str:
            messagebox.showerror(
                "Error",
                "Product code and quantity required"
            )
            return

        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror(
                "Error",
                "Quantity must be a positive integer"
            )
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
                    cont = messagebox.askyesno(
                        "Expired",
                        "Item expired. Continue?"
                    )
                    if not cont:
                        return
            except Exception:
                cont = messagebox.askyesno(
                    "Expired",
                    "Invalid expiry date format. Continue?"
                )
                if not cont:
                    return

        line_total = float(product.get("price")) * qty
        cart.append({
            "product": product,
            "qty": qty,
            "line_total": line_total,
            "discount_applied": 0
        })
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
            messagebox.showerror(
                "Error",
                "Select an item in the cart to apply discount"
            )
            return

        item = cart[selection]
        product = item["product"]
        try:
            max_disc = int(product.get("max_discount", 0))
        except Exception:
            max_disc = 0

        disc = simpledialog.askinteger(
            "Discount",
            f"Enter discount % (max {max_disc}%)",
            minvalue=0,
            maxvalue=max_disc
        )
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

        method = payment_var.get()

        # Recalculate total before payment
        recalc_total()

        # Cash payment
        if method == "cash":
            cash_str = cash_entry.get().strip()
            try:
                cash = float(cash_str)
            except ValueError:
                messagebox.showerror("Error", "Enter a valid cash amount")
                return
            if cash < total:
                messagebox.showerror(
                    "Error",
                    "Cash given is less than total"
                )
                return
            change = cash - total
            change_label.config(text=f"Change: ${change:.2f}")
            tender_info = {
                "method": "cash",
                "cash_given": cash,
                "change": change
            }

        # Card payment
        else:
            last4 = card_entry.get().strip()
            if len(last4) != 4 or not last4.isdigit():
                messagebox.showerror(
                    "Error",
                    "Enter last 4 digits of card"
                )
                return
            change = 0.0
            change_label.config(text=f"Change: ${change:.2f}")
            card_token = (
                f"CARD-{last4}-"
                f"{datetime.datetime.now().strftime('%H%M%S')}"
            )
            tender_info = {
                "method": "card",
                "last4": last4,
                "card_token": card_token
            }

        # Generate sale ID (Receipt ID)
        sale_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        sale = {
            "type": "sale",
            "sale_id": sale_id,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": [],
            "total": total,
            "tender": tender_info
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

        messagebox.showinfo(
            "Payment",
            f"Payment successful.\n"
            f"Receipt ID: {sale_id}\n"
            f"Change: ${tender_info.get('change', 0.0):.2f}"
        )

    def manager_override():
        username = simpledialog.askstring(
            "Manager Override",
            "Manager username:"
        )
        password = simpledialog.askstring(
            "Manager Override",
            "Manager password:",
            show="*"
        )

        if not username or not password:
            return

        if (
            username not in users
            or users[username]["password"] != password
            or users[username]["role"] != "manager"
        ):
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
        messagebox.showinfo(
            "Override",
            f"Voided item {void_item['product'].get('code')}"
        )

    def print_receipt():
        if not cart:
            messagebox.showerror("Error", "Cart is empty")
            return

        # Try to show the last sale's receipt ID and tender
        sales = load_sales()
        if sales and sales[-1].get("type", "sale") == "sale":
            last_sale = sales[-1]
            sale_id = last_sale.get("sale_id", "N/A")
            tender = last_sale.get("tender", {})
            method = tender.get("method", "cash")
            last4 = tender.get("last4", "")
            tender_desc = method
            if method == "card" and last4:
                tender_desc += f" (****{last4})"
        else:
            sale_id = "N/A"
            tender_desc = "N/A"

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
        lines.append(f"Receipt ID: {sale_id}")
        lines.append(f"Tender: {tender_desc}")
        lines.append("")

        for item in cart:
            p = item["product"]
            qty = item["qty"]
            price = float(p.get("price"))
            disc = item.get("discount_applied", 0)
            line_total = item.get("line_total")
            base = (
                f"{p.get('code')} - {p.get('type')} "
                f"x{qty} @ ${price:.2f}"
            )
            if disc:
                base += f" (-{disc}%)"
            if p.get("type") == "fruits" and p.get("expiry_date"):
                try:
                    exp_date = datetime.date.fromisoformat(
                        p.get("expiry_date")
                    )
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
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".txt",
                mode="w",
                encoding="utf-8"
            ) as tmp:
                tmp.write(receipt_text)
                tmp_path = tmp.name
            try:
                os.startfile(tmp_path, "print")
                messagebox.showinfo(
                    "Print",
                    "Receipt sent to printer dialog"
                )
            except Exception as e:
                messagebox.showerror("Print Error", f"Failed to print: {e}")
        else:
            top = tk.Toplevel(root)
            top.title("Receipt")
            txt = tk.Text(top, width=80, height=20)
            txt.pack(fill="both", expand=True)
            txt.insert("1.0", receipt_text)

        def new_sale():
            show_sales_ui()

    def new_sale():
        show_sales_ui()

    def exit_app():
        root.destroy()

    tk.Button(
        sales_frame,
        text="Add to Cart",
        command=add_to_cart
    ).grid(row=3, column=0, columnspan=3, pady=5, sticky="we")

    tk.Button(
        sales_frame,
        text="Apply Discount",
        command=apply_discount
    ).grid(row=9, column=0, pady=5, sticky="we")

    tk.Button(
        sales_frame,
        text="Pay",
        command=pay
    ).grid(row=9, column=1, pady=5, sticky="we")

    tk.Button(
        sales_frame,
        text="Manager Override",
        command=manager_override
    ).grid(row=9, column=2, pady=5, sticky="we")

    tk.Button(
        sales_frame,
        text="Print Receipt",
        command=print_receipt
    ).grid(row=10, column=0, pady=8, sticky="we")

    tk.Button(
        sales_frame,
        text="New Sale",
        command=new_sale
    ).grid(row=10, column=1, pady=8, sticky="we")

    tk.Button(
        sales_frame,
        text="Exit",
        command=exit_app
    ).grid(row=10, column=2, pady=8, sticky="we")

    # ---------------- Manager-secured Inventory Access ----------------
    def go_to_inventory_secure():
        username = simpledialog.askstring("Manager Login", "Manager username:")
        password = simpledialog.askstring("Manager Login", "Manager password:", show="*")

        if (
            username in users
            and users[username]["password"] == password
            and users[username]["role"] == "manager"
        ):
            show_inventory_ui()
        else:
            messagebox.showerror("Access Denied", "Manager credentials required")

    tk.Button(
        sales_frame,
        text="Go to Inventory (Manager)",
        command=go_to_inventory_secure
    ).grid(row=11, column=0, columnspan=3, pady=6, sticky="we")

    tk.Button(
        sales_frame,
        text="Returns",
        command=show_returns_ui
    ).grid(row=12, column=0, columnspan=3, pady=6, sticky="we")

    # -------------------- Returns UI --------------------
def show_returns_ui():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=12, pady=12)

    tk.Label(frame, text="Returns", font=("Arial", 14)).grid(
        row=0, column=0, columnspan=3, pady=10, sticky="w"
    )

    tk.Label(frame, text="Receipt ID").grid(row=1, column=0, sticky="w")
    receipt_entry = tk.Entry(frame)
    receipt_entry.grid(row=1, column=1, sticky="we", columnspan=2)

    tk.Label(frame, text="Card Last 4 (optional)").grid(row=2, column=0, sticky="w")
    card_lookup_entry = tk.Entry(frame)
    card_lookup_entry.grid(row=2, column=1, sticky="we", columnspan=2)

    sales_list = tk.Listbox(frame, width=80, height=8)
    sales_list.grid(row=3, column=0, columnspan=3, pady=10, sticky="we")

    tk.Label(frame, text="Return Quantity").grid(row=4, column=0, sticky="w")
    qty_entry = tk.Entry(frame)
    qty_entry.grid(row=4, column=1, sticky="we")

    refund_label = tk.Label(frame, text="Refund: $0.00")
    refund_label.grid(row=5, column=0, columnspan=3, sticky="w")

    return_cart = []
    refund_total = 0.0
    original_sale = None

    def load_sale():
        nonlocal original_sale, return_cart, refund_total

        receipt_id = receipt_entry.get().strip()
        card_last4 = card_lookup_entry.get().strip()

        sales = load_sales()

        # 1. Lookup by Receipt ID
        if receipt_id:
            original_sale = next(
                (
                    s
                    for s in sales
                    if s.get("type", "sale") == "sale"
                    and s.get("sale_id") == receipt_id
                ),
                None
            )
        # 2. Lookup by Card Last 4
        elif card_last4:
            original_sale = next(
                (
                    s
                    for s in sales
                    if s.get("type", "sale") == "sale"
                    and s.get("tender", {}).get("method") == "card"
                    and s.get("tender", {}).get("last4") == card_last4
                ),
                None
            )
        else:
            messagebox.showerror(
                "Error",
                "Enter Receipt ID or Card Last 4"
            )
            return

        if not original_sale:
            messagebox.showerror("Error", "Sale not found")
            return

        # Enforce a 30-day return window
        try:
            sale_date = datetime.datetime.strptime(
                original_sale["date"], "%Y-%m-%d %H:%M:%S"
            ).date()
            if (datetime.date.today() - sale_date).days > 30:
                messagebox.showerror(
                    "Error",
                    "Return window (30 days) has expired"
                )
                original_sale = None
                return
        except Exception:
            # If date parsing fails, allow for now
            pass

        sales_list.delete(0, tk.END)
        return_cart = []
        refund_total = 0.0
        refund_label.config(text="Refund: $0.00")

        for idx, item in enumerate(original_sale.get("items", [])):
            line = (
                f"{idx+1}. {item.get('code')} - {item.get('type')} "
                f"x{item.get('qty')} @ ${item.get('price'):.2f} "
                f"(Disc {item.get('discount_applied', 0)}%) "
                f"= ${item.get('line_total', 0.0):.2f}"
            )
            sales_list.insert(tk.END, line)

    def add_return_item():
        nonlocal refund_total
        if not original_sale:
            messagebox.showerror("Error", "Load a sale first")
            return

        try:
            selection = sales_list.curselection()[0]
        except IndexError:
            messagebox.showerror(
                "Error",
                "Select an item to return"
            )
            return

        qty_str = qty_entry.get().strip()
        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror(
                "Error",
                "Return quantity must be a positive integer"
            )
            return

        item = original_sale["items"][selection]
        sold_qty = item.get("qty", 0)

        if qty > sold_qty:
            messagebox.showerror(
                "Error",
                f"Cannot return more than sold quantity ({sold_qty})"
            )
            return

        line_total = float(item.get("line_total", 0.0))
        per_unit = line_total / sold_qty if sold_qty else 0.0
        this_refund = per_unit * qty

        return_cart.append({
            "code": item.get("code"),
            "qty": qty,
            "refund_amount": this_refund
        })
        refund_total += this_refund
        refund_label.config(text=f"Refund: ${refund_total:.2f}")
        qty_entry.delete(0, tk.END)

    def process_return():
        nonlocal refund_total
        if not original_sale:
            messagebox.showerror("Error", "Load a sale first")
            return
        if not return_cart:
            messagebox.showerror("Error", "No items selected for return")
            return

        return_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return_tx = {
            "type": "return",
            "return_id": return_id,
            "original_sale_id": original_sale.get("sale_id"),
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": return_cart,
            "total_refund": refund_total
        }

        sales = load_sales()
        sales.append(return_tx)
        save_sales(sales)

        messagebox.showinfo(
            "Return processed",
            f"Return ID: {return_id}\n"
            f"Refund amount: ${refund_total:.2f}\n"
            "Issue refund as per store policy (cash/card/store credit)."
        )

        # Reset UI
        receipt_entry.delete(0, tk.END)
        card_lookup_entry.delete(0, tk.END)
        sales_list.delete(0, tk.END)
        qty_entry.delete(0, tk.END)
        refund_total = 0.0
        refund_label.config(text="Refund: $0.00")

    def back_to_sales():
        show_sales_ui()

    tk.Button(frame, text="Load Sale", command=load_sale).grid(
        row=6, column=0, pady=5, sticky="we"
    )
    tk.Button(frame, text="Add Return Item", command=add_return_item).grid(
        row=4, column=2, pady=5, sticky="we"
    )
    tk.Button(frame, text="Process Return", command=process_return).grid(
        row=7, column=0, columnspan=3, pady=10, sticky="we"
    )
    tk.Button(frame, text="Back to Sales", command=back_to_sales).grid(
        row=8, column=0, columnspan=3, pady=6, sticky="we"
    )


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
root.geometry("900x700")

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