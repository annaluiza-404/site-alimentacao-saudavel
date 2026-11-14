from flask import Flask
from routes.auth import bp_auth
from routes.frete import bp_frete
from routes.pedidos import bp_pedidos
from routes.catalogo import bp_catalogo

app = Flask(__name__)

app.register_blueprint(bp_auth, url_prefix='/api')
app.register_blueprint(bp_frete, url_prefix='/api')
app.register_blueprint(bp_pedidos, url_prefix='/api')
app.register_blueprint(bp_catalogo, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)