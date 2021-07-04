from enum import Enum

from app.service.load.load_weights.weights_config import RelationShips


class EntityMap(Enum):
    ENTITY_ID = 0
    ENTITY_LABEL = 1
    ENTITY_TYPE = 2


class RelationshipType(Enum):
    RELATIONSHIP_ID = 0
    RELATIONSHIP_LABEL = 1


relationship_supertype_translation = {
    RelationShips.CAUSES: 'CAUSE',
    RelationShips.OBSERVATION: 'OBSERVABLES',
    RelationShips.CONSEQUENCES: 'CONSEQUENCES',
    RelationShips.TREATMENTS: 'TREATMENTS',
    RelationShips.TEST: 'TESTS',
    RelationShips.PREVENTION: 'PREVENTION',
    RelationShips.SIMILAR: 'SIMILARITIES',
    RelationShips.ATTENTION: 'ATTENTION'
}
