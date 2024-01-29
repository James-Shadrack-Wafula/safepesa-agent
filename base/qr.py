import qrcode
class Qr:
    def __init__(self,text, filename):
        
        self.text = text
        self.filename = filename
    def gen(self):
        img = qrcode.make(f'{self.text}')
        type(img)
        try:
            img.save(f"/home/jimmy/Documents/AI/qrV1/web/qr/{self.filename}.png")
        except Exception as e:
            print(e)
            return "File exists Exception"
# img = qrcode.make('Some data here')
# type(img)  # qrcode.image.pil.PilImage
# img.save("some_file.png")

Qr("https://midset-group.org", 'mindset').gen()