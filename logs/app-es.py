import logging
from logging.handlers import RotatingFileHandler
from flask import Flask,jsonify,request
from elasticsearch import Elasticsearch

app = Flask(__name__)

# Set the log level to capture the desired messages
app.logger.setLevel(logging.INFO)

# Define the log file and its properties
log_file = 'app.log'
handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=1)

# Set the log format
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)

# Add the log handler to the Flask application
app.logger.addHandler(handler)


# Configure Flask to use the logging module for its internal logs
app.logger.removeHandler(app.logger.handlers[0])  # Remove the default Flask log handler
app.logger.addHandler(logging.StreamHandler())  # Add a handler to redirect logs to the logging module

@app.errorhandler(Exception)
def handle_exception_error(e):
    app.logger.error('Exception occurred: %s', str(e))
    return jsonify(error='Internal Server Error'), 500

# Create an Elasticsearch client
es_client = Elasticsearch(hosts=['http://172.31.31.143:9200'])

# Define a custom logging handler to send logs to Elasticsearch
class ElasticsearchHandler(logging.Handler):
    def emit(self, record):
        # Create a log document to be indexed in Elasticsearch
        log_document = {
            'message': self.format(record),
            'level': record.levelname,
            'path': record.pathname,
            'line': record.lineno
        }
        # Index the log document in Elasticsearch
        es_client.index(index='app-logs', body=log_document)

# Create an instance of the custom logging handler
es_handler = ElasticsearchHandler()

# Set the log level and add the Elasticsearch handler to the Flask application's logger
app.logger.setLevel(logging.INFO)
app.logger.addHandler(es_handler)

@app.route('/')
def index():
    app.logger.info('Hello, world!')
    return 'Hello, world!'


if __name__ == '__main__':
    app.run('0.0.0.0',60,debug=True)
