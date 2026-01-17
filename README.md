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
# 🧾 **Returns Feature — Documentation**

## 📌 Overview  
The **Returns Feature** simulates a realistic retail return workflow modeled after stores like Five Below.  
It supports:

- Receipt‑based returns  
- Card‑based returns (using last 4 digits)  
- Partial returns  
- Refund calculation based on original sale price and discounts  
- 30‑day return window  
- Full audit logging into `sales.json`  
- Manager‑secured inventory access (optional)

This feature is designed to mimic real POS behavior while remaining simple enough for local testing and demos.

---

## 🛒 **How Returns Work**

### 1. **Locate the Original Transaction**
The system allows two lookup methods:

#### **A. Receipt ID Lookup**
The user enters a valid receipt ID.  
The system searches `sales.json` for a matching transaction and loads:

- Items purchased  
- Quantities  
- Prices  
- Discounts  
- Payment method  
- Card last‑4 (if applicable)

#### **B. Card Last‑4 Lookup**
If the customer does not have a receipt, the system can search by:

- Last 4 digits of the card  
- Date range (optional)  
- Most recent matching transaction

This simulates real retail fallback behavior.

---

## 🔍 **Selecting Items to Return**
Once the original sale is loaded, the UI displays:

- Each item purchased  
- Quantity purchased  
- Quantity eligible for return  
- Price and discount applied at the time of sale  

The user can select:

- **Full return** of an item  
- **Partial return** (e.g., return 1 out of 3 items)

The system prevents:

- Returning more items than originally purchased  
- Returning items already returned in a previous session  

This ensures audit integrity.

---

## 💰 **Refund Calculation**
Refunds are calculated using the **original sale price**, not current price.

Refund =  
\[
\text{(Original Price - Discount)} \times \text{Quantity Returned}
\]

This matches real retail policy.

### Refund Method
Refunds are issued using the **same payment method** as the original sale:

- **Cash sale → Cash refund**  
- **Card sale → Refund to same card (simulated using last‑4)**  

This prevents fraud and maintains consistency.

---

## ⏳ **30‑Day Return Window**
The system checks the sale date stored in `sales.json`.

If the sale is older than 30 days:

- The return is blocked  
- A message is shown:  
  **“Return window expired — returns allowed only within 30 days.”**

This matches common retail policy.

---

## 🧾 **Audit Logging**
Every return is appended to `sales.json` with:

- Return timestamp  
- Receipt ID  
- Items returned  
- Quantity returned  
- Refund amount  
- Payment method  
- Card last‑4 (if applicable)  
- Reference to original sale  

This creates a complete audit trail for compliance and debugging.

---

## 🔐 **Manager Override **
If the user attempts to access inventory or perform restricted actions, the system prompts for:

- Manager username  
- Manager password  

This prevents unauthorized access by sales associates.

---

## 🖥️ **UI Flow Summary**
1. User opens **Returns UI**  
2. Enters **Receipt ID** or **Card Last‑4**  
3. System loads matching sale  
4. User selects items to return  
5. System validates quantities + return window  
6. Refund is calculated  
7. Refund is issued (cash or card)  
8. Return is logged in `sales.json`  
9. Inventory is updated (optional)

---

## 📂 **Files Involved**
| File | Purpose |
|------|---------|
| `AppReturnsFeature.py` | Main UI + return logic |
| `sales.json` | Stores all sales + return audit logs |
| `inventory.json` | Tracks stock levels (optional for returns) |

---

## 🧪 **Testing the Returns Feature**
To test:

1. Perform a sale in the Sales UI  
2. Note the generated **Receipt ID**  
3. Open **Returns UI**  
4. Enter the Receipt ID  
5. Select items to return  
6. Verify refund calculation  
7. Check `sales.json` for the new return entry  

---

## 🏁 **Summary**
This Returns Feature provides a realistic, fraud‑resistant, audit‑ready return workflow suitable for:

- POS demos  
- Retail simulations  
- Training environments  
- Python learning projects  

It mirrors real store behavior while remaining simple and transparent.
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

## 📌 Future Enhancements (Returns Feature)
Not added in this release. See AppReturnsfeature.py or Appreturnsfeature branch.

---



---

##  Author
Mohan Ravindran

