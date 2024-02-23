from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
conn = sqlite3.connect('messaging_system.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS conversations (
             id INTEGER PRIMARY KEY,
             name TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS messages (
             id INTEGER PRIMARY KEY,
             conversation_id INTEGER,
             content TEXT,
             FOREIGN KEY(conversation_id) REFERENCES conversations(id))''')

conn.commit()

# Routes
# Load conversations
@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    c.execute("SELECT id, name FROM conversations")
    conversations = c.fetchall()
    return jsonify([{'id': conv[0], 'name': conv[1]} for conv in conversations])

# Load messages for a conversation
@app.route('/api/messages', methods=['GET'])
def get_messages():
    conversation_id = request.args.get('conversationId')
    c.execute("SELECT content FROM messages WHERE conversation_id=?", (conversation_id,))
    messages = c.fetchall()
    return jsonify([{'content': msg[0]} for msg in messages])

# Send a message
@app.route('/api/sendMessage', methods=['POST'])
def send_message():
    data = request.json
    conversation_id = data['conversationId']
    content = data['content']
    c.execute("INSERT INTO messages (conversation_id, content) VALUES (?, ?)", (conversation_id, content))
    conn.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)