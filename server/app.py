from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)



@app.route('/messages',methods=["GET"])
def messages():       
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_list = [message.to_dict() for message in messages]
        return jsonify(messages_list), 200
    
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.json
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"id": new_message.id, "body": new_message.body, "username": new_message.username, "created_at": new_message.created_at, "updated_at": new_message.updated_at})

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.json
    message.body = data['body']
    message.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({"id": message.id, "body": message.body, "username": message.username, "created_at": message.created_at, "updated_at": message.updated_at})
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Message deleted successfully"})

       
  

if __name__ == '__main__':
    app.run(port=5555)
