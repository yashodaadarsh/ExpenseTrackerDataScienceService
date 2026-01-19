from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
import os

from app.service.messageService import MessageService


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    kafka_host = os.getenv('KAFKA_HOST', 'localhost')
    kafka_port = os.getenv('KAFKA_PORT', '9092')
    kafka_bootstrap_servers = f"{kafka_host}:{kafka_port}"
    kafka_topic = os.getenv('KAFKA_TOPIC', 'expense_service')

    print(f"Kafka Bootstrap Servers: {kafka_bootstrap_servers}")

    message_service = MessageService()
    producer = KafkaProducer(
        bootstrap_servers=kafka_bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    @app.route('/v1/ds/message', methods=['POST'])
    def handle_message():
        user_id = request.headers.get('x-user-id')
        if not user_id:
            return jsonify({'error': 'x-user-id header is required'}), 400

        payload = request.json or {}
        message = payload.get('message')

        result = message_service.process_message(message)
        print("result :-", result)

        if result is not None:
            result['user_id'] = user_id
            producer.send(kafka_topic, result)
            return jsonify(result)

        return jsonify({'error': 'Invalid message format'}), 400

    @app.route('/', methods=['GET'])
    def handle_get():
        return 'Hello world'

    @app.route('/health', methods=['GET'])
    def health_check():
        return 'OK'

    return app
