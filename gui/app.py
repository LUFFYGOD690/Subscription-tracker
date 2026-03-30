import tkinter as tk
from tkinter import ttk, messagebox
from services import manager
import datetime

# Main Application Class (View Layer)
class SubscriptionApp:
    def __init__(self, root):
        # Initialize main window
        self.root = root
        self.root.title("Subscription Tracker")
        self.root.geometry("600x650")
        self.root.configure(bg="#eef2f7")

        # Apply modern ttk theme
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Build UI and load data
        self.build_ui()
        self.refresh_list()
        self.upcoming_bills_alert()

    # ---------- Build UI ----------
    def build_ui(self):
        # Title label
        title = tk.Label(self.root, text="💳 Subscription Tracker",
                         font=("Segoe UI", 22, "bold"),
                         bg="#eef2f7", fg="#222")
        title.pack(pady=15)

        # Input card container
        card = tk.Frame(self.root, bg="white", bd=0, relief="flat")
        card.pack(padx=15, pady=10, fill="x")

        # Name input
        tk.Label(card, text="Name", bg="white").grid(row=0, column=0, pady=5)
        self.entry_name = ttk.Entry(card)
        self.entry_name.grid(row=0, column=1, pady=5, padx=5)

        # Price input
        tk.Label(card, text="Price", bg="white").grid(row=1, column=0, pady=5)
        self.entry_price = ttk.Entry(card)
        self.entry_price.grid(row=1, column=1, pady=5, padx=5)

        # Billing days input
        tk.Label(card, text="Billing Days", bg="white").grid(row=2, column=0, pady=5)
        self.entry_days = ttk.Entry(card)
        self.entry_days.grid(row=2, column=1, pady=5, padx=5)

        # Button section
        btn_frame = tk.Frame(self.root, bg="#eef2f7")
        btn_frame.pack(pady=10)

        # Action buttons
        ttk.Button(btn_frame, text="Add", command=self.add).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_list).grid(row=0, column=2, padx=5)

        # Cost calculation buttons
        ttk.Button(btn_frame, text="Monthly", command=self.show_monthly).grid(row=1, column=0, pady=5)
        ttk.Button(btn_frame, text="Yearly", command=self.show_yearly).grid(row=1, column=1, pady=5)

        # Search section
        search_frame = tk.Frame(self.root, bg="#eef2f7")
        search_frame.pack(pady=5)

        self.entry_search = ttk.Entry(search_frame, width=25)
        self.entry_search.grid(row=0, column=0, padx=5)

        ttk.Button(search_frame, text="Search", command=self.search).grid(row=0, column=1, padx=5)
        ttk.Button(search_frame, text="Clear", command=self.refresh_list).grid(row=0, column=2, padx=5)

        # Table (Treeview) to display subscriptions
        self.tree = ttk.Treeview(self.root, columns=("Name", "Price", "Next"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Next", text="Next Billing")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    # ---------- Refresh List ----------
    def refresh_list(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        today = datetime.date.today()

        # Load all subscriptions
        for sub in manager.get_all():
            next_date = datetime.datetime.strptime(sub["next_billing"], "%Y-%m-%d").date()

            # Highlight upcoming bills (within 7 days)
            tag = ""
            if 0 <= (next_date - today).days <= 7:
                tag = "warning"

            # Insert into table
            self.tree.insert("", "end", values=(sub['name'], f"₹{sub['price']}", sub['next_billing']), tags=(tag,))

        # Configure highlight style
        self.tree.tag_configure("warning", background="#ffe5e5")

    # ---------- Add Subscription ----------
    def add(self):
        try:
            manager.add_subscription(
                self.entry_name.get(),
                float(self.entry_price.get()),
                int(self.entry_days.get())
            )
            self.refresh_list()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- Delete Subscription ----------
    def delete(self):
        try:
            selected = self.tree.selection()[0]
            index = self.tree.index(selected)
            manager.delete_subscription(index)
            self.refresh_list()
        except:
            messagebox.showerror("Error", "Select item")

    # ---------- Show Monthly Cost ----------
    def show_monthly(self):
        total = manager.total_monthly_cost()
        messagebox.showinfo("Monthly Cost", f"₹{total:.2f}")

    # ---------- Show Yearly Cost ----------
    def show_yearly(self):
        total = manager.total_monthly_cost() * 12
        messagebox.showinfo("Yearly Cost", f"₹{total:.2f}")

    # ---------- Search Subscriptions ----------
    def search(self):
        results = manager.search_subscription(self.entry_search.get())

        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert search results
        for sub in results:
            self.tree.insert("", "end", values=(sub['name'], f"₹{sub['price']}", sub['next_billing']))

    # ---------- Clear Input Fields ----------
    def clear_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_days.delete(0, tk.END)

    # ---------- Upcoming Bills Alert ----------
    def upcoming_bills_alert(self):
        today = datetime.date.today()
        upcoming = []

        # Check all subscriptions
        for sub in manager.get_all():
            next_date = datetime.datetime.strptime(sub["next_billing"], "%Y-%m-%d").date()

            # Add if due within 7 days
            if 0 <= (next_date - today).days <= 7:
                upcoming.append(f"{sub['name']} due on {next_date}")

        # Show popup alert
        if upcoming:
            messagebox.showinfo("Upcoming Bills", "\n".join(upcoming))


# ---------- Run Application ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = SubscriptionApp(root)
    root.mainloop()
