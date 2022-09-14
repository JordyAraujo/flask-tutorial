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

Isso vai criar o arquivo ```requirements.txt```, contendo as bibliotecas instaladas no seu ambiente virtual até então, com suas respectivas versões. Se você instalou apenas o Flask, note que outras bibliotecas foram adicionadas, pois são auxiliares ao Flask. Você pode deixar apenas o Flask na lista, mas as outras serão instaladas com ele da mesma forma.

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