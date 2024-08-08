import os
import time

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ExifTags

from imageTools.baseClass.ExifFormat import ExifFormat


def create_image_with_blurred_background(image_path,
                                         border_size_ratio,
                                         text_area_ratio,
                                         text,
                                         font_path,
                                         output_path,
                                         blur_radius=20,
                                         text_alignment='center',
                                         font_color='black',
                                         shadow_offset=(20, 20),
                                         shadow_color=(0, 0, 0, 128),
                                         corner_radius_ratio=0.05,
                                         font_size=None,
                                         image_text_margin=30,
                                         line_spacing=5):
    """
    在原始图片周围添加边框，并在底部添加文字说明。底图为主图的模糊版本，并在边框添加阴影效果。

    参数：
    image_path (str): 原始图片的路径。
    border_size_ratio (float): 边框占原始图片宽度和高度的比例。
    text_area_ratio (float): 底部文字展示区域高度占原始图片高度的比例。
    text (str): 底部展示的文字内容。
    font_path (str): 文字字体文件的路径。
    output_path (str): 保存新图片的路径。
    blur_radius (int): 模糊半径，默认为20。
    text_alignment (str): 文字对齐方式，可选值为'left', 'center', 'right'。默认为居中对齐。
    font_color (str): 文字颜色，默认为黑色。
    shadow_offset (tuple): 阴影的偏移量，默认为(10, 10)。
    shadow_color (tuple): 阴影的颜色和透明度，默认为(0, 0, 0, 128)。
    corner_radius_ratio (float): 圆角的半径占原始图片最小边长的比例，默认为0.05。
    font_size (int, optional): 自定义字体大小，如果为None，则自动调整。
    image_text_margin (int): 图片和第一行文本之间的间距。
    line_spacing (int): 每行文本之间的间距。
    """
    # 打开原始图片
    original_image = Image.open(image_path)

    # 获取原始图片的尺寸
    original_width, original_height = original_image.size

    # 计算新的尺寸
    border_width = int(original_width * border_size_ratio)  # 左右各扩展宽度的比例
    border_height = int(original_height * border_size_ratio)  # 上下各扩展高度的比例
    text_area_height = int(original_height * text_area_ratio)  # 下方文字展示区域高度的比例

    new_width = original_width + 2 * border_width
    new_height = original_height + 2 * border_height + text_area_height

    # 创建模糊背景图片
    blurred_background = original_image.filter(ImageFilter.GaussianBlur(blur_radius)).resize((new_width, new_height))

    # 创建阴影图片
    shadow_image = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_image)
    shadow_rect = [
        border_width + shadow_offset[0],
        border_height + shadow_offset[1],
        border_width + original_width + shadow_offset[0],
        border_height + original_height + shadow_offset[1]
    ]
    shadow_draw.rectangle(shadow_rect, fill=shadow_color)
    shadow_image = shadow_image.filter(ImageFilter.GaussianBlur(blur_radius))

    # 将阴影图片粘贴到模糊背景图片上
    blurred_background.paste(shadow_image, (0, 0), shadow_image)

    # 创建圆角蒙版
    corner_radius = int(min(original_width, original_height) * corner_radius_ratio)
    mask = Image.new('L', (original_width, original_height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (original_width, original_height)], radius=corner_radius, fill=255)

    # 将圆角蒙版应用到原始图片
    rounded_image = Image.new('RGBA', (original_width, original_height))
    rounded_image.paste(original_image, (0, 0), mask=mask)

    # 将处理后的原始图片粘贴到模糊背景图片上，位置是(border_width, border_height)
    blurred_background.paste(rounded_image, (border_width, border_height), rounded_image)

    # 在新图片上绘制文字
    draw = ImageDraw.Draw(blurred_background)

    if font_size is None:
        # 尝试不同的字体大小，直到找到合适的大小
        font_size = int(text_area_height * 0.2)  # 初始字体大小
        font = ImageFont.truetype(font_path, font_size)

        # 获取文字尺寸
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

        # 调整字体大小直到文字合适地放入文字展示区域
        while text_width > new_width - 2 * border_width and font_size > 1:
            font_size -= 1
            font = ImageFont.truetype(font_path, font_size)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    else:
        font = ImageFont.truetype(font_path, font_size)

    # 将文本分行处理
    text_lines = text.strip().split('\n')
    line_heights = []
    for line in text_lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        line_heights.append(text_bbox[3] - text_bbox[1])

    total_text_height = sum(line_heights) + (len(line_heights) - 1) * line_spacing  # 增加行间距

    text_y = original_height + border_height + image_text_margin

    for line, line_height in zip(text_lines, line_heights):
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]

        # 根据对齐方式设置文字的x坐标
        if text_alignment == 'left':
            text_x = border_width
        elif text_alignment == 'right':
            text_x = new_width - border_width - text_width
        else:  # 'center'
            text_x = (new_width - text_width) // 2

        draw.text((text_x, text_y), line, fill=font_color, font=font)
        text_y += line_height + line_spacing  # 增加行间距

    # 保存新的图片
    blurred_background.save(output_path)


def get_exif_info(image_path):
    """
    获取图片的EXIF信息，并返回一个包含这些信息的字典。

    参数：
    image_path (str): 图片的路径。

    返回：
    dict: 包含EXIF信息的字典。
    """
    image = Image.open(image_path)
    info = image._getexif()

    exif_dict = {}
    if info is not None:
        for key, value in info.items():
            tag_name = ExifTags.TAGS.get(key, key)
            exif_dict[tag_name] = value

    exif_base = ExifFormat(exif_dict)._

    exif_info = {
        "相机厂商": exif_base.Make(),
        "机型": exif_base.Model(),
        "照片拍摄时间": exif_base.DateTimeOriginal(),
        "照片拍摄GPSInfo": exif_base.GPSInfo(),
        "快门速度": exif_base.ExposureTime(),
        "光圈大小": exif_base.FNumber(),
        "焦距": exif_base.FocalLength(),
        "等效焦距": exif_base.FocalLengthIn35mmFormat(),
        "ISO": exif_base.ISO(),
        "档位": exif_base.ExposureProgram(),
        "镜头型号": exif_base.LensModel().replace('\x00', ''),
        "镜头厂商": exif_base.LensMake(),
        "曝光补偿": exif_base.ExposureCompensation(),
        "测光模式": exif_base.MeteringMode(),
        "闪光灯": exif_base.Flash(),
        "曝光模式": exif_base.ExposureMode(),
        "白平衡": exif_base.WhiteBalance()
    }

    return exif_info


# 项目基础路径
base_path = os.path.dirname(os.path.abspath(__file__))
# print(base_path)
# 示例调用
image_path = '/Users/kusch/Desktop/摄影/原图/DSC_0235.JPG'
border_size_ratio = 0.07
text_area_ratio = 0.09
font_path = base_path + "/font/Konatu-2.ttf"
output_extension = os.path.splitext(image_path)[1]
output_path = f'./new_image{str(time.time()).split(".")[0]}{output_extension}'
blur_radius = 300  # 增加模糊半径
text_alignment = 'center'  # 可选值：'left', 'center', 'right'
font_color = 'white'  # 设置字体颜色
shadow_offset = (40, 40)  # 设置阴影偏移量
shadow_color = (0, 0, 0, 128)  # 设置阴影颜色和透明度
corner_radius_ratio = 0.05  # 设置圆角半径比例
font_size = 180  # 字体大小
image_text_margin = 80  # 图片和第一行文本之间的间距
line_spacing = 10  # 每行文本之间的间距

# 获取图片的EXIF信息
exif_info = get_exif_info(image_path)

# 构造底部文字
text = f"""
{exif_info["机型"]}
{exif_info["镜头型号"]} {exif_info["快门速度"]} {exif_info["光圈大小"]} {exif_info["焦距"]} {exif_info["ISO"]}
{exif_info["照片拍摄时间"]}
"""
create_image_with_blurred_background(image_path,
                                     border_size_ratio,
                                     text_area_ratio,
                                     text,
                                     font_path,
                                     output_path,
                                     blur_radius,
                                     text_alignment,
                                     font_color,
                                     shadow_offset,
                                     shadow_color,
                                     corner_radius_ratio,
                                     font_size,
                                     image_text_margin,
                                     line_spacing)
print(f"新图片已保存到：{output_path}")
