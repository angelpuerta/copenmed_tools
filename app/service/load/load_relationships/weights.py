from dataclasses import dataclass

from pandas import DataFrame

from app.service.build_relationships.graph_config import WeightsColumns
from app.service.load.load_relationships.relationship_config import RelationShips, relationships_excel_map, \
    relationships_weights_map
from app.utils.utils import list_difference


def transform_weights(database: DataFrame, relation_ship: RelationShips) -> DataFrame:
    return database[relationships_excel_map[relation_ship]] \
        .fillna(0) \
        .rename(columns=relationships_weights_map, inplace=False)


@dataclass()
class Weights:
    _data: dict

    def __init__(self, database: DataFrame):
        if not all([row in database.keys() for row in relationships_excel_map.values()]):
            raise IOError("Row does not contain {}".format(
                list_difference(database.keys, relationships_excel_map.values())))
        self._data = {
            RelationShips.CAUSES: transform_weights(database, RelationShips.CAUSES),
            RelationShips.OBSERVATION: transform_weights(database, RelationShips.OBSERVATION),
            RelationShips.CONSEQUENCES: transform_weights(database, RelationShips.CONSEQUENCES),
            RelationShips.TREATMENTS: transform_weights(database, RelationShips.TREATMENTS),
            RelationShips.TEST: transform_weights(database, RelationShips.TEST),
            RelationShips.PREVENTION: transform_weights(database, RelationShips.PREVENTION),
            RelationShips.SIMILAR: transform_weights(database, RelationShips.SIMILAR),
            RelationShips.ATTENTION: transform_weights(database, RelationShips.ATTENTION)
        }

    def get_weight_types(self):
        return self._data.keys()

    def get_weight(self, weight_type, id_association, weight_column) -> float:
        selected_index = self._data[weight_type][WeightsColumns.ID_RELATIONSHIP] == id_association
        select_element = self._data[weight_type][selected_index]
        if len(select_element) == 0:
            return 0
        return select_element[weight_column].values[0]
