from rembg import remove
from PIL import Image
def remove_bg(photo):
    if type(photo) == "list":
        for image in photo_list:
            image_input = Image.open(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\images\{image}.jpg')
            output = remove(image_input)
            output.save(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\\{image}_nbg.png')
    else:
        image_input = Image.open(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\images\{photo}.jpg')
        output = remove(image_input)
        output.save(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\\{photo}_nbg.png')
   
remove_bg("photo2")