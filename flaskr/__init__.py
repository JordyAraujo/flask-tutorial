import os

from flask import Flask


def create_app(test_config=None):
    # Cria e configura a aplicação
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Carrega as configurações da instância, quando existem e quando não testando
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Carrega as configurações de teste
        app.config.from_mapping(test_config)

    # Garante que o diretório da instância existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Uma página simples que diz Olá
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app