from prometheus_client import make_wsgi_app, Counter
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask

# Step 3: Define Prometheus Metrics
REQUEST_COUNT = Counter('flask_app_request_count', 'Total number of requests')

# Step 5: Instrument Your Flask Routes
app = Flask(__name__)

@app.route('/hello')
def hello():
    REQUEST_COUNT.inc()
    return 'Hello, world!'

# Step 6: Create Prometheus WSGI Middleware
app_dispatch = DispatcherMiddleware(app, {
    '/metrics': make_wsgi_app()
})

# Step 7: Run the Flask Application
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, app_dispatch)
