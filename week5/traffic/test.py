import os
import sys
import cv2
from PIL import Image
EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4

def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    load_data(sys.argv[1])

def load_data(data_dir):
    ''''file_path = os.path.abspath(data_dir)
    for i in range(NUM_CATEGORIES):
        current_path = os.path.join(file_path,str(i))
        print(current_path)
        for image in os.listdir(current_path):
            img = Image.open(image)
            numpydata = asarray(img)
            #image = cv2.resize(image1,(IMG_WIDTH,IMG_HEIGHT))
            print(numpydata.shape)'''
    #initial lits for images and labels
    images = []
    labels = []

    #define path to file folder
    path_to_folder = os.path.abspath(data_dir)

    #save list of labels
    categories = [f for f in os.listdir(path_to_folder)]

    for category in categories:
        path_to_category = os.path.join(path_to_folder,f"{category}")

        dirs = os.listdir(path_to_category)

        for file in dirs:
            path_to_file = os.path.join(path_to_folder,f"{category}",f"{file}")

            img = cv2.imread(path_to_file)
            img = cv2.resize(img,(IMG_WIDTH,IMG_HEIGHT))
            print(img)

            #images.append(img)
            #labels.append(category)
    
    return (images,labels)    
if __name__ == '__main__':
    main()

