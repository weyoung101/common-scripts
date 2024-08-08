from imageTools.baseClass.ExifBaseClass import ExifBase
from imageTools.utils.RomanUtil import to_roman


class NikonExif(ExifBase):
    def Model(self):
        v = (self.exif.get('Model', '')
             # .replace(self.exif.get('Make', '').upper(), '')
             .replace('Z', 'ℤ')
             .replace('z', 'ℤ'))
        arr = v.split('_')
        if len(arr) > 1:
            i = arr.pop()
            if i and i.isdigit():
                return f"{' '.join(arr)} {to_roman(int(i))}"
            return f"{' '.join(arr)} {i}"
        return v
