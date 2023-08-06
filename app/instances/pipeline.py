import yaml
from addict import Dict

from app.quality_judgment.laplacian import Laplacian
from app.quality_judgment.brightness import Brightness
from app.correction_module.correction_v1 import Correction_v1
from app.correction_module.correction_v2 import Correction_v2

class Pipeline(object):
    def __init__(self, config_path):
        with open(config_path, "r", encoding="UTF-8") as conf:
            config = yaml.load(conf, Loader=yaml.FullLoader)
        config = Dict(config)

        self.quality_judgment = []

        # image quality judgement
        if config.quality_judgment.laplacian.enable:
            self.quality_judgment.append(Laplacian(config.quality_judgment.laplacian))

        if config.quality_judgment.brightness.enable:
            self.quality_judgment.append(Brightness(config.quality_judgment.brightness))

        # correct_module
        if config.correction_module.correction_v1.enable:
            self.correction_module = Correction_v1(config.correction_module.correction_v1)

        if config.correction_module.correction_v2.enable:
            self.correction_module = Correction_v2()

        # id_recog
