import numpy as np
import cv2

# Function to save snapshots when a crack is detected
def save_snapshots(video_feed, snapshot_path):
    # read a cracked sample image
    count = 0

    while(video_feed.isOpened()):
        # Read the frame
        ret, frame = video_feed.read()

        if ret:
            # Convert into gray scale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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

            if len(keypoints) > 0:
                # Save snapshot if crack detected
                cv2.imwrite(snapshot_path, frame)
                break

            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release the video capture
    video_feed.release()
