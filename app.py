from flask import (
    Flask,
    jsonify, 
    redirect, 
    render_template, 
    request, 
    url_for,
    abort
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost:5432/lab20'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#{% if cred.completed %} red {% endif %}

class Registro(db.Model):
    __tablename__ = 'registro'
    nombres = db.Column(db.String(), nullable=False , primary_key=True)
    apellidos = db.Column(db.String(), nullable=True)
    sexo = db.Column(db.String(), nullable=True, default=False)
    ano_nacimiento = db.Column(db.DateTime(), nullable=True, default=False)
    pais = db.Column(db.String(), nullable=True, default=False) 
    usuario = db.Column(db.String(), nullable=True, default=False)
    password = db.Column(db.Integer, nullable=False, default=False)


db.create_all()


@app.route('/')
def index():
    return render_template ('index.html', registros=Registro.query.all())


@app.route('/registro/create', methods=['POST'])
def create_user():
    error = False
    response = {}
    try:
        password = request.get_json()['password']
        resistro = Registro(password=password)
        db.session.add(resistro)
        db.session.commit()
        response['password'] = password
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify(response)


#run
if __name__ == '__main__':
    app.run(debug=True, port=5002)
