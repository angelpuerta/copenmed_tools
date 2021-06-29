from app.service.build_relationships.edges import Edges
from app.service.load.load_database.COpenMedObject import COpenMedObject
from app.service.load.load_relationships.excel_relationship import ExcelRelationShipLoader

database = COpenMedObject()
relation_loader = ExcelRelationShipLoader()
relation = relation_loader.load_database()
graph = Edges(database.edge, relation)

successor = graph.evaluate_succesors(503)
successor.build_successors()
successor.to_json()