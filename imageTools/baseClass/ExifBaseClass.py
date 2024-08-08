class ExifBase:
    def __init__(self, exif=None):
        self.exif = exif or {}

    # 相机厂商
    def Make(self, v=None):
        v = v or self.exif.get('Make')
        return v[0] + v[1:].lower() if v else ''

    # 机型 Nikon Z 30
    def Model(self, v=None):
        v = v or self.exif.get('Model')
        return v.lower() if v else ''

    # 照片拍摄时间
    def DateTimeOriginal(self, v=None):
        v = v or self.exif.get('DateTimeOriginal')
        return v

    # 照片拍摄地点
    def GPSInfo(self, v=None):
        v = v or self.exif.get('GPSInfo')
        return v

    # 快门速度
    def ExposureTime(self, v=None):
        v = v or self.exif.get('ExposureTime')
        if not v:
            return ''
        if v < 1:
            return f"1/{round(1 / v)}"
        return str(v)

    # 光圈大小
    def FNumber(self, v=None):
        v = v or self.exif.get('FNumber')
        return v

    # 焦距
    def FocalLength(self, v=None):
        v = v or self.exif.get('FocalLength')
        return round(v) if v else ''

    # 等效焦距
    def FocalLengthIn35mmFormat(self, v=None):
        v = v or self.exif.get('FocalLengthIn35mmFormat')
        return round(v) if v else ''

    # ISO
    def ISO(self, v=None):
        v = v or self.exif.get('ISO')
        return v or ''

    # 档位
    def ExposureProgram(self, v=None):
        v = v or self.exif.get('ExposureProgram')
        return v

    # 镜头型号
    def LensModel(self):
        return self.exif.get('LensModel', '')

    # 镜头厂商
    def LensMake(self):
        return self.exif.get('LensMake', '')

    # 曝光补偿
    def ExposureCompensation(self):
        return self.exif.get('ExposureCompensation')

    # 测光模式
    def MeteringMode(self):
        return self.exif.get('MeteringMode')

    # 闪光灯
    def Flash(self):
        return self.exif.get('Flash')

    # 曝光模式
    def ExposureMode(self):
        return self.exif.get('ExposureMode')

    # 白平衡
    def WhiteBalance(self):
        return self.exif.get('WhiteBalance')
