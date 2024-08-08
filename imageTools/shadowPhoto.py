import time

from PIL import Image

from imageTools.baseClass.ExifFormat import ExifFormat

# 图片文件
image = Image.open('/Users/kusch/Desktop/摄影/原图/DSC_0235.JPG')


# 生成图片缩略图
def generateThumbnail():
    size = (image.size[0] / 10, image.size[1] / 10)
    outfile = "./" + str(time.time()).split('.')[0] + ".png"
    print("原始图片信息：", image.mode, image.size, image.format)
    image.thumbnail(size)
    image.convert('RGB')
    image.save(outfile)
    img = Image.open(outfile)
    print("缩略图信息：", img.mode, img.size, img.format)


# 读取图片的Exif信息
def getExfiInfo():
    info = image._getexif()
    # 将EXIF数据转换为一个字典
    exif_dict = {}
    if info is not None:
        for key, value in info.items():
            tag_name = Image.ExifTags.TAGS.get(key, key)
            exif_dict[tag_name] = value
    # 使用ExifBase类处理EXIF数据
    # exif_base = NikonExif(exif_dict)
    exif_base = ExifFormat(exif_dict)._

    # 示例：打印相机厂商和机型
    print("相机厂商:", exif_base.Make())
    print("机型:", exif_base.Model())
    print("照片拍摄时间:", exif_base.DateTimeOriginal())
    print("照片拍摄GPSInfo:", exif_base.GPSInfo())
    print("快门速度:", exif_base.ExposureTime())
    print("光圈大小:", exif_base.FNumber())
    print("焦距:", exif_base.FocalLength())
    print("等效焦距:", exif_base.FocalLengthIn35mmFormat())
    print("ISO:", exif_base.ISO())
    print("档位:", exif_base.ExposureProgram())
    print("镜头型号:", exif_base.LensModel())
    print("镜头厂商:", exif_base.LensMake())
    print("曝光补偿:", exif_base.ExposureCompensation())
    print("测光模式:", exif_base.MeteringMode())
    print("闪光灯:", exif_base.Flash())
    print("曝光模式:", exif_base.ExposureMode())
    print("白平衡:", exif_base.WhiteBalance())

    # 示例：打印所有的EXIF数据
    # for tag, value in info.items():
    #     decoded = TAGS.get(tag, tag)
    #     print(decoded, value)


# 主函数
if __name__ == '__main__':
    # generateThumbnail()
    getExfiInfo()
