import skimage.io as io
import numpy as np

c_HIDDEN_IMG_H = 131
c_HIDDEN_IMG_W = 100
c_HIDDEN_IMG_P = 3 # initiated hidden image dimentions to be used throughout the class in different methods

class ImageAnalysis:

    def __init__(self, imagename):
        self.image = io.imread(imagename)
        self.hiddenimage = None # initiated hidden image to be applied to both retrieveHidden and averageRGB

    def show (self):
        io.imshow(self.image)
        io.show()

    def __str__(self):
        return "Shape is: {0}".format(self.image.shape)

    def retriveHidden (self):
        self.hiddenimage = np.zeros((c_HIDDEN_IMG_H, c_HIDDEN_IMG_W, c_HIDDEN_IMG_P))
        i = 0
        while i < c_HIDDEN_IMG_H:
            j = 0
            while j < c_HIDDEN_IMG_W:
                self.hiddenimage[i,j] = self.image[i*11,j*11]
                j += 1
            i+= 1
        io.imsave("hidden.png", self.hiddenimage)
        print('Shape of hidden image is: ', self.hiddenimage.shape) # used to make sure shape is accurate

    def fix (self):
        i = 0
        fixedimage = self.image.copy() #copies the original image to seperate the memory locations for the image to be fixed and the original
        while i < c_HIDDEN_IMG_H:
            j = 0
            while j < c_HIDDEN_IMG_W:
                fixedimage[i*11,j*11] = self.average([i*11,j*11]) # used another method to define the averaging to seperate and so that it is easier to fix either loops
                j += 1
            i+= 1
        io.imsave("fixed.png", fixedimage)
        print ("Shape of fixed image is: ", fixedimage.shape) # to make sure the shape is correct
    
    def average (self, position):
        i = position[0]
        j = position[1]
        pixeltot = np.zeros([])
        
        pixel2 = self.image[i+1,j]
        pixel4 = self.image[i,j+1] # calculated these two seperately since these two always need to be calculated throughout the pixel fixing

        pixeltot = np.sum([pixel2, pixel4], axis=0)
        n_pix = 2 

        if i > 0: # checking if edge condition is not i=0 since then it would need pixel1
            pixel1 = self.image[i-1,j]
            pixeltot = np.sum([pixel1, pixeltot], axis = 0)
            n_pix += 1 # adding 1 since one more pixel is added to the average
        
        if j > 0: # checking if edge condition is not j=0 since then it would need pixel3
            pixel3 = self.image[i,j-1]
            pixeltot = np.sum([pixel3, pixeltot], axis = 0)
            n_pix += 1 # adding 1 since one more pixel is added to the average
        
        pixelavg = pixeltot / n_pix
        return pixelavg

    def averageRGB (self):
        avgarray = np.zeros((c_HIDDEN_IMG_H,c_HIDDEN_IMG_W)) # applied size of hidden image to new array of the average values
        for i in range(c_HIDDEN_IMG_H):
            for j in range(c_HIDDEN_IMG_W):
                total = self.hiddenimage[i,j,0] + self.hiddenimage[i,j,1] + self.hiddenimage[i,j,2]
                average = total / 3
                avgarray[i,j] = int(average) # converts to integers as it comes out as float
        np.savetxt("RGB.csv", avgarray, delimiter=",")

    def load_rgb_from_file (self, csv_file):
        average = np.genfromtxt(csv_file, delimiter=',')
        newarray = np.zeros((c_HIDDEN_IMG_H, c_HIDDEN_IMG_W, c_HIDDEN_IMG_P), dtype=np.uint8) #initiating this to be integers as only integer rgb values allowed
        for i in range(c_HIDDEN_IMG_H):
            for j in range(c_HIDDEN_IMG_W):
                newarray[i,j] = [average[i,j], average[i,j], average[i,j]] # implementing the average into each rgb value
        io.imshow(newarray)
        io.show()

i = ImageAnalysis("mountain.png")
# print(i)
i.retriveHidden()
i.fix()
# i.show()
i.averageRGB()
i.load_rgb_from_file('RGB.csv')