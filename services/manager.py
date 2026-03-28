import datetime
from data.storage import load_data, save_data

# Add a new subscription
def add_subscription(name, price, days):
    data = load_data()
    sub = {
        "name": name,  # Subscription name
        "price": price,  # Cost
        "added": str(datetime.date.today()),  # Date added
        "next_billing": str(datetime.date.today() + datetime.timedelta(days=days))  # Next billing date
    }
    data.append(sub)
    save_data(data)

# Get all subscriptions
def get_all():
    return load_data()

# Delete subscription by index
def delete_subscription(index):
    data = load_data()
    data.pop(index)  # Remove selected item
    save_data(data)

# Search subscriptions by keyword
def search_subscription(keyword):
    data = load_data()
    return [sub for sub in data if keyword.lower() in sub["name"].lower()]

# Calculate total monthly cost
def total_monthly_cost():
    data = load_data()
    return sum(sub["price"] for sub in data)