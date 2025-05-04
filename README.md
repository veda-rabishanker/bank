# TEXAS VEDA FINANCIAL

Texas Veda Financial is a simple banking system that allows users to manage their accounts securely. This project is built using Flask and SQLite, providing a web-based interface for users to perform essential banking operations.

---

## **Features**

### **For Users**
- **Login**: Users can log in using their account number and PIN.
- **Check Balance**: View the current balance of their account.
- **Deposit Money**: Add funds to their account.
- **Withdraw Money**: Withdraw funds from their account (if sufficient balance is available).
- **Close Account**: Permanently close their account (with confirmation).

### **For Administrators**
- **Create New Accounts**: Add new users to the system.
- **Modify Account Details**: Update user information such as name, email, or phone number.
- **Close Accounts**: Remove accounts from the system.

---

## **Technologies Used**
- **Backend**: Flask (Python)
- **Database**: SQLite (via SQLAlchemy ORM)
- **Frontend**: HTML, CSS (for styling)
- **Testing**: Python's `unittest` (optional)

---

## **Setup and Installation**

### **Prerequisites**
- Python 3.8 or higher installed on your system.
- `pip` (Python package manager) installed.

### **Steps to Run the Project**
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
2. **Import Files**:
    ```bash
   pip install flask_sqlalchemy
3. **Run the Repository**:
    ```bash
   python app.py