from imageTools.baseClass.ExifBaseClass import ExifBase
from imageTools.baseClass.cameras.NikonExfi import NikonExif
from imageTools.baseClass.cameras.SonyExfi import SonyExif


class ExifFormat:
    def __init__(self, exif=None):
        self.exif = exif or {}
        self.exifIns = None
        self.exifClassRecord = {
            'NIKON': NikonExif,
            'SONY': SonyExif,
        }
        self.init()
        self.insExif()

    @property
    def _(self):
        return self.exifIns

    @property
    def oriExif(self):
        return self.exif

    def init(self):
        if self.exif.get('Make'):
            self.exif['Make'] = self.exif['Make'].replace('CORPORATION', '').strip()

    def insExif(self):
        Classes = self.exifClassRecord.get(self.exif.get('Make'))
        if Classes:
            self.exifIns = Classes(self.exif)
        else:
            self.exifIns = ExifBase(self.exif)
