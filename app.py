from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Needed for flash messages

# Database configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<Contact {self.name}>"

# Create database tables
with app.app_context():
    db.create_all()

# Index route: list, search, and sort contacts
@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = ""
    sort_option = request.args.get('sort')

    if request.method == 'POST':
        search_query = request.form.get('search', '')

    # Base query
    contacts_query = Contact.query

    # Search filter
    if search_query:
        contacts_query = contacts_query.filter(Contact.name.contains(search_query))

    # Sorting
    if sort_option == 'name_asc':
        contacts_query = contacts_query.order_by(Contact.name.asc())
    elif sort_option == 'name_desc':
        contacts_query = contacts_query.order_by(Contact.name.desc())

    contacts = contacts_query.all()
    return render_template('index.html', contacts=contacts)

# Add new contact
@app.route('/add_contact', methods=['POST'])
def add_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    if not (phone.isdigit() and len(phone) == 10):
        flash("Phone number must be exactly 10 digits!", "warning")
        return redirect(url_for('index'))

    new_contact = Contact(name=name, email=email, phone=phone)
    db.session.add(new_contact)
    db.session.commit()
    flash(f"Contact {name} added successfully!", "success")
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

