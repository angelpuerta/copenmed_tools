from enum import Enum
from os import path

from app.definitions import ROOT_DIR
from app.service.build_relationships.graph_config import WeightsColumns

serialized_file = path.abspath(path.join(ROOT_DIR,"data/copenmed.pkl"))
excel_file = path.abspath(path.join(ROOT_DIR,"data/reasonerCOSS_0003_clasifRelaciones.xlsx"))

class RelationShips(Enum):
    CAUSES = 1
    OBSERVATION = 2
    CONSEQUENCES = 3
    TREATMENTS = 4
    TEST = 5
    PREVENTION = 6
    SIMILAR = 7
    ATTENTION = 8

relationships_excel_map = {
    RelationShips.CAUSES : 'CAUSAS',
    RelationShips.OBSERVATION: 'OBSERVABLES',
    RelationShips.CONSEQUENCES : 'CONSECUENCIAS',
    RelationShips.TREATMENTS : 'TRATAMIENTOS',
    RelationShips.TEST : 'TESTS' ,
    RelationShips.PREVENTION : 'PREVENCION',
    RelationShips.SIMILAR :  'SIMILAR',
    RelationShips.ATTENTION : 'ATENCION'
}

relationships_weights_map = {
    'IdTipoAsociacion': WeightsColumns.ID_RELATIONSHIP,
    'A1+, Down': WeightsColumns.WDOWN_1,
    'A1-, Down': WeightsColumns.WDOWN_2,
    'A2+, Up': WeightsColumns.WUP_1,
    'A2-, Up': WeightsColumns.WUP_2,
}
