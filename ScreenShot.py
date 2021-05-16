# import imutils
# import pyautogui
# import cv2
# import os
import pyscreenshot

# def Take_Screenshot(filename):
#     pyautogui.screenshot(filename)
#     image = cv2.imread(filename)
#     cv2.imshow("image", imutils.resize(image, width=600))
#     cv2.waitKey(0)

def Take_Screenshot(filename):
    image = pyscreenshot.grab()
  
    # To display the captured screenshot
    # image.show()
    
    # To save the screenshot
    image.save(filename)



# 259172: Screen shot


# with open("ScreenShot.png","rb") as file:
#     print(get_Size(file))

# with open("ScreenShotFromServer.png","rb") as file:
#     print(get_Size(file))

    


    