import cv2
from matplotlib import pyplot as plt
import numpy as np
def countRGB(img):
    RGB = np.array([0,0,0])
    for line in img:
        for item in line:
            RGB += item
    return RGB

def plotRGB(filename):
    SAVEDIR = 'plot/'
    READDIR = 'images/'
    img_bgr = cv2.imread(READDIR + filename)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    RGB = countRGB(img_rgb)
    
    name_list = ['R','G','B']
    X = [1,2,3]
    Y = RGB / np.sum(RGB)
    plt.bar(X,Y ,color=['r','g','b'],tick_label=name_list)
    for a,b in zip(X,Y):  
        plt.text(a, b, round(b,3) , ha='center', va= 'bottom',fontsize=11)  
        plt.title('RGB Bar graph of ' + filename)
    #plt.show()
    plt.savefig(SAVEDIR + filename +'_RGB_Bar.png')
    plt.close()

if __name__ == '__main__':
    files = [
    'img1.jpg',
    'img2.jpg',
    'img3.jpg'
    ] 
    for file in files:
        plotRGB(file)  




