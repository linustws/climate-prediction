from flask import Flask
from flask_cors import CORS

from models import cache

app = Flask(__name__)
CORS(app)

cache.init_app(app)

if __name__ == '__main__':
    from routes import routes

    app.register_blueprint(routes)
    app.run(debug=False)
