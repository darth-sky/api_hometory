"""Small apps to demonstrate endpoints with basic feature - CRUD"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import jwt
from api.books.endpoints import books_endpoints
from api.auth.endpoints import auth_endpoints
from api.data_protected.endpoints import protected_endpoints
from api.ruangan.endpoints import ruangan_endpoints
from api.container.endpoints import container_endpoints
from api.barang_dlm_ruangan.endpoints import barang_dlm_ruangan_endpoints
from api.barang_dlm_container.endpoints import barang_dlm_container_endpoints
from api.pengguna.endpoints import pengguna_endpoints
from config import Config
from static.static_file_server import static_file_server

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)


jwt.init_app(app)

# register the blueprint
app.register_blueprint(auth_endpoints, url_prefix='/api/v1/auth')
app.register_blueprint(protected_endpoints,
                       url_prefix='/api/v1/protected')
app.register_blueprint(books_endpoints, url_prefix='/api/v1/books')
app.register_blueprint(static_file_server, url_prefix='/static/')
app.register_blueprint(ruangan_endpoints, url_prefix='/api/v1/ruangan')
app.register_blueprint(barang_dlm_ruangan_endpoints, url_prefix='/api/v1/barang_dlm_ruangan')
app.register_blueprint(barang_dlm_container_endpoints, url_prefix='/api/v1/barang_dlm_container')
app.register_blueprint(pengguna_endpoints, url_prefix='/api/v1/pengguna')
app.register_blueprint(container_endpoints, url_prefix='/api/v1/container')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
