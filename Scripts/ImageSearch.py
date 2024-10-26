import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
import shutil
from serpapi import GoogleSearch

class ImageGridApp:
    def __init__(self, root, query):
        self.root = root
        self.root.title("Image Grid Viewer")

        self.query = query
        self.image_urls = self.serpapi_image_search(query)[:10]  # Limit to first 10 results
        self.selected_images = []

        self.create_image_grid()

        self.close_button = tk.Button(self.root, text="Download Selected", command=self.download_selected_images)
        self.close_button.grid(row=len(self.image_urls) // 5 + 1, columnspan=5, pady=10)

    def serpapi_image_search(self, query):
        params = {
            "api_key": 'af1fa8c30b3a1265ea073c76a8bd957295a20f108ba0a6558f815ea7394cbce9',
            "engine": "google_images",
            "q": f"{query}",
            "tbm": "isch",
            "num": "10",
            "ijn": "0",
            "image_type": "photo",
            "safe": "off",
            "filter": "1",
            "tbs": "isz:l"  # This parameter requests large images
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            image_results = results.get("images_results", [])
            return [img["original"] for img in image_results if self.is_valid_image(img)]
        except Exception as e:
            print(f"Error occurred during image search: {e}")
            return []

    def is_valid_image(self, img):
        return img.get("original") is not None and img.get("original_width", 0) >= 800 and img.get("original_height", 0) >= 600

    def create_image_grid(self):
        num_columns = 5
        for index, url in enumerate(self.image_urls):
            try:
                response = requests.get(url, timeout=10)
                image_data = response.content
                image = Image.open(BytesIO(image_data))
                image.thumbnail((200, 200))  # Resize image to fit in grid
                photo = ImageTk.PhotoImage(image)

                label = tk.Label(self.root, image=photo, bd=2, relief="solid")
                label.image = photo
                label.grid(row=index // num_columns, column=index % num_columns, padx=5, pady=5)

                label.bind("<Button-1>", lambda event, index=index: self.toggle_selection(event, index))
            except Exception as e:
                print(f"Error loading image {index}: {e}")

    def toggle_selection(self, event, index):
        label = event.widget
        if index in self.selected_images:
            self.selected_images.remove(index)
            label.config(bd=2, relief="solid")
        else:
            self.selected_images.append(index)
            label.config(bd=2, relief="sunken")

    def download_selected_images(self):
        path = "C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/images"
        for index in self.selected_images:
            url = self.image_urls[index]
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    images_downloaded = len([image for image in os.listdir(path) if 'photo' in image])
                    filename = f"{path}/photo{images_downloaded+1}.jpg"
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    print(f"Image {images_downloaded+1} downloaded successfully!")
                else:
                    print(f"Failed to download image {index+1}: HTTP status {response.status_code}")
            except Exception as e:
                print(f"Error downloading image {index+1}: {e}")
        
        self.root.destroy()

 

def ImageSearch(player):
    root = tk.Tk()
    app = ImageGridApp(root, player)
    root.mainloop()
