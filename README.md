# RetailBillingApp
This is a retail billing App built for test purposes by Mohan Ravindran . It is a personal project with no associations to Organizations. 

## Overview
This project is a **Retail Billing & Inventory Management System** built using **Python** and **Tkinter**.  
It provides a complete workflow for small retail stores, including:

- Inventory management (manager only)
- Sales processing (sales associate)
- Expiry validation for fruits
- Discounts with max‑discount enforcement
- Manager override for voiding items
- Receipt printing
- Persistent sales logging
- Reporting (Inventory Report + Sales Report)

The application is lightweight, file‑based, and requires no external database.

---

##  Features

###  **User Login**
Two roles are supported:
- **Sales** → Access to Sales UI only  
- **Manager** → Access to Inventory, Reports, and Sales UI  

Credentials are defined in `app.py`.

---

###  **Inventory Management (Manager Only)**
Managers can:
- Add new products  
- Set product type  
- Set price  
- Set max discount  
- Set expiry date (required for fruits)  
- Prevent duplicate product codes  

Inventory is stored in:

```
inventory.json
```

---

###  **Sales UI**
Sales associates can:
- Add items to cart using product code
- Enter quantity
- Automatically validate expiry for fruits
- Apply discounts (within allowed max)
- Process payments (cash)
- View change due
- Print receipts
- Start new sale
- Request manager override to void items

---

### **Receipt Printing**
Receipts include:
- Date/time  
- Items purchased  
- Discounts applied  
- Expiry warnings (if applicable)  
- Total, cash received, change  

On Windows, receipts are sent to the system print dialog.

---

### 📊 **Reports Module**
Managers can view:

#### **Inventory Report**
- All products  
- Prices  
- Max discounts  
- Expiry dates  
- Expired fruit items highlighted  

#### **Sales Report**
- All completed sales  
- Items sold  
- Discounts applied  
- Total revenue per sale  

Sales are stored in:

```
sales.json
```

---

## 🗂️ Project Structure

```
Dailysalestrackerv2/
│
├── app.py               # Main application
├── inventory.json       # Inventory storage
├── sales.json           # Sales history storage
├── README.md            # Documentation
└── .github/workflows/   # (Optional) CI workflows
```

---

## Installation & Setup

### **1. Install Python**
Python 3.8+ is recommended.

### **2. Install Tkinter**
Tkinter comes preinstalled on:
- Windows  
- macOS  

On Linux (Ubuntu/Debian):

```
sudo apt install python3-tk
```

### **3. Run the application**

```
python app.py
```

---

## 🧪 Testing the Application

### **Login**
- Manager: `manager / manager123`
- Sales: `sales / sales123`

### **Inventory**
- Add a fruit → must enter expiry date  
- Add a non‑fruit → expiry ignored  
- Duplicate product code → blocked  

### **Sales**
- Add expired fruit → prompts user  
- Apply discount → enforces max discount  
- Pay → logs sale to `sales.json`  
- Print receipt → opens print dialog  

### **Reports**
- Inventory report shows all items  
- Sales report shows all completed transactions  

---

## 📁 Data Files

### **inventory.json**
Stores all products added by the manager.

### **sales.json**
Stores every completed sale, including:
- Items
- Discounts
- Totals
- Cash received
- Change
- Timestamp

These files act as a lightweight database.

---

## 🧱 Tech Stack

- **Python 3**
- **Tkinter** (GUI)
- **JSON** (data persistence)
- **os / tempfile / platform** (receipt printing)

---

## 📌 Future Enhancements (Optional)
To be decided

---

## 🙌 Author
Mohan Ravindran

