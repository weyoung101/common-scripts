from imageTools.baseClass.ExifBaseClass import ExifBase

class SonyExif(ExifBase):
    def Model(self):
        return self.exif.get('Model', '').replace('ILCE-', 'α').lower()
