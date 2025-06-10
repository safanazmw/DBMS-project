from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database config
db = mysql.connector.connect(
    host="localhost",
    user="safanaz",
    password="23cd015",
    database="addressbook101"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        cursor.execute("INSERT INTO contacts (name, email, phone, address) VALUES (%s, %s, %s, %s)",
                       (name, email, phone, address))
        db.commit()
        return redirect('/')
    return render_template('add_contact.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        cursor.execute("""
            UPDATE contacts SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s
        """, (name, email, phone, address, id))
        db.commit()
        return redirect('/')
    cursor.execute("SELECT * FROM contacts WHERE id = %s", (id,))
    contact = cursor.fetchone()
    return render_template('edit_contact.html', contact=contact)

@app.route('/delete/<int:id>')
def delete_contact(id):
    cursor.execute("DELETE FROM contacts WHERE id = %s", (id,))
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
