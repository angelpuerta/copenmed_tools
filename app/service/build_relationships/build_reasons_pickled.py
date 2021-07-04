import pickle
from os import path

from app.service.build_relationships.graph_config import PICKLED_PATH
from app.service.build_relationships.relations import Relations
from app.service.load.load_database.excel_database import ExcelDatabaseLoader
from app.service.load.load_weights.excel_weights import WeightsLoader
from app.utils.singleton import singleton


@singleton
class ReasonPickledBuilder:
    _relations: Relations

    def build(self) -> Relations:
        if not path.isfile(PICKLED_PATH):
            database_loader = ExcelDatabaseLoader()
            database = database_loader.load_database()
            weights_loader = WeightsLoader()
            weights = weights_loader.load_database()
            self._relations = Relations(database.edge, weights)
            with open(PICKLED_PATH, "xb") as file:
                pickle.dump(self._relations, file)
        if not hasattr(self, '_relations'):
            with open(PICKLED_PATH, "rb") as file:
                self._relations = pickle.load(file)
        return self._relations
