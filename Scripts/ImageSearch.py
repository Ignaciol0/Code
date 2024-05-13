import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import shutil

class ImageGridApp:
    def __init__(self, root, query):
        self.root = root
        self.root.title("Image Grid Viewer")

        self.image_urls, self.real_urls = self.google_image_search(query) 
        self.visited_urls = []
        self.create_image_grid()

        self.close_button = tk.Button(self.root, text="Close", command=self.close_and_move_images)
        self.close_button.grid(row=len(self.image_urls) // 5 + 1, columnspan=5, pady=10)

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
        path = "C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/Video Output"
        images_downloaded = len([image for image in os.listdir(path) if 'photo' in image])
        image_url = image_results[0]['src']
        image = requests.get(image_url)
        with open(f"{path}/image_{images_downloaded+1}.jpg", "wb") as f:
            f.write(image.content)
        print(f"Image {images_downloaded+1} downloaded successfully!")

    def close_and_move_images(self):
        images = [image for image in os.listdir("C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/Video Output") if 'photo' in image]
        for image in images:
            source_folder = "C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/Video Output"
            output_folder = "C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/images"
            shutil.move(source_folder+image,output_folder)
        root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    query =  "Jeremie Frimpong" # Replace "your_query_here" with your desired query
    app = ImageGridApp(root, query)
    root.mainloop()


def ImageSearch(player):
    root = tk.Tk()
    query =  "Jeremie Frimpong" # Replace "your_query_here" with your desired query
    app = ImageGridApp(root, query)
    root.mainloop()