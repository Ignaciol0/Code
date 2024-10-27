import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
import shutil
from serpapi import GoogleSearch

class ImageGridApp:
    def __init__(self, root, player):
        self.root = root
        self.player = player
        self.root.title(f"Image Search - {player}")
        
        # Configure API
        self.api_key = 'af1fa8c30b3a1265ea073c76a8bd957295a20f108ba0a6558f815ea7394cbce9'
        
        # Get images
        self.images = self.search_images()
        self.selected_images = []
        
        # Create grid
        self.create_grid()
        
        # Create download button
        self.download_button = tk.Button(root, text="Download Selected", command=self.download_images)
        self.download_button.grid(row=(len(self.images) // 3) + 1, column=1, pady=10)

    def search_images(self):
        params = {
            "api_key": self.api_key,
            "engine": "google",
            "q": f"{self.player} soccer player 2024",
            "tbm": "isch",
            "num": 10
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        return results.get("images_results", [])[:10]

    def create_grid(self):
        self.buttons = []
        for i, img_data in enumerate(self.images):
            try:
                response = requests.get(img_data["original"])
                img = Image.open(BytesIO(response.content))
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                button = tk.Button(self.root, image=photo, relief="raised")
                button.image = photo
                button.grid(row=i//3, column=i%3, padx=5, pady=5)
                button.bind('<Button-1>', lambda e, idx=i: self.toggle_selection(e, idx))
                self.buttons.append(button)
            except Exception as e:
                print(f"Error loading image {i}: {e}")

    def toggle_selection(self, event, idx):
        if idx in self.selected_images:
            self.selected_images.remove(idx)
            event.widget.config(relief="raised")
        else:
            self.selected_images.append(idx)
            event.widget.config(relief="sunken")

    def download_images(self):
        output_dir = "C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/Video Output/photos"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Remove existing photo files
        for filename in os.listdir(output_dir):
            if filename.startswith('photo') and filename.endswith('.jpg'):
                os.remove(os.path.join(output_dir, filename))

        # Download selected images with sequential naming
        for i, idx in enumerate(self.selected_images, 1):
            try:
                response = requests.get(self.images[idx]["original"])
                output_path = os.path.join(output_dir, f"photo{i}.jpg")
                
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: photo{i}.jpg")
            except Exception as e:
                print(f"Error downloading image {i}: {e}")

        self.root.destroy()

def ImageSearch(player):
    root = tk.Tk()
    app = ImageGridApp(root, player)
    root.mainloop()

# Example usage
if __name__ == "__main__":
    ImageSearch("Jeremie Frimpong")
