import cv2
import math

img = cv2.imread('./pdfData/pic/2021-9-25_11-03_1.png', 0)

threshold = 48

ret, threshImg = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

cv2.imwrite('./threshImg.png', threshImg)

for i in range(21):
    upperL = 2 + i * 35 + i * 2
    lowerR = 36 + i * 35 + i * 2 + 1
    if i == 20:
        cv2.imwrite('./10-3.png', threshImg[34:70, upperL:lowerR])
        continue
    cv2.imwrite('./' + str(math.floor(i/2)+1) + '-' + str(i%2+1) + '.png', threshImg[34:70, upperL:lowerR])



#print(threshImg[34:70, 2:37])


#print(sum(sum(0==tI for tI in threshImg[34:70, 2:37])))