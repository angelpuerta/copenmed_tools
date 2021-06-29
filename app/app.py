from flask import Flask
from flask_cors import CORS, cross_origin

from app.service.build_relationships.edges import Edges
from app.service.load.load_database.COpenMedObject import COpenMedObject
from app.service.load.load_relationships.excel_relationship import ExcelRelationShipLoader

database = COpenMedObject()
relation_loader = ExcelRelationShipLoader()
relation = relation_loader.load_database()
graph = Edges(database.edge, relation)

app = Flask(__name__)
cors = CORS(app)



@app.route('/ping', methods=['GET'])
def index():
    return 'Server ok'


@app.route('/relationships/<node>', methods=['GET'])
def info_node(node):
    successor = graph.evaluate_succesors(int(node))
    successor.build_successors()
    return successor.to_json()
