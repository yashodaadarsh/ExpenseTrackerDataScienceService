from flask import Flask, request, jsonify
from service.messageService import MessageService
from kafka import KafkaProducer

app = Flask(__name__)
app.config.from_pyfile('config.py')

messageService = MessageService()
# producer = KafkaProducer(boo)

@app.route('/v1/ds/message', methods=['POST'])
def handle_message():
    message = request.json.get('message')
    result = messageService.process_message(message)
    return jsonify(result)

@app.route('/', methods=['GET'])
def handle_get():
    return "Hello World"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8093, debug=False)
