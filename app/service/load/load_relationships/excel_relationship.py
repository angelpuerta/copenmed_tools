
import pandas as pd

from app.service.load.load_relationships.load_relationship import LoadDatabase
from app.service.load.load_relationships.relationship_config import excel_file
from app.service.load.load_relationships.weights import Weights
from app.utils.singleton import singleton


@singleton
class ExcelRelationShipLoader(LoadDatabase):

    def load_database(self) -> Weights:
        database = pd.read_excel(excel_file,
                           sheet_name=None, engine="openpyxl")
        return Weights(database)


