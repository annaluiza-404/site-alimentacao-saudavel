import config
import db
from flask import Flask, jsonify
from flask_cors import CORS
from utils.erros import ApiErro
from routes.auth import bp_auth
from routes.frete import bp_frete
from routes.pedidos import bp_pedidos
from routes.catalogo import bp_catalogo
from routes.receitas import bp_receitas
from routes.arquivos import bp_arquivos

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5000"])

config.carregar(app)
db.init_app(app)


@app.errorhandler(ApiErro)
def tratar_api_erro(e):
    return jsonify({'erro': e.mensagem}), e.status


app.register_blueprint(bp_auth, url_prefix='/api')
app.register_blueprint(bp_frete, url_prefix='/api')
app.register_blueprint(bp_pedidos, url_prefix='/api')
app.register_blueprint(bp_catalogo, url_prefix='/api')
app.register_blueprint(bp_receitas, url_prefix='/api')
app.register_blueprint(bp_arquivos)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
