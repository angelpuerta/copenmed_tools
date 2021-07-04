from app.service.build_relationships.build_reasons_pickled import ReasonPickledBuilder
from app.service.build_relationships.relations import Relations

relations_builder = ReasonPickledBuilder()
relations : Relations = relations_builder.build()
evaluations = relations.evaluate_node(503)
evaluations.make_explanation()
print(evaluations)
print(evaluations.to_json())
