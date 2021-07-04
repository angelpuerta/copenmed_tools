from enum import Enum
from os import path

from app.definitions import ROOT_DIR

EDGE_THRESHOLD = 0.25
WEIGHTS_THRESHOLD = 1e-4
DEFAULT_DEPTH = 2
PICKLED_PATH = path.abspath(path.join(ROOT_DIR, "data/reasoner.pkl"))



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

class EdgeType(Enum):
    INCOMING = 1
    OUTCOMING = 2