from enum import Enum

EDGE_THRESHOLD = 0.25
WEIGHTS_THRESHOLD = 1e-4
DEFAULT_DEPTH = 2


class RelationshipGraph(Enum):
    ID_RELATIONSHIP = 1
    ID_FIRST_ENTITY = 2
    ID_SECOND_ENTITY = 3
    ID_RELATIONSHIP_TYPE = 4
    WEIGHT = 5

class WeightTypes(Enum):
    WDOWN_1 = 2
    WDOWN_2 = 3
    WUP_1 = 4
    WUP_2 = 5

class WeightsColumns(Enum):
    ID_RELATIONSHIP = 1
    WDOWN_1 = 2
    WDOWN_2 = 3
    WUP_1 = 4
    WUP_2 = 5

