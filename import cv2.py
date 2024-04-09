import cv2
import numpy as np

# Read the image
img = cv2.imread('image.jpg')

# Check if the image was successfully loaded
if img is None:
    print("Error: Image not found")
else:
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur to the image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply edge detection to the image
    edges = cv2.Canny(blur, 50, 150)

    # Display the original image
    cv2.imshow('Original', img)

    # Display the grayscale image
    cv2.imshow('Grayscale', gray)

    # Display the blurred image
    cv2.imshow('Blurred', blur)

    # Display the edge detected image
    cv2.imshow('Edges', edges)

    # Wait for the user to press a key
    cv2.waitKey(0)

    # Close all windows
    cv2.destroyAllWindows()
