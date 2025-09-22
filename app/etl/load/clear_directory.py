import os

def clear_directory(path):
        for file in os.listdir(path):
            item_path = os.path.join(path, file)
            if os.path.isfile(item_path):
                os.remove(item_path)