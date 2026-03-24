from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

# Load data
def load_data():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except:
        return []

# Save data
def save_data(data):
    with open("expenses.json", "w") as file:
        json.dump(data, file, indent=4)

# Home page
@app.route("/")
def index():
    data = load_data()
    total = sum(exp["amount"] for exp in data)
    return render_template("index.html", expenses=data, total=total)

# Add expense
@app.route("/add", methods=["POST"])
def add():
    amount = float(request.form["amount"])
    category = request.form["category"]
    date = request.form["date"]

    data = load_data()

    expense = {
        "amount": amount,
        "category": category,
        "date": date
    }

    data.append(expense)
    save_data(data)

    return redirect("/")

# Delete one expense
@app.route("/delete/<int:index>")
def delete(index):
    data = load_data()

    if 0 <= index < len(data):
        data.pop(index)

    save_data(data)
    return redirect("/")

# Clear all expenses
@app.route("/clear")
def clear():
    save_data([])
    return redirect("/")

# Run app
if __name__ == "__main__":
    app.run(debug=True)