import io
import json
import argparse
from app.ac_identification import AnswerCardsIdentification


def parse_args():
    parser = argparse.ArgumentParser("SmartBanner")
    parser.add_argument("--config", default="../app/configs/answer_cards.yaml")
    parser.add_argument("--template_info", default="../data/template_info/template1.json", type=str)
    parser.add_argument("--imgs", default=["../data/test_imgs/ac1_bar_circle1_rotated.png",
                                           "../data/test_imgs/ac2.png",
                                           "../data/test_imgs/ac3.png",
                                           "../data/test_imgs/ac4.png"], type=list)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    config = args.config
    imgs = args.imgs
    template_info = args.template_info

    # 入参输入基础模板应为json，不需要解析
    with io.open(template_info, "r", encoding="UTF-8") as template_:
        template_info = json.load(template_)

    answer_crads_identification = AnswerCardsIdentification(config, template_info)

    # for img in imgs:
    #     result = answer_crads_identification.run(img)
    result = answer_crads_identification.run(imgs)
