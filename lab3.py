import cv2
import numpy as np

DEBUG = True

def nothing(x):
    pass

def main():
    cap = cv2.VideoCapture('project_video.mp4')
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    # Parameters of the ROI
    IMAGE_H = 1024
    IMAGE_W = 1280

    src = np.float32([[0, IMAGE_H], [IMAGE_W, IMAGE_H], [0, 0], [IMAGE_W, 0]])

    topWidth = 0
    botWidth = 570
    topHeight = 724
    botHeight = 0

    cv2.namedWindow('Frame')

    cv2.createTrackbar("top width", "Frame", topWidth, 600, nothing)
    cv2.createTrackbar("bot width", "Frame", botWidth, 600, nothing)
    cv2.createTrackbar("top hight", "Frame", topHeight, 900, nothing)
    cv2.createTrackbar("bot hight", "Frame", botHeight, 600, nothing)

    frame_width = int(max(IMAGE_W - 2 * topWidth, IMAGE_W - 2 * botWidth))
    frame_height = int(IMAGE_H - topHeight - botHeight)

    # Press 'S' to start
    while not (cv2.waitKey(25) & 0xFF == ord('s')):
        continue

    topWidth = cv2.getTrackbarPos("top width", "Frame")
    botWidth = cv2.getTrackbarPos("bot width", "Frame")
    topHeight = cv2.getTrackbarPos("top hight", "Frame")
    botHeight = cv2.getTrackbarPos("bot hight", "Frame")

    out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
    dst = np.float32([[botWidth, IMAGE_H - topHeight], [IMAGE_W - botWidth, IMAGE_H - topHeight], [topWidth, botHeight],
                      [IMAGE_W - topWidth, botHeight]])
    M = cv2.getPerspectiveTransform(src, dst)  # The transformation matrix

    # Read until video is completed
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret == True:
            # Bird's eye stuff
            # 460 is the start of the road
            frame = frame[460:(460 + frame_height), 0:IMAGE_W]  # Apply np slicing for ROI crop
            warped_frame = cv2.warpPerspective(frame, M, (frame_width, frame_height))  # Image warping

            # canvas
            hsv_img = cv2.cvtColor(warped_frame, cv2.COLOR_RGB2HSV)
            color_from = np.array([0, 0, 165])
            color_to = np.array([360, 255, 255])

            mask = cv2.inRange(hsv_img, color_from, color_to)
            range_img = cv2.bitwise_and(hsv_img, hsv_img, mask=mask)

            warped2 = cv2.cvtColor(range_img, cv2.COLOR_HSV2RGB)

            # Write warped frame in output file
            out.write(warped2)

            if DEBUG == True:
                # Display the resulting frame. Needed for debug
                cv2.imshow('Frame', warped2)

                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

        # Break the loop
        else:
            break

    # When everything done, release the video capture object and close the frames
    cap.release()
    out.release()
    cv2.destroyAllWindows()



main()