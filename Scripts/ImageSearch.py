import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import tkinter as tk
from PIL import Image, ImageTk
import os


# Example usage
query = "Jeremie Frimpong"


images = ['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAIXM7r0oB_aqs_1dOaq6t_WgxthzN8LlzmEFq__By2yoUvoAEoNEXVcAutQ&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQsa_G8Ke7eGmRxPE8gkwOj7TdJ2mWTJx36zg4tDSTEtMLJSAlX632AkW9qWw&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6RGBVbXJeLardmLMqpVJ4aFoM5jSffTeDSn4CzDh8YivYBMK0zYdcbwIKg6w&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYJd_mzNO4TO8r50rznnmvw027xqpCkKXAxB0743fBlNLClMbTq1CA4UWf_Q&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSC5f6CGA6sFn6FIvk5BbES1p2HwAW8nQ2NheW4hdCPOItg1cZ2xIAgWE2in5A&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwuceAsyJluAps6RWsL3Yx8ymbRvj1NU95K-SGiQ13_VdlIK7y1t5qEL6jFQ&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRH4nnbPdjsrB8g3mm3RMeOfYjRj54JjUsFkQpFK9GpIk_yspeTlpK7CivzEcw&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSM1CmSCDFWCmMhhw0TL_X_IhsEachzmQ40yTbvFwh2Ib4kzdYzkN_GUymGug&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2gqw7UsXowRFlRemEMkwvL2DwSnPC1SyMoma1VIZost8JE9YHmG-mOhaFig&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZtEBTU2zQkDWxY47XeVA4fabgz8L6spseCM-nU4Go2q8vNhS1MDdY6-r3Vg&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5MYWDYGOszStBhocY2ZXo69C8_ycPyiUlX19R23qyob1HBBoyH6XGNIEMKw&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPKdLgJ-sULpU-uO3pN_pfByM-RyC1YD_56rltK2GUP4rirAsOibMltuXhza4&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaF6zB0DLQIy1S0Nw7KSCgb3cXi0mVYegyHCc4jup_zcCGZqQECYYaeOHwShs&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtGlocNKr0Ib_b8gq9J3lNWGj9PS6SLvJDTNGZCTNfjh3lgQiVQxLHVeanCw&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcOFl3crxDUeDoKtBS7CFxrDpZx8WxKhAdPAK7uxMl9xzTFRIhK6KshUjHSi4&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT21Lk7YkENL1jsB_uOS8F7Nesf72zMN3uDws16laKwykQpqsWlUOkLl9BIoRk&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpe9MwVUSzx21ov0Q2LTtKufj1uOzakqhz_ZXngu-dPJxAybJ50uXAfK_b34A&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkrWuL2Pomq7wbfATSI-ir0JL-ZXmhO7K1IT-xbDkK2Y3HHmaQHFmEL7bEjAs&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTIQR5aHaQbkiWaMh8iXAzznZjU419amc1co1lAjV5UsbVRVj94oyvDObORNA&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSE-lwo6wthdZ--UUNUFJ9JlBVkh1Uk4M2ULvJm0v4FCCP41OAK2h559NFq5A&s']

import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

class ImageGridApp:
    def __init__(self, root, query):
        self.root = root
        self.root.title("Image Grid Viewer")

        self.image_urls, self.real_urls = self.google_image_search(query) 

        self.create_image_grid()

    def google_image_search(self, query):
        # Define the base URL
        base_url = "https://www.google.com/search"

        # Define the query parameters as a dictionary
        query_params = {
            "as_st": "y",              # Safe search: 'y' for enabled
            "as_q": query.lower(),# Query: 'jeremie frimpong'
            "as_epq": "",              # Exact phrase query: None specified
            "as_oq": "",               # Additional terms: None specified
            "as_eq": "",               # Excluded terms: None specified
            "imgsz": "xga",            # Image size: 'xga' (1024x768 pixels)
            "imgar": "",               # Aspect ratio: None specified
            "imgcolor": "",            # Image color: None specified
            "imgtype": "",             # Image type: None specified
            "cr": "",                  # Country: None specified
            "as_sitesearch": "",       # Site or domain to search within: None specified
            "as_filetype": "",         # File type: None specified
            "tbs": "",                 # Additional search criteria: None specified
            "udm": "2"                 # Unknown parameter
        }

        # Encode the query parameters
        encoded_params = urlencode(query_params)

        # Construct the full URL
        full_url = f"{base_url}?{encoded_params}"

        # Make the request
        response = requests.get(full_url)


        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            image_results = soup.find_all('a')
            urls = []
            images = []
            for image in image_results:
                url = image['href'].replace("/url?q=","").split("&sa=U&ved")[0]
                if "/search?" not in url and "/?sca" not in url and "google.com" not in url and url not in urls:
                    urls += [url]

            image_results = soup.find_all('img')
            
            for image in image_results:
                link = image['src']
                if 'https' in link:
                    images += [link]
        else:
            print("Failed to retrieve image search results")
        return images, urls

    def create_image_grid(self):
        num_columns = 5  # Number of columns in the grid
        for index, url in enumerate(self.image_urls):
            response = requests.get(url)
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            photo = ImageTk.PhotoImage(image)

            # Create a label for the image and add it to the grid
            label = tk.Label(self.root, image=photo)
            label.image = photo
            label.grid(row=index // num_columns, column=index % num_columns)

            # Bind a click event to each image label
            label.bind("<Button-1>", lambda event, index=index: self.download_image(index))

    def download_image(self, index):
        response = requests.get(self.real_urls[index])
        soup = BeautifulSoup(response.text, 'html.parser')
        image_results = soup.find_all('img')
        images_downladed = len([image for image in os.listdir("C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/Video Output") if 'photo' in image])
        image_url = image_results[0]['src']
        image = requests.get(image_url)
        with open(f"image_{images_downladed+1}.jpg", "wb") as f:
            f.write(image.content)
        print(f"Image {images_downladed+1} downloaded successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageGridApp(root, query)
    root.mainloop()
