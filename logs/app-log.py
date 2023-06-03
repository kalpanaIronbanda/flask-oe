import logging
from logging.handlers import RotatingFileHandler
from flask import Flask,jsonify,request

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


@app.route('/')
def index():
    app.logger.info('Hello, world!')
    return 'Hello, world!'


if __name__ == '__main__':
    app.run('0.0.0.0',60,debug=True)
