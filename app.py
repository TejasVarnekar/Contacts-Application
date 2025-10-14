
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model (table)
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

# Home page - list all contacts
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_name = request.form['search']
        contacts = Contact.query.filter(Contact.name.contains(search_name)).all()
    else:
        contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

# Add a new contact
@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        new_contact = Contact(name=name, phone=phone, email=email)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_contact.html')

# Edit contact
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.phone = request.form['phone']
        contact.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_contact.html', contact=contact)

# Delete contact
@app.route('/delete/<int:id>')
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # Create database and table automatically
    app.run(debug=True)


