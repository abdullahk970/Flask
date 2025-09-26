from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'devkey'

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()
    print("✅ Database initialized, tables created!")

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    items = Item.query.order_by(Item.id.desc()).paginate(page=page, per_page=6)
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_item = Item(title=title, description=description)
        db.session.add(new_item)
        db.session.commit()
        flash("Item added successfully!", "success")
        return redirect(url_for('index'))
    return render_template('add_item.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.title = request.form['title']
        item.description = request.form['description']
        db.session.commit()
        flash("Item updated successfully!", "success")
        return redirect(url_for('index'))
    return render_template('edit_item.html', item=item)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash("Item deleted successfully!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
