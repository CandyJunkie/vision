import cv2

def viewImage(image, name_of_window = "default"):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    img = cv2.imread(r'C:\Users\admin\PycharmProjects\vision\image.png')

    HSV_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    BGR_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    mono_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, bin_img = cv2.threshold(mono_img, 127, 255, cv2.THRESH_BINARY)
    canny_img = cv2.Canny(img, 100, 200)

    viewImage(img, 'Original image')
    viewImage(HSV_img, 'image -> HSV')
    viewImage(BGR_img, 'image -> BGR')
    viewImage(mono_img, 'image -> monochrome')
    viewImage(bin_img, 'image -> binary')
    viewImage(canny_img, 'image + canny')


main()