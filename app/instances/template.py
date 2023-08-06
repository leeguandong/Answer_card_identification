import os
import random
from PIL import Image, ImageDraw, ImageFont


class TemplateInfo(object):
    def __init__(self, template):
        self.template = template
        assert self.template is not None, "input template info none!"

        current_dir = os.path.dirname(__file__)
        font_path = os.path.join(current_dir, "custom.ttf")
        random.seed(0)
        self.font = ImageFont.truetype(font_path, 25, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小

    @property
    def pages(self):
        pages = []
        titles = self.template['titles']
        for title in titles:
            for item in title['items']:
                if item['page'] not in pages:
                    pages.append(item['page'])
        return max(pages)

    @property
    def anchor_points(self):
        return self.template["anchor_points"]

    @property
    def corner(self):
        return self.anchor_points["horizontal_points"][0]["points"][0], \
            self.anchor_points["horizontal_points"][0]["points"][1]

    def visual(self, draw_img_dict):
        # 2.在第一张图上先写学号
        id_card = self.template.get("id_card", None)
        if id_card is not None:
            bbox_tl = id_card["bbox"][0], id_card["bbox"][1]
            bbox_br = id_card["bbox"][0] + id_card["bbox"][2], id_card["bbox"][1] + id_card["bbox"][3]
            draw_img_dict["0"][1].rectangle([bbox_tl, bbox_br], outline=(255, 0, 0))

        # 3.在每页上把循环的item描绘出来，item只需要描绘一次
        for idx_title, title in enumerate(self.template['titles']):
            color = (random.randint(0, 255), random.randint(0, 255),
                     random.randint(0, 255))
            for idx_item, item in enumerate(title['items']):
                page_item = item.get("page", None)
                bbox_item = item.get("bbox", None)
                id_item = item.get("id", None)
                answer_item = item.get("answer", None)
                bbox_item_t_tl = bbox_item[0], bbox_item[1]
                bbox_item_t_br = bbox_item[0] + bbox_item[2], bbox_item[1] + bbox_item[3]
                draw_img_dict[f"{page_item}"][1].rectangle([bbox_item_t_tl, bbox_item_t_br], outline=color)
                if answer_item is not None:
                    coord = (max(bbox_item_t_tl[0] - 30, 0), max(bbox_item_t_tl[1] - 10, 0))
                    draw_img_dict[f"{page_item}"][1].text(coord, answer_item, (0, 0, 255), font=self.font)

    def visual_info(self):
        """
        只输入模板，看一下模板是否有问题
        :return:
        """
        # 0.新建通用画布
        self.canvas_w = self.template["bbox"][2] + self.template["bbox"][0]
        self.canvas_h = self.template["bbox"][3] + self.template["bbox"][1]
        draw_img = Image.new("RGB", (self.canvas_w, self.canvas_h), (255, 255, 255))

        # 1.新建页面
        draw_img_dict = {}
        for page in range(self.pages + 1):
            draw_img_ = draw_img.copy()
            draw = ImageDraw.Draw(draw_img_)
            draw_img_dict.update({f"{page}": [draw_img_, draw]})

        # 2/3
        self.visual(draw_img_dict)

        # 4.保存图片
        for page in range(self.pages + 1):
            draw_img_dict[f"{page}"][0].save(f"template_info_page_{page}.jpg")

    def visual_result(self, imgs):
        # 输入一个图片集合和一个templateinfo将两者匹配起来
        assert isinstance(imgs, list), "imgs must be list"
        draw_img_dict = {}
        for page in range(self.pages + 1):
            if isinstance(imgs[page], str):
                draw_img_ = Image.open(imgs[page])
            else:
                draw_img_ = imgs[page].copy()
            draw = ImageDraw.Draw(draw_img_)
            draw_img_dict.update({f"{page}": [draw_img_, draw]})

        self.visual(draw_img_dict)

        # 4.保存图片
        for page in range(self.pages + 1):
            draw_img_dict[f"{page}"][0].save(f"template_imgs_page_{page}.jpg")
