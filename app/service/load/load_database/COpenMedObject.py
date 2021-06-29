from dataclasses import dataclass

from pandas import DataFrame

from app.service.load.load_database.database_config import COpenMed_map, ROWS, relationship_map, relationship_type_map, \
    entity_map
from app.service.load.load_database.excel_database import ExcelDatabaseLoader
from app.utils.utils import list_difference, build_dataframe


@dataclass()
class COpenMedObject:
    details: DataFrame
    edge: DataFrame
    edge_type: DataFrame
    entity: DataFrame
    resource: DataFrame

    def __init__(self):
        database_loader = ExcelDatabaseLoader()
        database = database_loader.load_database()
        if not all([row in database.keys() for row in COpenMed_map.values()]):
            raise IOError("Row does not contain {}".format(list_difference(database.keys, COpenMed_map.values())))
        self.details = database[COpenMed_map[ROWS.DETAILS]]
        self.edge = build_dataframe(database[COpenMed_map[ROWS.RELATIONS]],
                                    relationship_map)
        self.edge_type = build_dataframe(database[COpenMed_map[ROWS.RELATION_TYPE]],
                                         relationship_type_map)
        self.entity = build_dataframe(database[COpenMed_map[ROWS.ENTITIES]],
                                      entity_map)
        self.resource = database[COpenMed_map[ROWS.ENTITY_TYPE]]
