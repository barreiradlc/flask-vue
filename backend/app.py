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
class Todo(db.Model):
    __tablename__ = 'todos'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def to_dict(self):
        return {
            'id': self.id, 
            'description': self.description,
            'completed': self.completed,
            'createdAt': self.created_at,
        }

# Create tables
with app.app_context():
    # db.drop_all()
    db.create_all()

@app.route('/')
def hello_world():
    return jsonify(message="Hello, World!")

# GET request: Retrieve all todos
@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

# GET request: Retrieve a specific item by ID
@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todo.to_dict())

# POST request: Create a new item
@app.route('/api/todos', methods=['POST'])
def create_todo():
    description = request.json.get('description')
    if not description:
        return jsonify({"error": "description is required"}), 400
    
    new_todo = Todo(description=description)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

# PUT request: Update an existing todo description
@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    
    description = request.json.get('description')
    if description:
        todo.description = description
    
    db.session.commit()
    return jsonify(todo.to_dict())


# PUT request: Update todo completed status
@app.route('/api/todos/check/<int:todo_id>', methods=['PUT'])
def update_todo_status(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    
    completed = request.args.get('completed')
    if completed is not None:
        todo.completed = completed
    else:
        todo.completed = not todo.completed
    
    db.session.commit()
    return jsonify(todo.to_dict())

# DELETE request: Delete an todo
@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    
    db.session.delete(todo)
    db.session.commit()
    return '', 204

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)