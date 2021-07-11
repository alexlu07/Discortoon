from google_images_search import GoogleImagesSearch
import os
import random


class ImageScraper:
    def __init__(self):
        with open("credentials.txt", "r") as f:
            _ = f.readline().strip()
            self.api_key = f.readline().strip()
            self.project_cx = f.readline().strip()

        self.image_dir = "./random"
        self.num_searches = 5

        self.searches = {"clean cartoon jokes": 0, "clean cartoon memes": 0, "clean anime jokes": 0, "clean anime memes": 0}

    def search(self):
        for f in os.scandir(self.image_dir):
            os.remove(f.path)

        gis = GoogleImagesSearch(self.api_key, self.project_cx)

        random_search = random.choice(list(self.searches.items()))
        gen_num = (random_search[1]+1) * self.num_searches
        del_num = random_search[1] * self.num_searches

        gis.search({'q': random_search[0], 'num': gen_num}, path_to_dir=self.image_dir, custom_image_name="image")

        files = sorted(os.listdir(self.image_dir))
        for i in range(-1, del_num-1):
            os.remove(os.path.join(self.image_dir, files[i]))

        self.searches[random_search[0]] += 1

        print(self.searches)
