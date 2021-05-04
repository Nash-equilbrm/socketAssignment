import imutils
import pyautogui
import cv2



def Take_Screenshot(filename):
    pyautogui.screenshot(filename)
    image = cv2.imread(filename)
    cv2.imshow("image", imutils.resize(image, width=600))
    cv2.waitKey(0)


    