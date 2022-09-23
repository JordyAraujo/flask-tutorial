# Tutorial __Flask__

> Este repositório tem como objetivo reproduzir o [tutorial da documentação do __Flask__](https://flask.palletsprojects.com/en/2.2.x/tutorial/), comentando, pesquisando, estudando e principalmente traduzindo para o português, na intenção de trazer conhecimento de forma didática e acessível.

O tutorial passa pela criação de um _blog_ chamado _Flaskr_. A ideia é que usuários possam se registrar, logar e criar, editar ou deletar _posts_. Também será possível empacotar e instalar a aplicação em outros computadores.
Alguns comentários são feitos na primeira página e eu resolvi traduzí-los diretamente aqui:

- Assumimos que você já é familiar com __Python__. O [tutorial oficial](https://docs.python.org/pt-br/3/tutorial/) na documentação do __Python__ é uma boa forma de aprender ou revisar primeiro;
- Apesar de ser pensado para dar um bom ponto de partida, este tutorial não cobre todas as características e ferramentas do __Flask__. Dá uma olhada no [_Quickstart_](https://flask.palletsprojects.com/en/2.2.x/quickstart/) para ver mais do que o __Flask__ pode fazer, e então mergulhe na documentação para encontrar ainda mais. O tutorial também só usa o que é dado pelo __Python__ e pelo __Flask__ em si. Em outros projetos, você pode decidir usar as [Extensões](https://flask.palletsprojects.com/en/2.2.x/extensions/) do __Flask__ ou outras bibliotecas para facilitar algumas atividades;
- O __Flask__ é flexível. Ele não requer que você use nenhum projeto ou estrutura particular. Porém, quando estamos começando, ajuda se formos mais estruturados e organizados. Portanto, o tutorial vai seguir uma certa estrutura, para evitar certas "armadilhas" ou "vícios" que podem ser encontrados por iniciantes, além de criar um projeto fácil de expandir. À medida que ficar mais confortável com o __Flask__, você poderá sair dessa estrutura e tirar maior proveito da flexibilidade do __Flask__;
- [O projeto completo do tutorial está disponível como exemplo no repositório do __Flask__](https://github.com/pallets/flask/tree/main/examples/tutorial), caso queira comparar com o nosso, à medida que proseguimos.

## Estrutura do Projeto

Crie um repositório e entre nele:

```bash
$ mkdir flask-tutorial
$ cd flask-tutorial
```

Siga as [instruções de instalação](https://flask.palletsprojects.com/en/2.2.x/installation/) para configurar um ambiente virtual __Python__ e instalar o __Flask__ pro seu projeto.

Após instalar, rode o seguinte comando:

```bash
$ pip freeze > requirements.txt
```

Isso vai criar o arquivo ```requirements.txt```, contendo as bibliotecas instaladas até então no seu ambiente virtual, com suas respectivas versões. Se você instalou apenas o __Flask__, note que outras bibliotecas foram adicionadas, pois são auxiliares ao __Flask__. Você pode deixar apenas o __Flask__ na lista, mas as outras serão instaladas com ele da mesma forma.

> Para instalar bibliotecas salvas dessa maneira, use o comando ```$ pip install -r requirements.txt```

A partir de agora o tutorial vai considerar que você está trabalhando do diretório ```flask-tutorial```. Os nomes dos arquivos acima de cada bloco de código serão relativosa este local.

### Uma aplicação __Flask__ pode ser tão simples quanto um arquivo.

> _hello.py_
```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'
```

Porém, conforme o projeto vai crescendo, fica quase impossível manter o controle de muito código em um só arquivo. Projetos em __Python__ usam pacotes para organizar código em múltiplos módulos que podem ser importados onde neessários, e nós não faremos diferente.

O diretório do projeto irá conter:

- ```flaskr/```, um pacote contendo nossa aplicação e seus arquivos;
- ```tests/```, um diretório com os módulos de teste;
- ```.venv/```, nosso ambiente virtual;
- ```requirements.txt```, com as bibliotecas que usaremos (basicamente o __Flask__ nesse caso);
- Arquivos de instalação, dizendo para o __Python__ como instalar seu projeto;
- Configurações de controle de versão (como o Git).

No final, a estrutura do projeto será mais ou menos assim:

```
/home/user/Projects/flask-tutorial
├── flaskr/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── .venv/
├── setup.py
└── MANIFEST.in
```

## Configurando a aplicação

Uma aplicação __Flask__ nada mais é do que uma instância da classe __[Flask](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask)__. Todas as informações da aplicação, bem como configurações e URLs, serão registradas nesta classe.

A forma mais direta de se criar uma aplicação em __Flask__ é criando uma instância global no topo do código, assim como fizemos no arquivo ```hello.py```. Isso pode ser simples e útil, mas pode causar complicações conforme o projeto evolui.

Ao invés de criar uma instância global, vamos criá-la dentro de uma função. Essa função é chamada de _Application Factory_, ou _função construtora_. Quaisquer configurações, registros ou outras definições devem ser feitos dentro desta função, e então a aplicação será retornada.

### A tal da _Application Factory_

Então vamos _codar_! Comece deletando o arquivo ```hello.py```. Ele não nos será útil. Depois crie o diretório ```flaskr``` e o arquivo ```__init__.py```. Este arquivo tem duas funções: conter a _Factory_ e dizer pro __Python__ que o diretório ```flaskr``` deve ser tratado como um pacote.

```bash
$ mkdir flaskr
```

> _flaskr/\_\_init\_\_.py_
```python
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
```

Iremos adicionar mais coisas à função ```create_app```, mas por hora ela já faz bastante coisa:

1. A instância do __Flask__ é criada no comando ```app = Flask(__name__, instance_relative_config=True)```.
   
   - ```__name__``` é o nome do módulo __Python__ atual. A aplicação precisa saber onde ele está localizado, para configurar alguns caminhos, e ```__name__``` é uma forma interessante de dizer isso.
   
   - ```instance_relative_config=True``` diz à aplicação que os arquivos de configuração são relativos ao [diretório de instância](https://flask.palletsprojects.com/en/2.2.x/config/#instance-folders). O diretório de instância fica localizado fora do pacote ```flaskr``` e pode guardar dados que não devem ser commitados, como segredos de configuração e o arquivo de banco de dados.

2. [app.config.from_mapping()](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Config.from_mapping) define algumas configurações padrão que a aplicação irá usar:

   - [SECRET_KEY](https://flask.palletsprojects.com/en/2.2.x/config/#SECRET_KEY) é usada pelo __Flask__ e suas extensões para manter dados seguros. Aqui setamos para ```'dev'``` para usar um valor conveniente durante o desenvolvimento, mas deve ser substituída por um valor aleatório ao subir para produção.
   - ```DATABASE``` é o caminho onde o arquivo de banco _SQLite_ será salvo. Está localizado em [app.instance_path](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.instance_path), que é o caminho que o __Flask__ escolheu para seu diretório de instância. Veremos mais sobre banco de dados na próxima sessão.

3. [app.config.from_pyfile()](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Config.from_pyfile) substitui as configurações padrão com os valores no arquivo ```config.py```, localizado no diretório de instância, se ele existir. Por exemplo, isso pode ser usado ao fazer deploy, para definir um valor real para ```SECRET_KEY```.

   - ```test_config``` também pode ser passado à _factory_ e será usado no lugar da configuração de instância. Assim, os testes que vamos escrever mais pra frente no tutorial, podem ser configurados independente dos valores escolhidos durante o desenvolvimento.

4. [os.makedirs()](https://docs.python.org/3/library/os.html#os.makedirs) garante que [app.instance_path()](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.instance_path) existe. O __Flask__ não cria o diretório de instância automaticamente, mas precisamos criar para que o arquivo do banco _SQLite_ seja criado lá dentro.

5. [@app.route()](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.route) cria uma rota simples para que você possa ver a aplicação rodando antes de ver o resto do tutorial. Aqui criamos uma conexão entre a _URL_ ```/hello``` e a função que retorna uma resposta, neste caso, a string ```'Hello,World!'```.

### Rodando a aplicação

Agora podemos rodar nossa aplicação com o comando ```flask```. Do terminal, diremos ao __Flask__ onde achar nossa aplicação e rodá-la em modo de _debug_. Lembre-se, você ainda deve estar no diretório ```flask-tutorial```, não no pacote ```flaskr```.

O modo de _debug_ nos mostra um debugador interativo sempre que a página levanta uma excessão, e reinicia o servidor sempre que fazemos alterações no código. Você pode deixar ele rodando e é só recarregar as páginas conforme avança no código pelo tutorial.

```bash
$ flask --app flaskr --debug run
```

O retorno deve ser parecido com isso:

```bash
* Serving Flask app "flaskr"
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: nnn-nnn-nnn
```

Visite http://127.0.0.1:5000/hello num navegador que você verá a mensagem "Hello, World!". Parabéns, você está rodando sua aplicação __Flask__!

> Se outra aplicação já estiver utilizando a porta 5000, você verá um erro ```OSError: [Errno 98]``` ou ```OSError: [WinError 10013]``` quando o servidor tenta iniciar. Veja a documentação sobre [endereço em uso](https://flask.palletsprojects.com/en/2.2.x/server/#address-already-in-use) para ver como lidar com isso (ou apenas para a outra aplicação, se não for gerar problema).

## Definindo e acessando o Banco de Dados

A aplicação vai usar um banco _[SQLite](https://sqlite.org/about.html)_ pra guardar usuários e _posts_. O próprio __Python__ já tem suporte nativo pro _SQLite_ com o módulo [sqlite3](https://docs.python.org/3/library/sqlite3.html#module-sqlite3).

O _SQLite_ é conveniente por não precisar de um banco rodando separado em outro servidor. Porém, se requisições concorrentes tentarem escrever ao mesmo tempo no banco, elas serão mais demoradas, pois cada escrita acontece individualmente. Pequenas aplicações não vão notar diferença. Conforme seu uso cresce, será melhor trocar para outro banco.

> O tutorial não entra em detalhes sobre SQL. Se você não é familiar, a [documentação do _SQLite_](https://sqlite.org/lang.html) descreve bem a linguagem.

### Conectando ao Banco de Dados

A primeira coisa a se fazer quando se trabalha com _SQLite_ (e várias outras bibliotecas de banco em __Python__) é criar uma conexão com ele. Quaisquer consultas e operações acontecem usando a conexão, que é fechada epois que o trabalho termina.

Em aplicações web essas conexões são tipicamente amarradas à requisição. Ela é criada em algum ponto durante o processamento da requisição, e fechada antes da resposta ser enviada.

> _flaskr/db.py_

```python
import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
```

[g](https://flask.palletsprojects.com/en/2.2.x/api/#flask.g) é um objeto especial único para cda requisição. Ele é utilizado para guardar dados que poderão ser acessados por múltiplas funções durante a requisição. A conexão é criada e reutilizada, ao invés de de criar uma nova conexão sempre que ```get_db``` for chamada na mesma requisição.

[current_app](https://flask.palletsprojects.com/en/2.2.x/api/#flask.current_app) é outro objeto especial que aponta para a aplicação __Flask__ que está lidando com a requisição. Uma vez que utilizamos uma _função construtora_, o objeto da aplicação não existe quando estamos escrevendo o resto do código. ```get_db``` será chamada depois que a aplicação já foi criada e está lidando com uma requisição, portanto [current_app](https://flask.palletsprojects.com/en/2.2.x/api/#flask.current_app) pode ser usado.

[sqlite3.connect()](https://docs.python.org/3/library/sqlite3.html#sqlite3.connect) estabelece uma conexão com o arquivo apontado pela chave de configuração ```DATABASE```. Este arquivo não precisa existir agora, e não irá, até que inicializemos o banco de dados mais à frente.

[sqlite3.Row](https://docs.python.org/3/library/sqlite3.html#sqlite3.Row) diz à conexão para retornar linhas que funcionam como dicionários. Isso nos permite acessar colunas por nome.

```close_db``` checa se uma conexão foi criada conferindo se existe um ```g.db```. Se a conexão existe, é fechada. Mais à frente iremos mencionar ```close_db``` na _função construtora_, para que seja chamada após cada requisição.

### Criando as tabelas

No _SQLite_, os dados são guardados em _tabelas_ e _colunas_. Estes precisam ser criados antes que possamos guardar ou acessar dados. _Flaskr_ irá salvar dados de usuários na tabela _```user```_, e _posts_ na tabela _```posts```_. Criaremos um arquivo com os comandos SQL necessários para criar as tabelas vazias:

> _flaskr/schema.sql_

```sql
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
```

Agora vamos adicionar as funções que vão executar esses comandos SQL ao arquivo ```db.py```:

> _flaskr/db.py_

```python
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
```

[open_resource()](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.open_resource) abre um arquivo relativo ao pacote ```flaskr```, o que é útil já que nós não necessariamente saberemos onde fica isso quando fizermos _deploy_ da aplicação mais tarde. ```get_db``` retorna uma conexão com o banco de dados, que é usada para executar os comandos lidos no arquivo.

[click.command()](https://click.palletsprojects.com/en/8.1.x/api/#click.command) define um comando de linha de comando chamado ```init-db```, que chama a função ```init_db``` e mostra uma mensagem de sucesso para o usuário. Você pode consultar [Interface de Linha de Comando](https://flask.palletsprojects.com/en/2.2.x/cli/) para aprender mais sobre escrever seus próprios comandos.

### Registrando com a aplicação

As funções ```close_db``` e ```init_db_command``` precisam ser registradas na instância da aplicação; caso contrário, elas não serão usadas pela aplicação. Porém, como estamos usando uma _função construtora_, esta instãncia não está disponível quando estamos escrevendo as funções. Ao invés disso, criaremos uma função que recebe a aplicação como parâmetro e faz o registro.

> _flaskr/db.py_

```python
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
```

```app.teardown_appcontext()``` diz ao __Flask__ para chamar esta função depois que a requisição termina de ser processada, após retornar a resposta. 

```app.cli.add_command()``` adiciona um novo comando que pode ser chamado no terminal com o comando ```flask```.

Importe e chame essa função dentro da construtora. Coloque o novo código na _função construtora_.

> _flaskr/\_\_init\_\_.py_

```python
import os

from flask import Flask
from . import db


def create_app(test_config=None):
    # Cria e configura a aplicação
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    db.init_app(app)

    # Código existente omitido


    return app
```

### Inicie o arquivo de Banco de Dados

Agora que ```init-db``` foi registrado no app, ele pode ser chamado usando o comando ```flask```, assim como o comando ```run``` usado anteriormente.

> Se você ainda está rodando o servidor, você pode pará-lo agora, ou rodar esse comando em um novo terminal. Se você vai usar um novo terminal, não esqueça de entrar no diretório e ativar seu ambiente virtual, como descrito [aqui](https://flask.palletsprojects.com/en/2.2.x/installation/).

Rode o comando ```init-db```:

```bash
$ flask --app flaskr init-db
Initialized the database.
```

Um arquivo ```flaskr.sqlite``` será criado no diretório de instância do seu projeto.

## _Blueprints_ e _Views_

Uma _view_ é o código que você escreve para responder a requisições feitas à sua aplicação. O __Flask__ usa padrões para comparar a _URL_ da requisição com a _view_ que irá processá-la. A _view_ retorna dados que o __Flask__ converte numa resposta. O __Flask__ também pode ir em outra direção e gerar uma _URL_ para a _view_ baseado em seu nome e argumentos.

### Criando uma _Blueprint_

Uma _[Blueprint](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Blueprint)_ é uma forma de organizar um grupo de _views_ relacionadas e outros códigos. Ao invés de registrar _views_ e outros códigos direto em uma aplicação, eles são registrados com uma _blueprint_. Então a _blueprint_ é registrada com a aplicação quando está disponível na _função construtora_.

_Flaskr_ terá duas _blueprints_, uma para funções de autenticação e uma para as funções sobre os _posts_. O código para cada _blueprint_ irá num módulo diferente. Uma vez que o _blog_ precisa fazer autenticação, vamos escrever suas funções primeiro.

> _flaskr/auth.py_

```python
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
```

Isso cria uma _[Blueprint](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Blueprint)_ chamada ```auth```. Assim como o objeto da aplicação, a _blueprint_ precisa saber onde é definida, então ```__name__``` é passado como segundo argumento. O prefixo ```url_prefix``` será adicionado ao início de todas as _URLs_ associadas com a _blueprint_.

Importamos e registramos a _blueprint_ na _construtora_ usando a função [app.register_blueprint()](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.register_blueprint). Colocaremos o novo código na _função construtora_:

> _flaskr/\_\_init\_\_.py_

```python
import os

from flask import Flask
from . import db
from . import auth


def create_app(test_config=None):
    # Cria e configura a aplicação
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    db.init_app(app)
    app.register_blueprint(auth.bp)
    # Código existente omitido


    return app
```

A _blueprint_ de autenticação terá _views_ para registrar novos usuários, bem como _login_ e _logout_.

### Nossa primeira _view_: _register_

Quando usuários visitam a _URL_ ```/auth/register```, a _view_ ```register``` vai retornar um _[HTML](https://developer.mozilla.org/docs/Web/HTML)_ com um formulário a ser preenchido. Ao submeter o formulário, as entradas serão validadas e dependendo da validação, o usuário será criado e seremos redirecionados à pagina de _login_, ou o formulário será recarregado com uma mensagem de erro, se for o caso.

Por enquanto vamos escrever o código da _view_. Mais na frente iremos escrever os _templates_ para gerar o _HTML_ do formulário.

> _flaskr/auth.py_

```python
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')
```

Vamos ver o que a função ```register``` faz:

1. [@bp.route](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Blueprint.route) associa a _URL_ ```/register``` à função _view_ ```register```. Quando o _Flask_ recebe uma requisição para ```/auth/register```, ele chama a _view_ ```register``` e usa seu retorno como resposta.

2. Se o usuário submeteu o formulário, o método da requisição ([request.method](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Request.method)) será ```'POST'```. Neste caso, começamos a validar a entrada.

3. [request.form](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Request.form) é um tipo especial de [dicionário](https://docs.python.org/3/library/stdtypes.html#dict) que mapeia as chaves e valores do formulário submetido. O usuário vai preencher seus ```username``` e ```password```.

4. Validamos que ```username``` e ```password``` não estão vazios.

5. Se a validação suceder, inserimos o novo usuário no banco de dados.

   - [db.execute](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.execute) recebe uma instrução _SQL_ com parâmetros representados por ```?``` para entradas do usuário, e uma tupla de valores que os preencherão na ordem fornecida. A biblioteca de banco irá cuidar de converter as _strings_ para que não fiquemos vulneráveis a _ataques de injeção de SQL_
   - Por segurança, senhas nunca devem ser salvas diretamente no banco de dados. Ao invés disso, a função [generate_password_hash()](https://werkzeug.palletsprojects.com/en/2.2.x/utils/#werkzeug.security.generate_password_hash) é usada para criptografar seguramente a senha. Essa senha criptografada é que será salva. Como esta instrução modifica dados, a função [db.commit()](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.commit) precisa ser chamada para salvar as alterações.
   - Um erro [sqlite3.IntegrityError](https://docs.python.org/3/library/sqlite3.html#sqlite3.IntegrityError) irá ocorrer se o _username_ já existe, o que deve ser mostrado para o usuário como um erro de validação.

6. Depois de salvar o usuário, somos redirecionados para a página de login. [url_for()](https://flask.palletsprojects.com/en/2.2.x/api/#flask.url_for) gera a URL para a _view_  de login baseado em seu nome. É preferível usar esse método ao invés de escrever a URL diretamente, pois assim podemos mudar a URL depois sem precisar mudar todo o código relacionado. [redirect()](https://flask.palletsprojects.com/en/2.2.x/api/#flask.redirect) gera uma resposta de redirecionamento para a URL gerada.

7. Se a validação falhar, o erro é mostrado para o usuário. [flash()](https://flask.palletsprojects.com/en/2.2.x/api/#flask.flash) salva informações que podem ser recuperadas quando renderizando o template.

8. Quando o usuário navega inicialmente para ```auth/register```, ou acontece um erro de validação, uma página HTML com o formulário de registro deve ser mostrada. [render_template()](https://flask.palletsprojects.com/en/2.2.x/api/#flask.render_template) irá renderizar um template contendo o HTML que iremos escrever nas próximas etapas.

### Login

Esta _view_segue o mesmo padrão que a _view_ de _register_ acima.

> _flaskr/auth.py_

```python
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')
```

Aqui vemos algumas diferenças da _view_ ```register```:

1. O usuário é consultado primeiro e salvo em uma variável para usarmos depois.
    [fetchone()](https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.fetchone) retorna uma linha da consulta. Se a consulta não retornar resultados, retorna ```None```. Usaremos [fetchall()](https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.fetchall) depois, para retornar uma lista com todos os resultados.

2. [check_pasword_hash()](https://werkzeug.palletsprojects.com/en/2.2.x/utils/#werkzeug.security.check_password_hash) criptografa a senha submetida da mesma forma que a criptografada salva no banco e as compara seguramente. Se forem iguais, a senha é válida.

3. [session](https://flask.palletsprojects.com/en/2.2.x/api/#flask.session) é um [dicionário](https://docs.python.org/3/library/stdtypes.html#dict) que guarda dados entre requisições. Que a validação é bem sucedida, o ```id``` do usuário é guardado em uma nova sessão. Os dados são guardado em um _cookie_ que é enviado para o navegador, que as manda de volta nas próximas requisições. O próprio Flask _assina_ os dados seguramente para que não possam ser adulterados.

Agora que o ```id``` do usuário está salvo na [sessão](https://flask.palletsprojects.com/en/2.2.x/api/#flask.session), ele ficará disponível nas próximas requisições. No início de cada requisição, se um usuário está logado, suas informações devem ser carregadas e estar disponíveis para outras _views_.

> _flaskr/auth.py_

```python
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
```

[bp.before_app_request()](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Blueprint.before_app_request) registra uma função que roda antes da função da _view_, independente da URL requisitada. ```load_logged_in_user```checa se um id de usuário está salvo na [sessão](https://flask.palletsprojects.com/en/2.2.x/api/#flask.session) e pega as informações desse usuário no banco de dados, salvando em [g.user](https://flask.palletsprojects.com/en/2.2.x/api/#flask.g), que tem a duração da requisição. Se não há id de usuário, ou se o id não existe, ```g.user```será ``Ǹone```.

### Logout

Para deslogar, precisamos remover o id do usuário da [sessão](https://flask.palletsprojects.com/en/2.2.x/api/#flask.session).Assim ```load_logged_in_user``` não irá carregar um usuário nas próximas requisições.

> _flaskr/auth.py_

```python
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
```

### Solicitando autenticação em outras _views_

Criar, editar e deletar _posts_ no _blog_ só deverá ser possível com um usuário logado. Um _decorador_ pode ser usado para checar isso em cada _view_ em que o aplicarmos.

> _flaskr/auth.py_

```python
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
```

Este _decorador_ retorna uma nova função _view_ que envolve a _view_original na qual é aplicada. A nova função checa se um usuário foi carregadoe redireciona para a página de login em caso negativo. Se um usuário foi carregado, a _view_ original é chamada e continua normalmente. Usaremos este decorador quando escrevermos as _views_ do _blog_.

### _Endpoints_ e URLs

A função [url_for()](https://flask.palletsprojects.com/en/2.2.x/api/#flask.url_for) gera a URL para a _view_ em um nome e argumentos. O nome associado com a _view_ também é chamado de _endpoint_, e por padrão tem o mesmo nome da função da _view_.

Por exemplo, a _view_ ```hello()``` que foi adicionada à  _função construtora_ mais cedo no tutorial tem o nome ```'hello'``` e pode ser referenciada com ```url_for('hello')```. Se ela recebe um argumento, o que veremos depois, usamos a sintaxe ```url_for('hello', who='World')```.

Quando usamos uma _blueprint_, o nome dela deve ser adicionado ao nome da função, assim o _endpoint_ para a função ```login``` que escrevemos será ```'auth.login'``` pois o adicionamos à _blueprint_ ```'auth'```.