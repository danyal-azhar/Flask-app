from flask import Flask
from routes import main
from config import Config
from extensions import mysql

app = Flask(__name__)
app.config.from_object(Config)
mysql.init_app(app)
app.register_blueprint(main)

if __name__ == '__main__':
    app.run()
