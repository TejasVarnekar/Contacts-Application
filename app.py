from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SECRET_KEY'] = 'my_secret_key_123'  # Needed for flash messages
db = SQLAlchemy(app)

# Define Contact table
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)

# Home page: list, search, sort
@app.route('/', methods=['GET', 'POST'])
def home():
    search_query = request.form.get('search') if request.method == 'POST' else ''
    sort_option = request.args.get('sort', 'name_asc')

    query = Contact.query
    if search_query:
        query = query.filter(Contact.full_name.contains(search_query))
    
    if sort_option == 'name_asc':
        query = query.order_by(Contact.full_name.asc())
    else:
        query = query.order_by(Contact.full_name.desc())
    
    my_contacts = query.all()
    return render_template('index.html', contacts=my_contacts)

# Add new contact
@app.route('/add_contact', methods=['POST'])
def add_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    # Validate phone number
    if not (phone.isdigit() and len(phone) == 10):
        flash("Phone number must be 10 digits exactly!", "warning")
        return redirect(url_for('home'))

    contact_entry = Contact(full_name=name, email=email, phone_number=phone)
    db.session.add(contact_entry)
    db.session.commit()
    flash(f"{name} has been added to your contacts!", "success")
    return redirect(url_for('home'))

# Optional: Delete contact (bonus feature)
@app.route('/delete_contact/<int:id>')
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash(f"{contact.full_name} has been removed from contacts.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

