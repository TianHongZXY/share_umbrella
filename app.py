from flask import Flask, request, render_template, jsonify
from . import create_app, db
from flask_migrate import Migrate
from .models import User

app = create_app('default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


