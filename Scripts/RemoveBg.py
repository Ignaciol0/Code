from rembg import remove
from PIL import Image
def remove_bg(photo):
    if len(photo[0]) != 1:
        for image in photo:
            image_input = Image.open(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\images\{image}')
            output = remove(image_input)
            output.save(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Video Output\\{image.split(".")[0]}_nbg.png')
    else:
        image_input = Image.open(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\images\{photo}')
        output = remove(image_input)
        output.save(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Video Output\\{photo.split(".")[0]}_nbg.png')
   
