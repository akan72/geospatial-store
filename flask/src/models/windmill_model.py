import os
import cv2
import numpy as np
import matplotlib

matplotlib.use('agg')

def predict_windmill_orientation(filepath: str)-> str:
    """ Predict the orientation of an image containing a windmill

    Args:
        filepath [str]: The path to the image within the static/uploads directory

    Returns 
        str: The path to the processed image
    """
    # Input the image 
    img = cv2.imread(filepath)

    # Canny and hough lines required a monochrome image, so we convert the image to black and white
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    # Blur the gray image by a little to remove bright artifacts
    blur = cv2.blur(gray,(3,3))
    
    # Threshold the image. I chose this lower limit arbitrarily based on what gave the best results
    ret,thresh1 = cv2.threshold(blur,180,255,cv2.THRESH_TOZERO)
    
    # Remove artifacts using median blur
    thresh1 = cv2.medianBlur(thresh1,5)

    # OPTIONAL: perform Canny edge detection. This produced inferior results so I commented it out
    #edges = cv2.Canny(thresh1,10,30,apertureSize = 3)
    
    # Perform Hough line transform
    minLineLength = 20
    maxLineGap = 50
    lines = cv2.HoughLinesP(thresh1,1,np.pi/180,100,minLineLength,maxLineGap)
    
    # add lines to the image
    for l in lines:
        x1,y1,x2,y2 = l[0]
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),5)
        
    upload_idx = filepath.find('uploads/')
    output_path = 'src/app/static/output/windmills/'  + filepath[upload_idx+8:]

    # upload_idx = filepath.find('windmills/') 
    # output_path = 'data/processed/windmills/' + filepath[upload_idx+10:]

    # save image
    matplotlib.pyplot.imshow(img)
    matplotlib.pyplot.savefig(output_path)

    return output_path
