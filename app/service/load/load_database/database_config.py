from enum import Enum
from os import path

from app.definitions import ROOT_DIR
from app.service.build_relationships.graph_config import RelationshipGraph
from app.service.translation.translation_config import EntityMap, RelationshipType

serialized_file = path.abspath(path.join(ROOT_DIR, "data/copenmed.pkl"))
excel_file = path.abspath(path.join(ROOT_DIR, "data/COpenMed_20210617.xlsx"))


class ROWS(Enum):
    ENTITY_TYPE = 1
    RELATION_TYPE = 2
    LANGUAGE = 3
    RELATIONS = 4
    ENTITIES = 5
    DETAILS = 6
    RESOURCES = 7
    DESCRIPTION = 8


COpenMed_map = {
    ROWS.ENTITY_TYPE: 'tipos_entidad',
    ROWS.RELATION_TYPE: 'tipos_relaciones',
    ROWS.LANGUAGE: 'idiomas',
    ROWS.RELATIONS: 'relaciones',
    ROWS.ENTITIES: 'entidades',
    ROWS.DETAILS: 'detalles',
    ROWS.RESOURCES: 'recursos',
    ROWS.DESCRIPTION: 'descripciones'
}

relationship_map = {
    'IdAsociacion': RelationshipGraph.ID_RELATIONSHIP,
    'IdEntidad1': RelationshipGraph.ID_FIRST_ENTITY,
    'IdEntidad2': RelationshipGraph.ID_SECOND_ENTITY,
    'IdTipoAsociacion': RelationshipGraph.ID_RELATIONSHIP_TYPE,
    'Nivel': RelationshipGraph.WEIGHT
}

entity_map = {
    'IdEntidad': EntityMap.ENTITY_ID,
    'Entidad': EntityMap.ENTITY_LABEL
}

relationship_type_map = {
    'IdTipoAsociacion': RelationshipType.RELATIONSHIP_ID,
    'TipoAsociacion': RelationshipType.RELATIONSHIP_LABEL

}