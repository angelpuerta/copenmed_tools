from app.service.load.load_database.COpenMedObject import COpenMedObject
from app.service.translation.translation_config import RelationshipType, EntityMap, relationship_supertype_translation
from app.utils.singleton import singleton


@singleton
class TranslationService:
    _database: COpenMedObject

    def __init__(self):
        self._database = COpenMedObject()

    def translate_relationship_type(self, relationship_id) -> str:
        index = self._database.edge_type[RelationshipType.RELATIONSHIP_ID] == relationship_id
        return self._database.edge_type[index][RelationshipType.RELATIONSHIP_LABEL].values[0]

    def translate_entity(self, entity_id) -> str:
        index = self._database.entity[EntityMap.ENTITY_ID] == entity_id
        return self._database.entity[index][EntityMap.ENTITY_LABEL].values[0]

    def translate_relationship_supertype(self, relationship_type)-> str:
        return relationship_supertype_translation[relationship_type]

