from flask import Flask
from flask_cors import CORS

from app.service.build_relationships.build_reasons_impl import ReasonBuilderImpl
from app.service.build_relationships.relations import Relations

relations_builder = ReasonBuilderImpl()
relations : Relations = relations_builder.build()

app = Flask(__name__)
cors = CORS(app)
print("App ready")

@app.route('/ping', methods=['GET'])
def index():
    return 'Server ok'


@app.route('/relationships/<node>', methods=['GET'])
def info_node(node):
    reasons = relations.evaluate_node(int(node))
    reasons.make_explanation()
    return reasons.to_json()
