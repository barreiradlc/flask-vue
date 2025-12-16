from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/flask_vue'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name}

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return jsonify(message="Hello, World!")

# GET request: Retrieve all items
@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

# GET request: Retrieve a specific item by ID
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item.to_dict())

# POST request: Create a new item
@app.route('/api/items', methods=['POST'])
def create_item():
    name = request.json.get('name')
    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    new_item = Item(name=name)
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

# PUT request: Update an existing item
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    
    name = request.json.get('name')
    if name:
        item.name = name
    
    db.session.commit()
    return jsonify(item.to_dict())

# DELETE request: Delete an item
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    
    db.session.delete(item)
    db.session.commit()
    return '', 204

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)