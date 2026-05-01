import cv2
import numpy as np

def read_image(file_path):
    # Read the image
    img = cv2.imread(file_path)
    if img is None:
        print("Error: Image not found")
    return img

def convert_to_gray(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def apply_gaussian_blur(image):
    # Apply a Gaussian blur to the image
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    return blur

def detect_edges(image):
    # Apply edge detection to the image
    edges = cv2.Canny(image, 50, 150)
    return edges

def display_image(title, image):
    # Display the image
    cv2.imshow(title, image)

def main():
    file_path = 'image.jpg'
    img = read_image(file_path)
    if img is not None:
        gray = convert_to_gray(img)
        blur = apply_gaussian_blur(gray)
        edges = detect_edges(blur)

        display_image('Original', img)
        display_image('Grayscale', gray)
        display_image('Blurred', blur)
        display_image('Edges', edges)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
