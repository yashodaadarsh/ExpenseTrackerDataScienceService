from flask import Flask, request, jsonify
from service.messageService import MessageService
from kafka import KafkaProducer
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')

messageService = MessageService()
producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/v1/ds/message', methods=['POST'])
def handle_message():
    message = request.json.get('message')
    result = messageService.process_message(message)
    producer.send('expense_service',result)
    return jsonify(result)

@app.route('/', methods=['GET'])
def handle_get():
    return "Hello World"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8093, debug=False)
