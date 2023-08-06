import json
from app.instances.template import TemplateInfo

templateinfo = json.load(open("../data/template_info/template1.json", "r", encoding="utf-8"))
imgs = ["../data/test_imgs/ac1.png",
        "../data/test_imgs/ac2.png",
        "../data/test_imgs/ac3.png",
        "../data/test_imgs/ac4.png"]

template = TemplateInfo(templateinfo)

template.visual_info()  # 可视化输入框
template.visual_result(imgs)  # 在输入图上可视化框

pass
