import cv2
import numpy as np
from PIL import ImageGrab
from PIL import Image
from mss import mss
import os

# img = ImageGrab.grab(bbox=(100,10,400,780)) #bbox specifies specific region (bbox= x,y,width,height *starts top-left)
# img_np = np.array(img) #this is the array obtained from conversion
# frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
# cv2.imshow("test", frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
class unlockManifolds:
    mainScreen = {
        'top': 350,
        'bottom': 350,
        'left': 550,
        'right': 550
    }

    position0 = {
        'top': 400,
        'bottom': 550,
        'left': 590,
        'right': 1200
    }

    position1 = {
        'top': 400,
        'bottom': 550,
        'left': 740,
        'right': 1050
    }

    position2 = {
        'top': 400,
        'bottom': 550,
        'left': 900,
        'right': 900
    }

    position3 = {
        'top': 400,
        'bottom': 550,
        'left': 1050,
        'right': 740
    }

    position4 = {
        'top': 400,
        'bottom': 550,
        'left': 1200,
        'right': 600
    }

    position5 = {
        'top': 550,
        'bottom': 410,
        'left': 590,
        'right': 1200
    }

    position6 = {
        'top': 550,
        'bottom': 410,
        'left': 740,
        'right': 1050
    }

    position7 = {
        'top': 550,
        'bottom': 410,
        'left': 900,
        'right': 900
    }

    position8 = {
        'top': 550,
        'bottom': 410,
        'left': 1050,
        'right': 740
    }

    position9 = {
        'top': 550,
        'bottom': 410,
        'left': 1200,
        'right': 600
    }  

    def getPosition(self, index):
        if index == 0:
            return self.position0
        elif index == 1:
            return self.position1
        elif index == 2:
            return self.position2
        elif index == 3:
            return self.position3
        elif index == 4:
            return self.position4
        elif index == 5:
            return self.position5
        elif index == 6:
            return self.position6
        elif index == 7:
            return self.position7
        elif index == 8:
            return self.position8
        elif index == 9:
            return self.position9
        else:
            return None

# mon = {'top': unlockManifolds.mainScreen['top'], 'left': unlockManifolds.mainScreen['left'], 'width': 1920 - unlockManifolds.mainScreen['left'] - unlockManifolds.mainScreen['right'], 'height': 1080 - unlockManifolds.mainScreen['top'] - unlockManifolds.mainScreen['bottom']}
# position = 9
mons = []
for i in range(10):
    mon = {'top': unlockManifolds().getPosition(i)['top'], 'left': unlockManifolds().getPosition(i)['left'], 'width': 1920 - unlockManifolds().getPosition(i)['left'] - unlockManifolds().getPosition(i)['right'], 'height': 1080 - unlockManifolds().getPosition(i)['top'] - unlockManifolds().getPosition(i)['bottom']}
    mons.append(mon)

sct = mss()
folderCount = 0
for _, dirnames, _ in os.walk('output/'):
    folderCount += len(dirnames)

imageSavedCount = folderCount
images = []
while 1:
    if cv2.waitKey(25) == ord('i'):
        if len(images) != 0:
            print('saving images #{}'.format(imageSavedCount))
            os.mkdir('output/{}'.format(imageSavedCount))
            for i in range(len(images)):
                cv2.imwrite('output/{}/{}.jpg'.format(imageSavedCount,i), images[i])
            imageSavedCount = imageSavedCount + 1
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    images = []

    for i in range(len(mons)):
        mon = mons[i]
        sct.get_pixels(mon)
        img = np.array(Image.frombytes('RGB', (sct.width, sct.height), sct.image))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        imS = cv2.resize(img, (256, 256)) # Resize image
        imgGray = cv2.cvtColor(imS, cv2.COLOR_RGB2GRAY)
        edged = cv2.Canny(imgGray, 30, 200) 
        ret, thrash = cv2.threshold(edged, 240 , 255, cv2.CHAIN_APPROX_NONE)
        contours, hierarchy = cv2.findContours(thrash,  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # for cnt in contours:
        #     size = cv2.contourArea(cnt)
        #     if 10000 < size:
        #         cv2.drawContours(imS, cnt, -1, (0, 230, 255), 3)
        # print("Number of Contours found = " + str(len(contours))) 
        cv2.imshow('test {}'.format(i), thrash.copy())
        images.append(thrash.copy())
        