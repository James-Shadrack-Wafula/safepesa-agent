import qrcode
import cloudinary
from cloudinary.uploader import upload
from io import BytesIO
class Qr:
    
        # self.text = text
        # self.filename = filename
    # def gen(self):
    #     img = qrcode.make(f'{self.text}')
    #     type(img)
    #     try:
    #         cloudinary.uploader.upload(f"{self.filename}.png")
    #         # img.save(f"/home/jimmy/Documents/AI/qrV1/web/qr/{self.filename}.png")
    #     except Exception as e:
    #         print(e)
    #         return "File exists Exception"

    @staticmethod   
    def gen(text, filename):
        # Generate the QR code image
        img = qrcode.make(f'{text}')

        try:
            # Convert PIL Image to bytes
            img_bytes = img.tobytes()

            img_bytes_io = BytesIO()
            img.save(img_bytes_io, format="PNG")
            img_bytes = img_bytes_io.getvalue()
            # Configure Cloudinary with your credentials
            # cloudinary.config(
            #     cloud_name="your_cloud_name",
            #     api_key="your_api_key",
            #     api_secret="your_api_secret"
            # )

            # Upload the image bytes to Cloudinary
            result = upload(img_bytes, resource_type="image", public_id=filename)

            # Print information about the uploaded image
            print(result)
            print("Uploaded ===========")
        except Exception as e:
            print(e)
            return "File exists Exception"
        
# img = qrcode.make('Some data here')
# type(img)  # qrcode.image.pil.PilImage
# img.save("some_file.png")

#Qr("https://midset-group.org", 'mindset').gen()
        
# def gen():
#         img = qrcode.make("Example_qr")
#         type(img)
#         try:
#             cloudinary.uploader.upload(img)
#             # img.save(f"/home/jimmy/Documents/AI/qrV1/web/qr/{self.filename}.png")
#             print("Uploaded ===========")
#         except Exception as e:
#             print(e)
#             return "File exists Exception"
        

def gen(filename):
    # Generate the QR code image
    img = qrcode.make("Example_qr 2")

    try:
        # Convert PIL Image to bytes
        img_bytes = img.tobytes()

        img_bytes_io = BytesIO()
        img.save(img_bytes_io, format="PNG")
        img_bytes = img_bytes_io.getvalue()
        # Configure Cloudinary with your credentials
        # cloudinary.config(
        #     cloud_name="your_cloud_name",
        #     api_key="your_api_key",
        #     api_secret="your_api_secret"
        # )

        # Upload the image bytes to Cloudinary
        result = upload(img_bytes, resource_type="image", public_id=filename)

        # Print information about the uploaded image
        print(result)
        print("Uploaded ===========")
    except Exception as e:
        print(e)
        return "File exists Exception"

        
#gen("Sendon Example")