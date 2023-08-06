import os.path as osp
import time
from pathlib import Path

from paddlelabel_ml.model import BaseModel
from paddlelabel_ml.util import abort


class SampleModel(BaseModel):
    def __init__(self, model_path: str = None, param_path: str = None):
        """
        init model

        Args:
            model_path (str, optioanl):
            param_path (str, optional):
        """
        super().__init__(curr_path=Path(__file__).parent.absolute())

    def predict(self, req):
        time.sleep(5)
        return [
            {
                "label_name": "Sample Detection Result",
                "score": 0.9,
                "result": "wmin,hmin,wmax,hmax",
            }
        ]


print("Sample called")
