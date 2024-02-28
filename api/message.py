from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource
from model.messages import Message
from __init__ import app, db

message_api = Blueprint('message_api', __name__, url_prefix='/api/message')
api = Api(message_api)

class MessageAPI(Resource):
    def post(self):
        data = request.get_json()
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        content = data.get('content')

        if sender_id is None or receiver_id is None or content is None:
            return jsonify({'message': 'sender_id, receiver_id, and content are required'}), 400

        new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
        db.session.add(new_message)
        db.session.commit()

        return jsonify(new_message.serialize()), 201

    def get(self):
        sender_id = request.args.get('sender_id')
        receiver_id = request.args.get('receiver_id')

        if sender_id and receiver_id:
            messages = Message.query.filter_by(sender_id=sender_id, receiver_id=receiver_id).all()
        else:
            messages = Message.query.all()

        return jsonify([message.serialize() for message in messages])

api.add_resource(MessageAPI, '/')

# Routes
# @app.route('/api/conversations', methods=['GET'])
# def get_conversations():
#     conversations = Message.query.with_entities(Message.conversation_id, Message.conversation_name).distinct().all()
#     return jsonify([{'id': conv[0], 'name': conv[1]} for conv in conversations])

# @app.route('/api/messages', methods=['GET'])
# def get_messages():
#     conversation_id = request.args.get('conversation_id')
#     if conversation_id:
#         messages = Message.query.filter_by(conversation_id=conversation_id).all()
#         return jsonify([{'content': msg.content} for msg in messages])
#     else:
#         return jsonify({'message': 'conversation_id is required'}), 400

# @app.route('/api/sendMessage', methods=['POST'])
# def send_message():
#     data = request.json
#     conversation_id = data.get('conversation_id')
#     content = data.get('content')

#     if conversation_id is None or content is None:
#         return jsonify({'message': 'conversation_id and content are required'}), 400

#     new_message = Message(conversation_id=conversation_id, content=content)
#     new_message.create()

#     return jsonify({'message': 'Message sent successfully'}), 201





