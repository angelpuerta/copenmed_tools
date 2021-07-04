from dataclasses import dataclass

from pandas import DataFrame

from app.service.build_relationships.graph_config import WeightsColumns, EdgeType
from app.service.load.load_weights.weights_config import RelationShips, relationships_excel_map, \
    relationships_weights_map
from app.utils.utils import list_difference


def transform_weights(database: DataFrame, relation_ship: RelationShips) -> DataFrame:
    return database[relationships_excel_map[relation_ship]] \
        .fillna(0) \
        .rename(columns=relationships_weights_map, inplace=False)


def _get_weight_column(edge_type: EdgeType, element_not_present: bool):
    if element_not_present:
        return WeightsColumns.WDOWN_2 if edge_type.INCOMING else WeightsColumns.WDOWN_2
    return WeightsColumns.WDOWN_1 if edge_type.INCOMING else WeightsColumns.WUP_1


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

    def get_weight(self, weight_type, type, edge_type: EdgeType) -> float:
        selected_index = (self._data[weight_type][WeightsColumns.ID_RELATIONSHIP] == type)
        select_element = self._data[weight_type][selected_index]
        select_row = _get_weight_column(edge_type, select_element.empty)
        if not select_element[select_row].empty:
            return select_element[select_row].values[0]
        return 0
