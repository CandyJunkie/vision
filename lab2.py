import cv2
import numpy as np

DEBUG = True

def main():
    cap = cv2.VideoCapture('project_video.mp4')
    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    IMAGE_H = 300
    IMAGE_W = 1280

    frame_width = int(IMAGE_W)
    frame_height = int(IMAGE_H)

    out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

    src = np.float32([[0, IMAGE_H], [IMAGE_W, IMAGE_H], [0, 0], [IMAGE_W, 0]])
    dst = np.float32([[570, IMAGE_H], [IMAGE_W-570, IMAGE_H], [0, 0], [IMAGE_W, 0]])
    M = cv2.getPerspectiveTransform(src, dst)  # The transformation matrix
    Minv = cv2.getPerspectiveTransform(dst, src)  # Inverse transformation

    # Read until video is completed
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            # Bird's eye stuff
            frame = frame[460:(460 + IMAGE_H), 0:IMAGE_W]  # Apply np slicing for ROI crop
            warped_frame = cv2.warpPerspective(frame, M, (IMAGE_W, IMAGE_H))  # Image warping

            # Write warped frame in output file
            out.write(warped_frame)

            if DEBUG == True:
                # Display the resulting frame. Needed for debug
                cv2.imshow('Frame', warped_frame)

                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()
    out.release()

    # Closes all the frames
    cv2.destroyAllWindows()



main()