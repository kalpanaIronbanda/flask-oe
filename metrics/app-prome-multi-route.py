from prometheus_client import make_wsgi_app, Counter
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask

# Step 3: Define Prometheus Metrics
REQUEST_COUNT = Counter('flask_app_request_count', 'Total number of requests', ['route'])  # Add the 'route' label

# Step 5: Instrument Your Flask Routes
app = Flask(__name__)

@app.route('/route1')
def route1():
    REQUEST_COUNT.labels(route='/route1').inc()  # Increment the request count for route1
    return 'Hello from route1!'

@app.route('/route2')
def route2():
    REQUEST_COUNT.labels(route='/route2').inc()  # Increment the request count for route2
    return 'Hello from route2!'

# Step 6: Create Prometheus WSGI Middleware
app_dispatch = DispatcherMiddleware(app, {
    '/metrics': make_wsgi_app()
})

# Step 7: Run the Flask Application
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, app_dispatch)
