import pandas as pd

from app.service.load.load_database.database_config import excel_file
from app.service.load.load_database.load_database import LoadDatabase
from app.utils.singleton import singleton


@singleton
class ExcelDatabaseLoader(LoadDatabase):

    def load_database(self):
        database = pd.read_excel(excel_file,
                           sheet_name=None, engine="openpyxl")
        return database