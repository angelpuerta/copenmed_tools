
import pandas as pd

from app.service.load.load_weights.load_weights import LoadDatabase
from app.service.load.load_weights.weights import Weights
from app.service.load.load_weights.weights_config import excel_file
from app.utils.singleton import singleton


@singleton
class WeightsLoader(LoadDatabase):

    def load_database(self) -> Weights:
        database = pd.read_excel(excel_file,
                           sheet_name=None, engine="openpyxl")
        return Weights(database)


