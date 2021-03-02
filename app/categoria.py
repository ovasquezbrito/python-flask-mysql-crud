from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:12345678@localhost:3306/bdpythonapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __init__(self, name,description):
        self.name = name
        self.description = description
db.create_all()

class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')

# Una sola respuesta
categoria_schema = CategoriaSchema()
# Listado de Categoráis
categorias_schema = CategoriaSchema(many=True)

# Listado de categorias
@app.route('/categorias', methods=['GET'])
def obtenerCategorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

# Mostrar una categoría
@app.route('/categorias/<id>', methods=['GET'])
def obtenerCategoria(id):
    one_categorias = Categoria.query.get(id)
    return categoria_schema.jsonify(one_categorias)

# GUardar una categoría en la data
@app.route('/categorias', methods=['POST'])
def addCategoria():
    data = request.get_json(force=True)
    name = data['name']
    description = data['description']

    nuevaCategoria = Categoria(name, description)

    db.session.add(nuevaCategoria)
    db.session.commit()

    return categoria_schema.jsonify(nuevaCategoria)

# Actualizar una categoría en la data
@app.route('/categorias/<id>', methods=['PUT'])
def updateCategoria(id):
    
    idCategoria = Categoria.query.get(id)

    data = request.get_json(force=True)
    name = data['name']
    description = data['description']

    idCategoria.name = name
    idCategoria.description = description

    db.session.commit()

    return categoria_schema.jsonify(idCategoria)

# Eliminar una categoría
@app.route('/categorias/<id>', methods=['DELETE'])
def eliminarCategoria(id):
    eliminarCategoria = Categoria.query.get(id)
    db.session.delete(eliminarCategoria)
    db.session.commit()
    return categoria_schema.jsonify(eliminarCategoria)

# Mensaje de Bienvenida
@app.route('/', methods=['GET'])
def index():
    return jsonify({'Mensaje': 'Bienvenido a tu Apy rest en python'})

if __name__=="__main__":
    app.run(debug=True)