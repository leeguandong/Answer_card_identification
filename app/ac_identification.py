import cv2
from app.instances.template import TemplateInfo
from app.instances.pipeline import Pipeline


class AnswerCardsIdentification(object):
    def __init__(self, config, template_info):
        # 数据结构初始化
        self.template = TemplateInfo(template_info)

        # pipeline初始化
        self.pipeline = Pipeline(config)

    def run_preprocess(self, img_dict):
        # quality_judgment
        for transform in self.pipeline.quality_judgment:
            img_dict = transform(img_dict)

        # correction_module
        img_dict = self.pipeline.correction_module.run(img_dict, self.template)

        # 组合逻辑
        self.preprocess_juge(img_dict)

    def preprocess_juge(self, img_dict):
        laplacian = img_dict.get("laplacian", False)
        brightness = img_dict.get("brightness", False)

        correct_socre = img_dict.get("score", 0)

        pass

    def run_process(self, imgs):
        pass

    def run(self, imgs):
        imgs_pro = []
        for img in imgs:
            img_dict = {"img": cv2.imread(img), "img_path": img}
            img_pre_dict = self.run_preprocess(img_dict)
            imgs_pro.append(img_pre_dict)

        # if imgpre:
