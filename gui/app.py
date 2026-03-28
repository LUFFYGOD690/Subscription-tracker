import tkinter as tk
from tkinter import messagebox
from services import manager
import datetime

# Main GUI Class
class SubscriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Subscription Tracker")  # Window title
        self.root.geometry("550x650")  # Window size
        self.root.configure(bg="#f0f2f5")  # Background color

        self.build_ui()  # Build UI components
        self.refresh_list()  # Load existing data
        self.upcoming_bills_alert()  # Show upcoming bills

    # ---------- Build UI ----------
    def build_ui(self):
        # App title label
        tk.Label(self.root, text="💳 Subscription Tracker",
                 font=("Helvetica", 20, "bold"),
                 bg="#f0f2f5", fg="#333").pack(pady=10)

        # Input section
        frame = tk.Frame(self.root, bg="#f0f2f5", padx=10, pady=10)
        frame.pack(fill="x")

        # Name input
        tk.Label(frame, text="Name", bg="#f0f2f5").grid(row=0, column=0)
        self.entry_name = tk.Entry(frame)
        self.entry_name.grid(row=0, column=1)

        # Price input
        tk.Label(frame, text="Price", bg="#f0f2f5").grid(row=1, column=0)
        self.entry_price = tk.Entry(frame)
        self.entry_price.grid(row=1, column=1)

        # Billing days input
        tk.Label(frame, text="Billing Days", bg="#f0f2f5").grid(row=2, column=0)
        self.entry_days = tk.Entry(frame)
        self.entry_days.grid(row=2, column=1)

        # Buttons section
        btn_frame = tk.Frame(self.root, bg="#f0f2f5")
        btn_frame.pack()

        # Add new subscription
        tk.Button(btn_frame, text="Add", command=self.add).grid(row=0, column=0)

        # Delete selected subscription
        tk.Button(btn_frame, text="Delete", command=self.delete).grid(row=0, column=1)

        # Refresh list
        tk.Button(btn_frame, text="Refresh", command=self.refresh_list).grid(row=0, column=2)

        # Show monthly cost
        tk.Button(btn_frame, text="Monthly Cost", command=self.show_monthly).grid(row=1, column=0)

        # Show yearly cost
        tk.Button(btn_frame, text="Yearly Cost", command=self.show_yearly).grid(row=1, column=1)

        # Search section
        search_frame = tk.Frame(self.root, bg="#f0f2f5")
        search_frame.pack()

        self.entry_search = tk.Entry(search_frame)
        self.entry_search.grid(row=0, column=0)

        # Search button
        tk.Button(search_frame, text="Search", command=self.search).grid(row=0, column=1)

        # Clear search results
        tk.Button(search_frame, text="Clear", command=self.refresh_list).grid(row=0, column=2)

        # Listbox to display subscriptions
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(list_frame)
        self.listbox.pack(side="left", fill="both", expand=True)

        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

    # ---------- Refresh List ----------
    def refresh_list(self):
        self.listbox.delete(0, tk.END)  # Clear list
        today = datetime.date.today()

        # Loop through subscriptions
        for sub in manager.get_all():
            next_date = datetime.datetime.strptime(sub["next_billing"], "%Y-%m-%d").date()

            # Highlight upcoming bills (within 7 days)
            if 0 <= (next_date - today).days <= 7:
                display_text = f"⚠️ {sub['name']} | ₹{sub['price']} | {sub['next_billing']}"
            else:
                display_text = f"{sub['name']} | ₹{sub['price']} | {sub['next_billing']}"

            self.listbox.insert(tk.END, display_text)

        self.entry_search.delete(0, tk.END)  # Clear search box

    # Clear input fields
    def clear_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_days.delete(0, tk.END)

    # Add subscription
    def add(self):
        try:
            name = self.entry_name.get()
            price = float(self.entry_price.get())
            days = int(self.entry_days.get())

            manager.add_subscription(name, price, days)
            self.refresh_list()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Delete selected subscription
    def delete(self):
        try:
            index = self.listbox.curselection()[0]
            manager.delete_subscription(index)
            self.refresh_list()
        except:
            messagebox.showerror("Error", "Select item")

    # Show monthly cost popup
    def show_monthly(self):
        total = manager.total_monthly_cost()
        messagebox.showinfo("Monthly Cost", f"₹{total:.2f}")

    # Show yearly cost popup
    def show_yearly(self):
        total = manager.total_monthly_cost() * 12
        messagebox.showinfo("Yearly Cost", f"₹{total:.2f}")

    # Search subscriptions
    def search(self):
        keyword = self.entry_search.get()
        results = manager.search_subscription(keyword)

        self.listbox.delete(0, tk.END)

        today = datetime.date.today()
        for sub in results:
            next_date = datetime.datetime.strptime(sub["next_billing"], "%Y-%m-%d").date()

            if 0 <= (next_date - today).days <= 7:
                display_text = f"⚠️ {sub['name']} | ₹{sub['price']} | {sub['next_billing']}"
            else:
                display_text = f"{sub['name']} | ₹{sub['price']} | {sub['next_billing']}"

            self.listbox.insert(tk.END, display_text)

    # Show popup for upcoming bills
    def upcoming_bills_alert(self):
        today = datetime.date.today()
        upcoming = []

        for sub in manager.get_all():
            next_date = datetime.datetime.strptime(sub["next_billing"], "%Y-%m-%d").date()

            # Check if bill is within 7 days
            if 0 <= (next_date - today).days <= 7:
                upcoming.append(f"{sub['name']} due on {next_date}")

        # Show alert if any upcoming bills
        if upcoming:
            messagebox.showinfo("Upcoming Bills", "\n".join(upcoming))


# Run directly (for testing)
if __name__ == "__main__":
    root = tk.Tk()
    app = SubscriptionApp(root)
    root.mainloop()