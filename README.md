# Tutorial Flask

> Este repositório tem como objetivo reproduzir o [tutorial da documentação do Flask](https://flask.palletsprojects.com/en/2.2.x/tutorial/), comentando, pesquisando, estudando e principalmente traduzindo para o português, na intenção de trazer conhecimento de forma didática e acessível.

O tutorial passa pela criação de um blog chamado Flaskr. A ideia é que usuários possam se registrar, logar e criar, editar ou deletar posts. Também será possível empacotar e instalar a aplicação em outros computadores.
Alguns comentários são feitos na primeira página e eu resolvi traduzí-los diretamente aqui:

- Assumimos que você já é familiar com Python. O [tutorial oficial](https://docs.python.org/pt-br/3/tutorial/) na documentação do Python é uma boa forma de aprender ou revisar primeiro;
- Apesar de ser pensado para dar um bom ponto de partida, este tutorial não cobre todas as características e ferramentas do Flask. Dá uma olhada no [_Quickstart_](https://flask.palletsprojects.com/en/2.2.x/quickstart/) para ver mais do que o Flask pode fazer, e então mergulhe na documentação para encontrar ainda mais. O tutorial também só usa o que é dado pelo Python e pelo Flask em si. Em outros projetos, você pode decidir usar as [Extensões](https://flask.palletsprojects.com/en/2.2.x/extensions/) do Flask ou outras bibliotecas para facilitar algumas atividades;
- O Flask é flexível. Ele não requer que você use nenhum projeto ou estrutura particular. Porém, quando estamos começando, ajuda se formos mais estruturados e organizados. Portanto, o tutorial vai seguir uma certa estrutura, para evitar certas "armadilhas" ou "vícios" que podem ser encontrados por iniciantes, além de criar um projeto fácil de expandir. À medida que ficar mais confortável com o Flask, você poderá sair dessa estrutura e tirar maior proveito da flexibilidade do Flask;
- [O projeto completo do tutorial está disponível como exemplo no repositório do Flask](https://github.com/pallets/flask/tree/main/examples/tutorial), caso queira comparar com o nosso, à medida que proseguimos.

## Estrutura do Projeto

Crie um repositório e entre nele:

```bash
$ mkdir flask-tutorial
$ cd flask-tutorial
```

Siga as [instruções de instalação](https://flask.palletsprojects.com/en/2.2.x/installation/) para configurar um ambiente virtual Python e instalar o Flask pro seu projeto.

Após instalar, rode o seguinte comando:

```bash
$ pip freeze > requirements.txt
```

Isso vai criar o arquivo ```requirements.txt```, contendo as bibliotecas instaladas até então no seu ambiente virtual, com suas respectivas versões. Se você instalou apenas o Flask, note que outras bibliotecas foram adicionadas, pois são auxiliares ao Flask. Você pode deixar apenas o Flask na lista, mas as outras serão instaladas com ele da mesma forma.

> Para instalar bibliotecas salvas dessa maneira, use o comando ```$ pip install -r requirements.txt```

A partir de agora o tutorial vai considerar que você está trabalhando do diretório ```flask-tutorial```. Os nomes dos arquivos acima de cada bloco de código serão relativosa este local.

### Uma aplicação Flask pode ser tão simples quanto um arquivo.

>_hello.py_
```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'
```

Porém, conforme o projeto vai crescendo, fica quase impossível manter o controle de muito código em um só arquivo. Projetos em Python usam pacotes para organizar código em múltiplos módulos que podem ser importados onde neessários, e nós não faremos diferente.

O diretório do projeto irá conter:

- ```flaskr/```, um pacote contendo nossa aplicação e seus arquivos;
- ```tests/```, um diretório com os módulos de teste;
- ```.venv/```, nosso ambiente virtual;
- ```requirements.txt```, com as bibliotecas que usaremos (basicamente o Flask nesse caso);
- Arquivos de instalação, dizendo para o Python como instalar seu projeto;
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

Uma aplicação Flask nada mais é do que uma instância da classe Flask. Todas as informações da aplicação, bem como configurações e URLs, serão registradas nesta classe.

A forma mais direta de se criar uma aplicação em Flask é criando uma instância global no topo do código, assim como fizemos no arquivo ```hello.py```. Isso pode ser simples e útil, mas pode causar complicações conforme o projeto evolui.

Ao invés de criar uma instância global, vamos criá-la dentro de uma função. Essa função é chamada de _Application Factory_, algo do tipo _fábrica da aplicação_, mas vamos apelidá-la de _Factory_ pra ficar mais fácil. Quaisquer configurações, registros ou outras definições devem ser feitos dentro desta função, e então a aplicação será retornada.

### A tal da _Application Factory_

Então vamos _codar_! Comece deletando o arquivo ```hello.py```. Ele não nos será útil. Depois crie o diretório ```flaskr``` e o arquivo ```__init__.py```. Este arquivo tem duas funções: conter a _Factory_ e dizer pro Python que o diretório ```flaskr``` deve ser tratado como um pacote.

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

1. A instância do Flask é criada no comando ```app = Flask(__name__, instance_relative_config=True)```.
   
   - ```__name__``` é o nome do módulo Python atual. A aplicação precisa saber onde ele está localizado, para configurar alguns caminhos, e ```__name__``` é uma forma interessante de dizer isso.
   
   - ```instance_relative_config=True``` diz à aplicação que os arquivos de configuração são relativos ao [diretório de instância](https://flask.palletsprojects.com/en/2.2.x/config/#instance-folders). O diretório de instância fica localizado fora do pacote ```flaskr``` e pode guardar dados que não devem ser commitados, como segredos de configuração e o arquivo de banco de dados.

2. ```app.config.from_mapping()``` define algumas configurações padrão que a aplicação irá usar:

   - ```SECRET_KEY``` é usada pelo Flask e suas extensões para manter dados seguros. Aqui setamos para ```'dev'``` para usar um valor conveniente durante o desenvolvimento, mas deve ser substituída por um valor aleatório ao subir para produção.
   - ```DATABASE``` é o caminho onde o arquivo de banco SQLite será salvo. Está localizado em ```app.instance_path```, que é o caminho que o Flask escolheu para seu diretório de instância. Veremos mais sobre banco de dados na próxima sessão.

3. ```app.config.from_pyfile()``` substitui as configurações padrão com os valores no arquivo ```config.py```, localizado no diretório de instância, se ele existir. Por exemplo, isso pode ser usado ao fazer deploy, para definir um valor real para ```SECRET_KEY```.

   - ```test_config``` também pode ser passado à _factory_ e será usado no lugar da configuração de instância. Assim, os testes que vamos escrever mais pra frente no tutorial, podem ser configurados independente dos valores escolhidos durante o desenvolvimento.

4. ```os.makedirs()``` garante que ```app.instance_path()``` existe. O Flask não cria o diretório de instância automaticamente, mas precisamos criar para que o arquivo do banco SQLite seja criado lá dentro.

5. ```@app.route()``` cria uma rota simples para que você possa ver a aplicação rodando antes de ver o resto do tutorial. Aqui criamos uma conexão entre a URL ```/hello``` e a função que retorna uma resposta, neste caso, a string ```'Hello,World!'```.

### Rodando a aplicação

Agora podemos rodar nossa aplicação com o comando ```flask```. Do terminal, diremos ao Flask onde achar nossa aplicação e rodá-la em modo de _debug_. Lembre-se, você ainda deve estar no diretório ```flask-tutorial```, não no pacote ```flaskr```.

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

Visite http://127.0.0.1:5000/hello num navegador que você verá a mensagem "Hello, World!". Parabéns, você está rodando sua aplicação Flask!

> Se outra aplicação já estiver utilizando a porta 5000, você verá um erro ```OSError: [Errno 98]``` ou ```OSError: [WinError 10013]``` quando o servidor tenta iniciar. Veja a documentação sobre [endereço em uso](https://flask.palletsprojects.com/en/2.2.x/server/#address-already-in-use) para ver como lidar com isso (ou apenas para a outra aplicação, se não for gerar problema).