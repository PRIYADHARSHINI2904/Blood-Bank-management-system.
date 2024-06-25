from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="bloodbank"
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_donor', methods=['GET', 'POST'])
def add_donor():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        blood_group = request.form['blood_group']
        contact = request.form['contact']

        if not (name and age and blood_group and contact):
            flash('All fields are required', 'warning')
            return redirect(url_for('add_donor'))

        try:
            cursor.execute("INSERT INTO donors (name, age, blood_group, contact) VALUES (%s, %s, %s, %s)", (name, age, blood_group, contact))
            cursor.execute("INSERT INTO blood_stock (blood_group, quantity) VALUES (%s, 1) ON DUPLICATE KEY UPDATE quantity = quantity + 1", (blood_group,))
            db.commit()
            flash('Donor added successfully', 'success')
        except Exception as e:
            flash(str(e), 'error')

        return redirect(url_for('add_donor'))

    return render_template('add_donor.html')

@app.route('/view_donors')
def view_donors():
    cursor.execute("SELECT name,age,blood_group,contact FROM donors")
    donors = cursor.fetchall()
    return render_template('view_donors.html', donors=donors)

@app.route('/view_stock')
def view_stock():
    cursor.execute("SELECT * FROM blood_stock")
    stock = cursor.fetchall()
    return render_template('view_stock.html', stock=stock)

if __name__ == '__main__':
    app.run(debug=True)
