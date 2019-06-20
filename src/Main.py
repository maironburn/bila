from common_config import IMG_DIRS
import numpy as np
import cv2

'''
cv2.IMREAD_COLOR : Loads a color image. Any transparency of image will be neglected. It is the default flag. (-1)
cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode (0) 
cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel (1)

'''

# lectura de las imagenes
# searched_image = cv2.imread("{}{}{}".format(IMG_DIRS, "\\", "domicilio_table_col.png"), cv2.IMREAD_GRAYSCALE)
searched_image = cv2.imread("{}{}{}".format(IMG_DIRS, "\\", "guardar_icon_main_window_32_32.png"), cv2.IMREAD_COLOR)
container_image = cv2.imread("{}{}{}".format(IMG_DIRS, "\\", "root_image.png"), cv2.IMREAD_COLOR)

result = cv2.matchTemplate(container_image, searched_image, cv2.TM_CCOEFF_NORMED)
# minimum squared difference
threshold = 0.8
loc = np.where(result >= threshold)


methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']


if len(loc) and len(loc[0]):
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)


    # Draw the rectangle:
    # Extract the coordinates of our best match
    MPx, MPy = mnLoc

    # Step 2: Get the size of the template. This is the same size as the match.
    trows, tcols = searched_image.shape[:2]

    # Step 3: Draw the rectangle on large_image
    cv2.rectangle(container_image, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 0, 255), 2)
    # Display the original image with the rectangle around the match.
    cv2.imshow('output', container_image)

    # The image is only displayed if we call this
    cv2.waitKey(0)

else:
    print("{}".format("NO Matchig"))
