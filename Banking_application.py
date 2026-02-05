import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import os
from datetime import datetime
import json


# ---------------- BANK ACCOUNT CLASS ----------------
class BankAccount:
    def __init__(self, name, password, accountNo, balance=0, loan=0, is_new=True):
        self.name = name
        self.__password = password
        self.accountNo = accountNo
        self.balance = balance
        self.loan = loan
        self.is_new = is_new
        self.transaction_history = []

        self.passbook_file = f"passbook_{self.accountNo}.txt"
        self.data_file = f"account_{self.accountNo}.json"

        if not os.path.exists(self.passbook_file):
            with open(self.passbook_file, "w") as f:
                f.write(f"{'='*60}\n")
                f.write(f"  BLUEWAVE BANK - PASSBOOK\n")
                f.write(f"  Account Holder: {self.name}\n")
                f.write(f"  Account Number: {self.accountNo}\n")
                f.write(f"{'='*60}\n\n")

    def check_password(self, password):
        return self.__password == password

    def change_password(self, new_pass):
        self.__password = new_pass

    def add_passbook_entry(self, message, trans_type="INFO"):
        time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open(self.passbook_file, "a") as f:
            f.write(f"[{time}] {trans_type}: {message}\n")
        
        # Add to transaction history
        self.transaction_history.append({
            'time': time,
            'type': trans_type,
            'message': message
        })

    def deposit(self, amount):
        if amount <= 0:
            return "Enter valid deposit amount!"

        self.balance += amount
        self.is_new = False
        self.add_passbook_entry(f"Deposited ₹{amount} | New Balance: ₹{self.balance}", "DEPOSIT")
        return f"✓ Deposit Successful!\n\nAmount: ₹{amount}\nNew Balance: ₹{self.balance}"

    def withdraw(self, amount):
        if amount <= 0:
            return "Enter valid withdraw amount!"

        if amount > self.balance:
            return "❌ Insufficient balance!\n\nAvailable Balance: ₹{self.balance}"

        self.balance -= amount
        self.add_passbook_entry(f"Withdrawn ₹{amount} | Remaining Balance: ₹{self.balance}", "WITHDRAW")
        return f"✓ Withdrawal Successful!\n\nAmount: ₹{amount}\nRemaining Balance: ₹{self.balance}"

    def apply_loan(self, amount):
        if self.loan > 0:
            return f"❌ Loan Application Denied!\n\nYou have a pending loan of ₹{self.loan}\nPlease clear it before applying for a new loan."

        if self.balance < 1000:
            return f"❌ Loan Application Denied!\n\nMinimum balance requirement: ₹1000\nYour current balance: ₹{self.balance}"

        if amount <= 0:
            return "Enter valid loan amount!"

        interest = int(amount * 0.10)
        total_loan = amount + interest

        self.loan = total_loan
        self.balance += amount

        self.add_passbook_entry(f"Loan Approved: ₹{amount} | Interest: ₹{interest} | Total Debt: ₹{total_loan}", "LOAN")
        return f"✓ Loan Approved!\n\nLoan Amount: ₹{amount}\nInterest (10%): ₹{interest}\nTotal Repayment: ₹{total_loan}\n\nAmount credited to account.\nNew Balance: ₹{self.balance}"

    def pay_loan(self, amount):
        if self.loan == 0:
            return "✓ No pending loans!\n\nYou have no outstanding loans."

        if amount <= 0:
            return "Enter valid payment amount!"

        if amount > self.balance:
            return f"❌ Insufficient Balance!\n\nPayment Amount: ₹{amount}\nAvailable Balance: ₹{self.balance}\nShortfall: ₹{amount - self.balance}"

        if amount > self.loan:
            amount = self.loan

        self.balance -= amount
        self.loan -= amount

        self.add_passbook_entry(f"Loan Payment: ₹{amount} | Remaining Debt: ₹{self.loan}", "PAYMENT")

        if self.loan == 0:
            return f"✓ Loan Fully Paid!\n\nPayment: ₹{amount}\nRemaining Loan: ₹0\n\nCongratulations! Your loan is cleared."

        return f"✓ Loan Payment Successful!\n\nPaid: ₹{amount}\nRemaining Loan: ₹{self.loan}\nAccount Balance: ₹{self.balance}"

    def check_loan_status(self):
        if self.loan > 0:
            self.loan += 1000
            self.add_passbook_entry(f"Late Payment Fine: ₹1000 | Updated Total Debt: ₹{self.loan}", "FINE")
            return f"⚠ LOAN ALERT!\n\nYou have a pending loan.\nLate payment fine of ₹1000 has been added.\n\nTotal Outstanding Loan: ₹{self.loan}\n\nPlease clear your dues at the earliest."
        return None

    def read_passbook(self):
        with open(self.passbook_file, "r") as f:
            return f.read()

    def get_recent_transactions(self, limit=5):
        return self.transaction_history[-limit:] if self.transaction_history else []


# ---------------- ACCOUNTS DATABASE ----------------
accounts = {}
accounts["1001"] = BankAccount("Cherry Blossom", 1234, "1001", 25000, 0, False)
accounts["1002"] = BankAccount("Aman Singh", 1111, "1002", 12000, 0, False)
accounts["1003"] = BankAccount("Riya Sharma", 2222, "1003", 45000, 0, False)
accounts["1004"] = BankAccount("Rahul Verma", 3333, "1004", 8500, 0, False)
accounts["1005"] = BankAccount("Neha Kapoor", 4444, "1005", 3200, 0, False)


# ---------------- CUSTOM WIDGETS ----------------
class ModernButton(tk.Button):
    def __init__(self, parent, text, command, bg="#2563eb", fg="white", **kwargs):
        super().__init__(
            parent, text=text, command=command,
            font=("Segoe UI", 11, "bold"),
            bg=bg, fg=fg,
            relief="flat", bd=0,
            activebackground=self.darken_color(bg),
            activeforeground="white",
            cursor="hand2",
            padx=25, pady=12,
            **kwargs
        )
        
        self.default_bg = bg
        self.hover_bg = self.darken_color(bg)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.config(bg=self.hover_bg)

    def on_leave(self, e):
        self.config(bg=self.default_bg)

    @staticmethod
    def darken_color(hex_color):
        # Simple color darkening
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, int(r * 0.8))
        g = max(0, int(g * 0.8))
        b = max(0, int(b * 0.8))
        return f'#{r:02x}{g:02x}{b:02x}'


class ModernEntry(tk.Entry):
    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(
            parent,
            font=("Segoe UI", 12),
            bd=0,
            bg="#f8fafc",
            fg="#1e293b",
            relief="flat",
            insertbackground="#2563eb",
            **kwargs
        )
        
        self.placeholder = placeholder
        self.placeholder_color = "#94a3b8"
        self.default_color = "#1e293b"
        
        if placeholder:
            self.insert(0, placeholder)
            self.config(fg=self.placeholder_color)
            self.bind("<FocusIn>", self.on_focus_in)
            self.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self, e):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=self.default_color)

    def on_focus_out(self, e):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)


# ---------------- GUI APP ----------------
class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BlueWave Bank - Modern Banking Experience")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#ffffff")

        self.current_user = None
        
        # Color scheme
        self.colors = {
            'primary': '#2563eb',
            'secondary': '#0ea5e9',
            'success': '#10b981',
            'danger': '#ef4444',
            'warning': '#f59e0b',
            'info': '#06b6d4',
            'dark': '#1e293b',
            'light': '#f8fafc',
            'purple': '#8b5cf6',
            'orange': '#f97316'
        }
        
        self.welcome_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------- SMOOTH GRADIENT BACKGROUND ----------------
    def create_gradient_background(self):
        canvas = tk.Canvas(self.root, width=1000, height=650, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Smooth gradient from blue to white
        steps = 100
        for i in range(steps):
            # Calculate color interpolation from blue (#3b82f6) to white (#ffffff)
            ratio = i / steps
            r = int(59 + (255 - 59) * ratio)
            g = int(130 + (255 - 130) * ratio)
            b = int(246 + (255 - 246) * ratio)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            y1 = i * (650 / steps)
            y2 = (i + 1) * (650 / steps)
            canvas.create_rectangle(0, y1, 1000, y2, fill=color, outline=color)

        return canvas

    # ---------------- WELCOME SCREEN ----------------
    def welcome_screen(self):
        self.clear_screen()
        canvas = self.create_gradient_background()

        # Logo and Title
        canvas.create_text(500, 140, text="🏦", font=("Segoe UI", 80), fill="white")
        
        canvas.create_text(500, 240, text="BLUEWAVE BANK",
                           font=("Segoe UI", 42, "bold"),
                           fill="white")

        canvas.create_text(500, 295, text="Your Trusted Digital Banking Partner",
                           font=("Segoe UI", 18),
                           fill="white")

        # Feature cards
        features_frame = tk.Frame(self.root, bg="white", bd=0)
        canvas.create_window(500, 390, window=features_frame)

        features = [
            ("🔒", "Secure"),
            ("⚡", "Fast"),
            ("📱", "Modern"),
            ("🌟", "Reliable")
        ]

        for i, (icon, text) in enumerate(features):
            frame = tk.Frame(features_frame, bg="white", relief="flat", bd=0)
            frame.grid(row=0, column=i, padx=15)
            
            tk.Label(frame, text=icon, font=("Segoe UI", 24), bg="white").pack()
            tk.Label(frame, text=text, font=("Segoe UI", 11, "bold"), 
                    bg="white", fg="#64748b").pack()

        # Call to action
        canvas.create_text(500, 480, 
                          text="Experience banking reimagined",
                          font=("Segoe UI", 14),
                          fill="#64748b")

        start_btn = ModernButton(self.root, "Get Started →", self.login_screen, 
                                bg=self.colors['primary'])
        canvas.create_window(500, 550, window=start_btn)

    # ---------------- LOGIN SCREEN ----------------
    def login_screen(self):
        self.clear_screen()
        canvas = self.create_gradient_background()

        # Header
        canvas.create_text(500, 100, text="Welcome Back",
                           font=("Segoe UI", 32, "bold"),
                           fill="white")

        canvas.create_text(500, 145, text="Sign in to your account",
                           font=("Segoe UI", 14),
                           fill="white")

        # Card
        card = tk.Frame(self.root, bg="white", width=480, height=400, relief="flat", bd=0)
        card.pack_propagate(False)
        canvas.create_window(500, 360, window=card)

        # Add shadow effect with subtle border
        canvas.create_rectangle(240, 160, 760, 560, fill="", outline="#e2e8f0", width=2)

        # Account Number
        tk.Label(card, text="Account Number", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#334155", anchor="w").pack(pady=(30, 5), padx=40, anchor="w")

        acc_entry = ModernEntry(card, placeholder="Enter your account number")
        acc_entry.pack(ipady=10, ipadx=20, padx=40, fill="x")

        # Password
        tk.Label(card, text="Password", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#334155", anchor="w").pack(pady=(20, 5), padx=40, anchor="w")

        pass_entry = ModernEntry(card, placeholder="Enter your password", show="")
        pass_entry.pack(ipady=10, ipadx=20, padx=40, fill="x")
        pass_entry.config(show="*")

        def login():
            accNo = acc_entry.get()
            if accNo == "Enter your account number":
                messagebox.showerror("Error", "Please enter your account number!")
                return
                
            try:
                password_text = pass_entry.get()
                if password_text == "Enter your password":
                    messagebox.showerror("Error", "Please enter your password!")
                    return
                password = int(password_text)
            except:
                messagebox.showerror("Error", "Password must be a number!")
                return

            if accNo in accounts:
                user = accounts[accNo]
                if user.check_password(password):
                    self.current_user = user

                    loan_warning = user.check_loan_status()
                    if loan_warning:
                        messagebox.showwarning("Loan Alert", loan_warning)

                    self.dashboard()
                else:
                    messagebox.showerror("Login Failed", "Incorrect password!\n\nPlease try again.")
            else:
                messagebox.showerror("Login Failed", "Account not found!\n\nPlease check your account number.")

        ModernButton(card, "LOGIN", login, bg=self.colors['primary']).pack(pady=(30, 10), padx=40, fill="x")

        # Divider
        divider_frame = tk.Frame(card, bg="white")
        divider_frame.pack(pady=15, fill="x", padx=40)
        
        tk.Frame(divider_frame, bg="#e2e8f0", height=1).pack(side="left", fill="x", expand=True)
        tk.Label(divider_frame, text=" or ", bg="white", fg="#94a3b8", 
                font=("Segoe UI", 9)).pack(side="left", padx=5)
        tk.Frame(divider_frame, bg="#e2e8f0", height=1).pack(side="left", fill="x", expand=True)

        # Secondary actions
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(pady=5, padx=40, fill="x")
        
        ModernButton(btn_frame, "Create Account", self.create_account_screen, 
                    bg=self.colors['success']).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ModernButton(btn_frame, "Reset Password", self.reset_password_screen, 
                    bg=self.colors['purple']).pack(side="right", expand=True, fill="x", padx=(5, 0))

        ModernButton(self.root, "← Back", self.welcome_screen, 
                    bg=self.colors['dark']).place(x=20, y=20)

    # ---------------- CREATE ACCOUNT ----------------
    def create_account_screen(self):
        self.clear_screen()
        canvas = self.create_gradient_background()

        canvas.create_text(500, 90, text="Create Your Account",
                           font=("Segoe UI", 32, "bold"),
                           fill="white")

        canvas.create_text(500, 135, text="Join thousands of satisfied customers",
                           font=("Segoe UI", 14),
                           fill="white")

        card = tk.Frame(self.root, bg="white", width=480, height=400, relief="flat")
        card.pack_propagate(False)
        canvas.create_window(500, 380, window=card)

        tk.Label(card, text="Full Name", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#334155", anchor="w").pack(pady=(30, 5), padx=40, anchor="w")

        name_entry = ModernEntry(card, placeholder="Enter your full name")
        name_entry.pack(ipady=10, ipadx=20, padx=40, fill="x")

        tk.Label(card, text="Create Password (numeric)", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#334155", anchor="w").pack(pady=(20, 5), padx=40, anchor="w")

        pass_entry = ModernEntry(card, placeholder="Create a 4-digit PIN", show="")
        pass_entry.pack(ipady=10, ipadx=20, padx=40, fill="x")
        pass_entry.config(show="*")

        # Info box
        info_frame = tk.Frame(card, bg="#eff6ff", relief="flat", bd=0)
        info_frame.pack(pady=20, padx=40, fill="x")
        
        tk.Label(info_frame, text="ℹ️", font=("Segoe UI", 14), bg="#eff6ff").pack(side="left", padx=10, pady=10)
        tk.Label(info_frame, text="Your account will be created instantly\nwith zero balance", 
                font=("Segoe UI", 10), bg="#eff6ff", fg="#1e40af", 
                justify="left").pack(side="left", pady=10)

        def create():
            name = name_entry.get()
            if name == "" or name == "Enter your full name":
                messagebox.showerror("Error", "Please enter your name!")
                return

            try:
                password_text = pass_entry.get()
                if password_text == "Create a 4-digit PIN":
                    messagebox.showerror("Error", "Please create a password!")
                    return
                password = int(password_text)
            except:
                messagebox.showerror("Error", "Password must be numeric!")
                return

            new_acc_no = str(1000 + len(accounts) + 1)
            accounts[new_acc_no] = BankAccount(name, password, new_acc_no, 0, 0, True)

            messagebox.showinfo("Success", 
                              f"🎉 Account Created Successfully!\n\n"
                              f"Account Number: {new_acc_no}\n"
                              f"Account Holder: {name}\n\n"
                              f"Please save your account number for future login.")
            self.login_screen()

        ModernButton(card, "CREATE ACCOUNT", create, bg=self.colors['success']).pack(pady=15, padx=40, fill="x")

        ModernButton(self.root, "← Back", self.login_screen, bg=self.colors['dark']).place(x=20, y=20)

    # ---------------- RESET PASSWORD ----------------
    def reset_password_screen(self):
        self.clear_screen()
        canvas = self.create_gradient_background()

        canvas.create_text(500, 90, text="Reset Password",
                           font=("Segoe UI", 32, "bold"),
                           fill="white")

        canvas.create_text(500, 135, text="Verify your identity to reset password",
                           font=("Segoe UI", 14),
                           fill="white")

        card = tk.Frame(self.root, bg="white", width=480, height=450, relief="flat")
        card.pack_propagate(False)
        canvas.create_window(500, 390, window=card)

        tk.Label(card, text="Account Number", font=("Segoe UI", 12, "bold"), 
                bg="white", fg="#334155", anchor="w").pack(pady=(30, 5), padx=40, anchor="w")
        acc_entry = ModernEntry(card, placeholder="Enter your account number")
        acc_entry.pack(ipady=10, ipadx=20, padx=40, fill="x")

        tk.Label(card, text="Full Name (for verification)", font=("Segoe UI", 12, "bold"), 
                bg="white", fg="#334155", anchor="w").pack(pady=(20, 5), padx=40, anchor="w")
        name_entry = ModernEntry(card, placeholder="Enter your registered name")
        name_entry.pack(ipady=10, ipadx=20, padx=40, fill="x")

        tk.Label(card, text="New Password", font=("Segoe UI", 12, "bold"), 
                bg="white", fg="#334155", anchor="w").pack(pady=(20, 5), padx=40, anchor="w")
        new_pass_entry = ModernEntry(card, placeholder="Enter new password", show="")
        new_pass_entry.pack(ipady=10, ipadx=20, padx=40, fill="x")
        new_pass_entry.config(show="*")

        def reset():
            accNo = acc_entry.get()
            name = name_entry.get()

            if accNo == "Enter your account number" or name == "Enter your registered name":
                messagebox.showerror("Error", "Please fill all fields!")
                return

            try:
                password_text = new_pass_entry.get()
                if password_text == "Enter new password":
                    messagebox.showerror("Error", "Please enter new password!")
                    return
                new_pass = int(password_text)
            except:
                messagebox.showerror("Error", "Password must be numeric!")
                return

            if accNo in accounts:
                user = accounts[accNo]
                if user.name == name:
                    user.change_password(new_pass)
                    user.add_passbook_entry("Password reset completed", "SECURITY")
                    messagebox.showinfo("Success", 
                                      "✓ Password Reset Successful!\n\n"
                                      "You can now login with your new password.")
                    self.login_screen()
                else:
                    messagebox.showerror("Verification Failed", 
                                       "Name doesn't match account records!\n\n"
                                       "Please enter the registered name.")
            else:
                messagebox.showerror("Error", "Account not found!")

        ModernButton(card, "RESET PASSWORD", reset, bg=self.colors['danger']).pack(pady=30, padx=40, fill="x")

        ModernButton(self.root, "← Back", self.login_screen, bg=self.colors['dark']).place(x=20, y=20)

    # ---------------- DASHBOARD ----------------
    def dashboard(self):
        self.clear_screen()
        canvas = self.create_gradient_background()

        # Header
        canvas.create_text(500, 70, text=f"Welcome back, {self.current_user.name.split()[0]}! 👋",
                           font=("Segoe UI", 28, "bold"),
                           fill="white")

        # Balance Card
        balance_card = tk.Frame(self.root, bg="white", width=920, height=140, relief="flat")
        balance_card.pack_propagate(False)
        canvas.create_window(500, 180, window=balance_card)

        # Account info section
        left_section = tk.Frame(balance_card, bg="white")
        left_section.pack(side="left", fill="both", expand=True, padx=30, pady=20)

        tk.Label(left_section, text="Account Balance", 
                font=("Segoe UI", 12), bg="white", fg="#64748b").pack(anchor="w")
        tk.Label(left_section, text=f"₹{self.current_user.balance:,}", 
                font=("Segoe UI", 36, "bold"), bg="white", fg="#10b981").pack(anchor="w", pady=5)
        tk.Label(left_section, text=f"Account No: {self.current_user.accountNo}", 
                font=("Segoe UI", 11), bg="white", fg="#64748b").pack(anchor="w")

        # Loan info section
        right_section = tk.Frame(balance_card, bg="#fef2f2", width=280, relief="flat")
        right_section.pack(side="right", fill="y")
        right_section.pack_propagate(False)

        tk.Label(right_section, text="Outstanding Loan", 
                font=("Segoe UI", 11), bg="#fef2f2", fg="#991b1b").pack(pady=(25, 5))
        tk.Label(right_section, text=f"₹{self.current_user.loan:,}", 
                font=("Segoe UI", 24, "bold"), bg="#fef2f2", 
                fg="#dc2626" if self.current_user.loan > 0 else "#10b981").pack()
        
        if self.current_user.loan > 0:
            tk.Label(right_section, text="⚠ Please clear dues", 
                    font=("Segoe UI", 9), bg="#fef2f2", fg="#991b1b").pack(pady=5)

        # Action Buttons Grid
        btn_container = tk.Frame(self.root, bg="white", width=920, height=320, relief="flat")
        btn_container.pack_propagate(False)
        canvas.create_window(500, 430, window=btn_container)

        actions = [
            ("💰 Deposit Money", self.deposit_screen, self.colors['success']),
            ("💸 Withdraw Money", self.withdraw_screen, self.colors['primary']),
            ("🏦 Apply for Loan", self.loan_screen, self.colors['purple']),
            ("💳 Pay Loan", self.pay_loan_screen, self.colors['orange']),
            ("📒 View Passbook", self.passbook_screen, self.colors['info']),
            ("📊 Account Summary", self.account_summary, self.colors['secondary'])
        ]

        for i, (text, cmd, color) in enumerate(actions):
            row = i // 3
            col = i % 3
            btn = ModernButton(btn_container, text, cmd, bg=color)
            btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

        # Configure grid weights
        for i in range(2):
            btn_container.grid_rowconfigure(i, weight=1)
        for i in range(3):
            btn_container.grid_columnconfigure(i, weight=1)

        # Logout button
        ModernButton(self.root, "Logout →", self.confirm_logout, 
                    bg=self.colors['dark']).place(x=850, y=20)

    def confirm_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.welcome_screen()

    # ---------------- ACCOUNT SUMMARY ----------------
    def account_summary(self):
        self.clear_screen()
        canvas = self.create_gradient_background()

        canvas.create_text(500, 70, text="Account Summary",
                           font=("Segoe UI", 28, "bold"),
                           fill="white")

        # Summary card
        card = tk.Frame(self.root, bg="white", width=900, height=500, relief="flat")
        card.pack_propagate(False)
        canvas.create_window(500, 360, window=card)

        # Account details
        details_frame = tk.Frame(card, bg="white")
        details_frame.pack(pady=30, padx=40, fill="both", expand=True)

        details = [
            ("Account Holder", self.current_user.name),
            ("Account Number", self.current_user.accountNo),
            ("Current Balance", f"₹{self.current_user.balance:,}"),
            ("Outstanding Loan", f"₹{self.current_user.loan:,}"),
            ("Account Status", "Active ✓"),
            ("Account Type", "Savings Account")
        ]

        for i, (label, value) in enumerate(details):
            row_frame = tk.Frame(details_frame, bg="#f8fafc" if i % 2 == 0 else "white", 
                                height=50, relief="flat")
            row_frame.pack(fill="x", pady=2)
            row_frame.pack_propagate(False)

            tk.Label(row_frame, text=label, font=("Segoe UI", 12, "bold"),
                    bg=row_frame['bg'], fg="#334155", anchor="w").pack(side="left", padx=20, pady=15)
            tk.Label(row_frame, text=value, font=("Segoe UI", 12),
                    bg=row_frame['bg'], fg="#64748b", anchor="e").pack(side="right", padx=20, pady=15)

        # Recent transactions
        tk.Label(card, text="Recent Transactions", font=("Segoe UI", 14, "bold"),
                bg="white", fg="#334155").pack(pady=(20, 10), padx=40, anchor="w")

        recent = self.current_user.get_recent_transactions(3)
        if recent:
            for trans in recent:
                trans_frame = tk.Frame(card, bg="#eff6ff", relief="flat")
                trans_frame.pack(fill="x", padx=40, pady=3)
                
                tk.Label(trans_frame, text=trans['type'], font=("Segoe UI", 10, "bold"),
                        bg="#eff6ff", fg="#1e40af").pack(side="left", padx=15, pady=8)
                tk.Label(trans_frame, text=trans['message'], font=("Segoe UI", 9),
                        bg="#eff6ff", fg="#64748b").pack(side="left", padx=5, pady=8)
        else:
            tk.Label(card, text="No recent transactions", font=("Segoe UI", 10),
                    bg="white", fg="#94a3b8").pack(padx=40, anchor="w")

        ModernButton(self.root, "← Back to Dashboard", self.dashboard, 
                    bg=self.colors['dark']).place(x=20, y=20)

    # ---------------- DEPOSIT ----------------
    def deposit_screen(self):
        self.transaction_screen("Deposit Money", "💰", "Deposit", 
                              self.current_user.deposit, self.colors['success'],
                              "Add funds to your account")

    # ---------------- WITHDRAW ----------------
    def withdraw_screen(self):
        self.transaction_screen("Withdraw Money", "💸", "Withdraw", 
                              self.current_user.withdraw, self.colors['primary'],
                              "Withdraw funds from your account")

    # ---------------- LOAN ----------------
    def loan_screen(self):
        self.transaction_screen("Apply for Loan", "🏦", "Apply for Loan", 
                              self.current_user.apply_loan, self.colors['purple'],
                              "Get instant loan approval (10% interest)")

    # ---------------- PAY LOAN ----------------
    def pay_loan_screen(self):
        self.transaction_screen("Pay Loan", "💳", "Pay Loan", 
                              self.current_user.pay_loan, self.colors['orange'],
                              "Clear your outstanding loan")

    # ---------------- COMMON TRANSACTION SCREEN ----------------
    def transaction_screen(self, title, icon, btn_text, func, color, subtitle):
        self.clear_screen()
        canvas = self.create_gradient_background()

        canvas.create_text(500, 80, text=icon, font=("Segoe UI", 50), fill="white")
        
        canvas.create_text(500, 160, text=title,
                           font=("Segoe UI", 28, "bold"),
                           fill="white")

        canvas.create_text(500, 200, text=subtitle,
                           font=("Segoe UI", 13),
                           fill="white")

        card = tk.Frame(self.root, bg="white", width=520, height=320, relief="flat")
        card.pack_propagate(False)
        canvas.create_window(500, 400, window=card)

        # Current balance display
        balance_frame = tk.Frame(card, bg="#f0fdf4", relief="flat")
        balance_frame.pack(fill="x", pady=(25, 20), padx=40)
        
        tk.Label(balance_frame, text="Available Balance:", font=("Segoe UI", 11),
                bg="#f0fdf4", fg="#166534").pack(side="left", padx=15, pady=10)
        tk.Label(balance_frame, text=f"₹{self.current_user.balance:,}", 
                font=("Segoe UI", 14, "bold"),
                bg="#f0fdf4", fg="#10b981").pack(side="right", padx=15, pady=10)

        tk.Label(card, text="Enter Amount (₹)", font=("Segoe UI", 12, "bold"), 
                bg="white", fg="#334155", anchor="w").pack(pady=(10, 5), padx=40, anchor="w")
        
        entry = ModernEntry(card, placeholder="0")
        entry.pack(ipady=12, ipadx=20, padx=40, fill="x")
        entry.config(font=("Segoe UI", 16), justify="center")

        def submit():
            try:
                amount_text = entry.get()
                if amount_text == "0" or amount_text == "":
                    messagebox.showerror("Error", "Please enter a valid amount!")
                    return
                amount = int(amount_text)
            except:
                messagebox.showerror("Error", "Please enter a valid number!")
                return

            msg = func(amount)
            
            if "✓" in msg or "Successful" in msg:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showwarning("Transaction Failed", msg)
            
            self.dashboard()

        ModernButton(card, btn_text.upper(), submit, bg=color).pack(pady=30, padx=40, fill="x")

        # Quick amount buttons for deposit/withdraw
        if "Deposit" in title or "Withdraw" in title:
            quick_frame = tk.Frame(card, bg="white")
            quick_frame.pack(pady=(0, 20))
            
            tk.Label(quick_frame, text="Quick Amount:", font=("Segoe UI", 9),
                    bg="white", fg="#64748b").pack(side="left", padx=5)
            
            for amt in [500, 1000, 5000, 10000]:
                btn = tk.Button(quick_frame, text=f"₹{amt}", 
                               font=("Segoe UI", 9), bg="#f1f5f9", fg="#334155",
                               relief="flat", bd=0, cursor="hand2",
                               command=lambda a=amt: entry.delete(0, tk.END) or entry.insert(0, str(a)))
                btn.pack(side="left", padx=3)

        ModernButton(self.root, "← Back to Dashboard", self.dashboard, 
                    bg=self.colors['dark']).place(x=20, y=20)

    # ---------------- PASSBOOK SCREEN ----------------
    def passbook_screen(self):
        self.clear_screen()
        canvas = self.create_gradient_background()

        canvas.create_text(500, 70, text="📒 Transaction Passbook",
                           font=("Segoe UI", 28, "bold"),
                           fill="white")

        canvas.create_text(500, 115, text="Complete history of all your transactions",
                           font=("Segoe UI", 13),
                           fill="white")

        # Passbook frame
        passbook_frame = tk.Frame(self.root, bg="white", width=900, height=460, relief="flat")
        passbook_frame.pack_propagate(False)
        canvas.create_window(500, 390, window=passbook_frame)

        # Text area with custom styling
        text_area = scrolledtext.ScrolledText(
            passbook_frame, 
            width=105, 
            height=24, 
            font=("Consolas", 10),
            bg="#f8fafc",
            fg="#1e293b",
            relief="flat",
            bd=0,
            padx=15,
            pady=15
        )
        text_area.pack(fill="both", expand=True, padx=20, pady=20)

        passbook_content = self.current_user.read_passbook()
        text_area.insert(tk.END, passbook_content)
        text_area.config(state="disabled")

        # Export button
        ModernButton(self.root, "💾 Export PDF", 
                    lambda: messagebox.showinfo("Export", "PDF export feature coming soon!"),
                    bg=self.colors['info']).place(x=780, y=20)

        ModernButton(self.root, "← Back to Dashboard", self.dashboard, 
                    bg=self.colors['dark']).place(x=20, y=20)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()