from app.service.build_relationships.relations import Relations
from app.service.load.load_database.excel_database import ExcelDatabaseLoader
from app.service.load.load_weights.excel_weights import WeightsLoader
from app.utils.singleton import singleton

@singleton
class ReasonBuilderImpl:
    _relations: Relations

    def build(self) -> Relations:
        database_loader = ExcelDatabaseLoader()
        database = database_loader.load_database()
        weights_loader = WeightsLoader()
        weights = weights_loader.load_database()
        return Relations(database.edge, weights)
