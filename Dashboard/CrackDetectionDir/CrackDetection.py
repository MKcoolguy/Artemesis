# importing necessary libraries
import cv2
import numpy as np


# read a cracked sample image
def do_this(img):
    #img = cv2.imread(img)
    count = 0

    # Convert into gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Image processing ( smoothing )
    # Averaging
    blur = cv2.blur(gray,(3,3))

    # Apply logarithmic transform
    img_log = (np.log(blur+1)/(np.log(1+np.max(blur))))*255

    # Specify the data type
    img_log = np.array(img_log,dtype=np.uint8)

    # Image smoothing: bilateral filter
    bilateral = cv2.bilateralFilter(img_log, 5, 75, 75)

    # Canny Edge Detection
    edges = cv2.Canny(bilateral,100,200)

    # Morphological Closing Operator
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Create feature detecting method
    # sift = cv2.xfeatures2d.SIFT_create()
    # surf = cv2.xfeatures2d.SURF_create()
    orb = cv2.ORB_create(nfeatures=1500)

    # Make featured Image
    keypoints, descriptors = orb.detectAndCompute(closing, None)
    featuredImg = cv2.drawKeypoints(closing, keypoints, None)

    # Create an output image
    cv2.imwrite('Output-Set/CrackDetected-{}.jpg'.format(count), featuredImg)

    # Return img
    return featuredImg


