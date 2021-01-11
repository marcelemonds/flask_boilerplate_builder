import os
import sys
import os.path as op
from codeblocks import CodeBlock, CodeBlockNested


class AppManager():
    def __init__(self, name='test_app', database=False, models=[], blueprints=False, blueprint_names=[], paths=None):
        self.name = name
        self.database = database
        self.models = models
        self.blueprints = blueprints
        self.blueprint_names = blueprint_names
        self.paths = paths


    def __repr__(self):
        return f'name: {self.name}, database: {self.database}, models: {self.models}, blueprints: {self.blueprints}, blueprint_names: {self.blueprint_names}'


    def create_files(self, files):
        for path, code in files.items():
            with open(path, 'w') as f:
                f.write(str(code))
                f.close()


    def create_dirs(self):
        # create app directories
        basedir = op.abspath(op.dirname(__file__))
        try:
            paths = dict()
            paths['app_dir'] = op.join(basedir, self.name)
            paths['app_sub_dir'] = op.join(paths['app_dir'], 'app')
            paths['templates_dir'] = op.join(paths['app_sub_dir'], 'templates')
            paths['templates_layouts_dir'] = op.join(paths['templates_dir'], 'layouts')
            paths['static_dir'] = op.join(paths['app_sub_dir'], 'static')
            paths['static_css_dir'] = op.join(paths['static_dir'], 'css')
            paths['static_js_dir'] = op.join(paths['static_dir'], 'js')
            if self.blueprints:
                for blueprint in self.blueprint_names:
                    paths[f'{blueprint}_folder'] = op.join(paths['app_sub_dir'], blueprint)
                    paths[f'{blueprint}_templates'] = op.join(paths['templates_dir'], blueprint)
        except Exception as e:
            print('ERROR: Folder paths could not be created.')
            print(str(e))
            return sys.exit()
        if not op.exists(paths['app_dir']):
            try:
                for key, value in paths.items():
                    os.mkdir(value)
            except OSError as e:
                print('ERROR: Folders could not be created.')
                print(str(e))
                if 'app_dir' in paths and op.exists(paths['app_dir']):
                    shutil.rmtree(paths['app_dir'])
                return sys.exit()
        else:
            print('ERROR: App folder already exists. Please select another app name or remove the folder.')
            return sys.exit()
        self.paths = paths


    def create_blueprints(self):
        files = dict()
        for name in self.blueprint_names:
            # create __init__.py
            path = op.join(self.paths[f'{name}_folder'], '__init__.py')
            code_block = CodeBlock([
                'from flask import Blueprint',
                '',
                f"bp = Blueprint('{name}', __name__)",
                '',
                f"from app.{name} import routes"
            ])
            files[path] = code_block
            # create routes.py
            path = op.join(self.paths[f'{name}_folder'], 'routes.py')
            if self.database:
                code_snippets = [
                    'from app import db',
                    f"from app.{name} import bp"
                    ]
            else:
                code_snippets = [
                    f"from app.{name} import bp"
                    ]
            route = CodeBlockNested(
                'python',
                'def index()',
                [
                    f"return render_template('{name}/{name}.html', title='Index')"
                ]
            )
            code_snippets.extend([
                'from flask import render_template, flash, redirect, url_for, request, jsonify',
                'from app.models import *',
                '',
                '',
                "@bp.route('/', methods=['GET', 'POST'])",
                route
                ])
            code_block = CodeBlock(code_snippets)
            files[path] = code_block
            # create html
            path = op.join(self.paths[f'{name}_templates'], f'{name}.html')
            code_block = CodeBlock([
                '{% extends "layouts/main.html" %}',
                '',
                '{% block meta %}{% endblock %}',
                '',
                '{% block css %}{% endblock %}',
                '',
                '{% block scripts_head %}{% endblock %}',
                '',
                '{% block content %}{% endblock %}',
                '',
                '{% block scripts %}{% endblock %}'
                ])
            files[path] = code_block
        self.create_files(files)


    def create_statics(self):
        files = dict()
        # create .gitignore
        path = op.join(self.paths['app_dir'], '.gitignore')
        code_block = CodeBlock([
            '.env',
            '__pycache__/',
            'env/',
            'migrations/'
            ])
        files[path] = code_block
        # create .env
        path = op.join(self.paths['app_dir'], '.env')
        if self.database:
            code_block = CodeBlock([
                '# Flask Variables',
                'FLASK_APP=main.py',
                'FLASK_DEBUG=1',
                '',
                '# App Variabels',
                'SECRET_KEY=<enter secret key>',
                '# Database',
                'DATABASE_URL=<sql_dialect>://<db_username>:<db_password>@localhost/<db_schema>'
                ])
        else:
            code_block = CodeBlock([
                '# Flask Variables',
                'FLASK_APP=main.py',
                'FLASK_DEBUG=1',
                '',
                '# App Variabels',
                'SECRET_KEY=<enter secret key>'
                ])
        files[path] = code_block
        # create main.html
        path = op.join(self.paths['templates_layouts_dir'], 'main.html')
        head = CodeBlockNested(
            'html',
            '<head>',
            [
                '<meta charset="UTF-8">',
                '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                '{% block meta %}{% endblock %}',
                '{% if title %}',
                '<title>{{ title }}</title>',
                '{% else %}',
                '<title>Welcome</title>',
                '{% endif %}',
                '{% block css %}{% endblock %}',
                '{% block scripts_head %}{% endblock %}'
            ],
            '</head>'
        )
        body = CodeBlockNested(
            'html',
            '<body>',
            [
                '{% block content %}{% endblock %}',
                '{% block scripts %}{% endblock %}'
            ],
            '</body>'
        )
        code_block = CodeBlock([
            '<!DOCTYPE html>',
            '<html lang="en">',
            head,
            body,
            '</html>'
        ])
        files[path] = code_block

        # create styles.css
        path = op.join(self.paths['static_css_dir'], 'styles.css')
        code_block = CodeBlock([''])
        files[path] = code_block

        # create javascript.js
        path = op.join(self.paths['static_js_dir'], 'javascipt.js')
        code_block = CodeBlock([''])
        files[path] = code_block
        self.create_files(files)


    def create_routes(self):
        files = dict()
        # create routes.py
        path = op.join(self.paths['app_sub_dir'], 'routes.py')
        if self.database:
            code_snippet = 'from app import app, db'
        else:
            code_snippet = 'from app import app'
        route = CodeBlockNested(
            'python',
            'def index()',
            [
                "return render_template('index.html', title='Index')"
            ]
        )
        code_block = CodeBlock([
            code_snippet,
            'from flask import render_template, flash, redirect, url_for, request, jsonify',
            'from app.models import *',
            '',
            '',
            "@app.route('/', methods=['GET', 'POST'])",
            route
            ])
        files[path] = code_block
        # create html
        path = op.join(self.paths['templates_dir'], 'index.html')
        code_block = CodeBlock([
            '{% extends "layouts/main.html" %}',
            '',
            '{% block meta %}{% endblock %}',
            '',
            '{% block css %}{% endblock %}',
            '',
            '{% block scripts_head %}{% endblock %}',
            '',
            '{% block content %}{% endblock %}',
            '',
            '{% block scripts %}{% endblock %}'
            ])
        files[path] = code_block
        self.create_files(files)


    def create_main(self):
        files = dict()
        path = op.join(self.paths['app_dir'], 'main.py')
        if self.database and self.blueprints:
            shell_context = CodeBlockNested(
                'python',
                'def make_shell_context()',
                [
                    "return {f'{model}': obj for model, obj in inspect.getmembers(models) if inspect.isclass(obj)}"
                ])
            code_block = CodeBlock([
                'from app import create_app, db',
                'import app.models as models',
                '',
                'app = create_app()',
                '',
                '',
                '@app.shell_context_processor',
                shell_context
                ])
        elif self.database and not self.blueprints:
            shell_context = CodeBlockNested(
                'python',
                'def make_shell_context()',
                [
                    "return {f'{model}': obj for model, obj in inspect.getmembers(models) if inspect.isclass(obj)}"
                ])
            code_block = CodeBlock([
                'from app import app, db',
                'import app.models as models',
                '',
                '',
                '@app.shell_context_processor',
                shell_context
                ])
        else:
            code_block = CodeBlock(['from app import app'])
        files[path] = code_block
        self.create_files(files)


    def create_config(self):
        files = dict()
        path = op.join(self.paths['app_dir'], 'config.py')
        if self.database:
            config_class = CodeBlockNested(
                'python',
                'class Config(object)',
                [
                    "SECRET_KEY = config('SECRET_KEY', default='you-will-never-guess')",
                    "SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')",
                    "SQLALCHEMY_TRACK_MODIFICATIONS = False"
                ])
            code_block = CodeBlock([
                'from decouple import config',
                '',
                '',
                config_class
                ])
        else:
            config_class = CodeBlockNested(
                'python',
                'class Config(object)',
                [
                    "SECRET_KEY = config('SECRET_KEY', default='you-will-never-guess')"
                ])
            code_block = CodeBlock([
                'from decouple import config',
                '',
                '',
                config_class
                ])
        files[path] = code_block
        self.create_files(files)


    def create_init(self):
        files = dict()
        path = op.join(self.paths['app_sub_dir'], '__init__.py')
        if self.database and self.blueprints:
            create_app_inner = [
                    'app = Flask(__name__)',
                    'app.config.from_object(config_class)',
                    '',
                    'db.init_app(app)',
                    'migrate.init_app(app, db)',
                    ''
                ]
            for name in self.blueprint_names:
                create_app_inner.extend([
                    f'from app.{name} import bp as {name}_bp',
                    f'app.register_blueprint({name}_bp)',
                    ''
                    ])
            create_app_inner.append('return app')
            create_app = CodeBlockNested(
                'python',
                'def create_app(config_class=Config)',
                create_app_inner
                )
            code_block = CodeBlock([
                'from flask import Flask',
                'from config import Config',
                'from flask_sqlalchemy import SQLAlchemy',
                'from flask_migrate import Migrate',
                '',
                '',
                'db = SQLAlchemy()',
                'migrate = Migrate()',
                '',
                create_app,
                '',
                'from app import models'
                ])
        elif self.database and not self.blueprints:
            code_block = CodeBlock([
                'from flask import Flask',
                'from config import Config',
                'from flask_sqlalchemy import SQLAlchemy',
                'from flask_migrate import Migrate',
                '',
                '',
                'app = Flask(__name__)',
                'app.config.from_object(Config)',
                '',
                'db = SQLAlchemy(app)',
                'migrate = Migrate(app, db)',
                '',
                'from app import routes, models'
                ])
        elif not self.database and self.blueprints:
            create_app_inner = [
                    'app = Flask(__name__)',
                    'app.config.from_object(config_class)',
                    ''
                ]
            for name in self.blueprint_names:
                create_app_inner.extend([
                    f'from app.{name} import bp as {name}_bp',
                    f'app.register_blueprint({name}_bp)',
                    ''
                    ])
            create_app_inner.append('return app')
            create_app = CodeBlockNested(
                'python',
                'def create_app(config_class=Config)',
                create_app_inner
                )
            code_block = CodeBlock([
                'from flask import Flask',
                'from config import Config',
                '',
                '',
                create_app,
                '',
                'from app import models'
                ])
        elif not self.database and not self.blueprints:
            code_block = CodeBlock([
                'from flask import Flask',
                'from config import Config',
                '',
                '',
                'app = Flask(__name__)',
                'app.config.from_object(Config)',
                '',
                'from app import routes'
                ])
        files[path] = code_block
        self.create_files(files)


    def create_models(self):
        files = dict()
        path = op.join(self.paths['app_sub_dir'], 'models.py')
        models_code =[
            'from app import db'
            ]
        if self.models:
            def_insert = CodeBlockNested(
                'python',
                'def insert(self)',
                [
                    'db.session.add(self)',
                    'db.session.commit()'
                ]
            )
            def_update = CodeBlockNested(
                'python',
                'def update(self)',
                [
                    'db.session.commit()'
                ]
            )
            def_delete = CodeBlockNested(
                'python',
                'def delete(self)',
                [
                    'db.session.delete(self)',
                    'db.session.commit()'
                ]
            )
            for model in self.models:
                db_table = CodeBlockNested(
                    'python',
                    f'\n\nclass {model}(db.Model)',
                    [
                        'id = db.Column(db.Integer, primary_key=True)',
                        '',
                        def_insert,
                        '',
                        def_update,
                        '',
                        def_delete
                    ]
                )
                models_code.append(db_table)
        code_block = CodeBlock(models_code)
        files[path] = code_block
        self.create_files(files)


    def create_app(self):
        self.create_dirs()
        self.create_statics()
        self.create_main()
        self.create_config()
        self.create_init()
        if self.blueprints:
            self.create_blueprints()
        else:
            self.create_routes()
        if self.database:
            self.create_models()