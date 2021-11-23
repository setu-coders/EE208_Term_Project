import cv2
from cv2 import cv2 # make vscode not complain
from matplotlib import pyplot as plt
import numpy as np
def calcGradient(img):
    HEIGHT, WIDTH = img.shape[0], img.shape[1]
    img_grad = np.zeros((HEIGHT - 2,WIDTH - 2))
    for x in range(1,HEIGHT - 1):
        for y in range(1,WIDTH - 1):
            grad_x = img[x+1][y] - img[x-1][y]
            grad_y = img[x][y+1] - img[x][y-1]
            grad_xy = (grad_x ** 2 + grad_y ** 2) ** 0.5
            img_grad[x - 1][y - 1] = grad_xy
    return img_grad

def plotGRAY(filename):
    SAVEDIR = 'plot/'
    READDIR = 'images/'
    img_gray = cv2.imread(READDIR + filename,cv2.IMREAD_GRAYSCALE).astype(int)
   
    img_grad = calcGradient(img_gray)
    bins = np.array(range(int(np.max(img_grad))))  - 0.01  # 防止值落在边界上
    plt.hist(img_grad.ravel(),bins=bins,density=True,rwidth=1)
    
    plt.title('Gradient Histogtam of ' + filename)
    plt.savefig(SAVEDIR + filename +'_GRAD_Hist.png')
    #plt.show()
    plt.close()

    

if __name__ == '__main__':
    files = [
    'img1.jpg',
    'img2.jpg',
    'img3.jpg'
    ] 
    for file in files:
        plotGRAY(file)  




