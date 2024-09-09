import cv2
import pytesseract
from pytesseract import Output

# Configure the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\lenovo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Load the image
img = cv2.imread('D:/demoimage/image1.jpg')
height, width, _ = img.shape

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding
thresh = cv2.adaptiveThreshold(
    gray, 
    255, 
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    cv2.THRESH_BINARY_INV, 
    11, 
    2
)

# Extract character-level bounding boxes using Tesseract
detection_boxes = pytesseract.image_to_boxes(img, output_type=Output.DICT)
text = pytesseract.image_to_string(img, output_type=Output.STRING)
print(text)
temptext=detection_boxes['char']  
print("text as list",temptext)
# print("as text",temptext)
print("detection_boxes")
print(detection_boxes)
print(len(detection_boxes['left']))
# print("actual text")
# print(text)
# Create a list to store bounding boxes
boxes = []
charactertoaddsymbol = []
charactertoaddspace = []
listofindicesbelow20 = [] 
wordsafterSlice = []
# Collect bounding boxes for each character

# for i in range(len(detection_boxes['char'])-1):
#     x1 = detection_boxes['left'][i]
#     y1 = detection_boxes['top'][i]
#     x2 = detection_boxes['right'][i]
#     y2 = detection_boxes['bottom'][i]
#     char = detection_boxes['char'][i]
#     # print("on",i)
#     x1next = detection_boxes['left'][i+1]
#     y1next = detection_boxes['top'][i+1]
#     x2next = detection_boxes['right'][i+1]
#     y2next = detection_boxes['bottom'][i+1]
#     charnext = detection_boxes['char'][i+1]
#     # Adjust y-coordinates to fit OpenCV's coordinate system
#     y1 = height - y1
#     y2 = height - y2
#     # Store bounding boxes
#     boxes.append((x1, y1, x2, y2,char))

#     if x2<x1next:
#       difference = x1next-x2 
#     #   if difference>20:
#     #     print("character to add symbol")
#     #     print(char,i)
#     #     charactertoaddsymbol.append(i)
#       if difference>2 and difference<10 :
#         print("character to add space")
#         print(char,i)
#         charactertoaddspace.append(i)

# print(boxes)
# # Sort and deduplicate indices to avoid issues
# space_indices  = sorted(charactertoaddspace)

# # print("split indices",split_indices)
# print("space indices",space_indices)
# # Initialize variables for splitting
# j=0
# for index in space_indices:
#     if index <= len(temptext):
#         temptext.insert(index+1+j, ' ')
#     j=j+1

# print("after first itertion")
# print(temptext)
# -----------------------------------------------------------------------------
for i in range(len(temptext)-1):

    if i>= len(temptext)-1:
       break
    x1 = detection_boxes['left'][i]
    y1 = detection_boxes['top'][i]
    x2 = detection_boxes['right'][i]
    y2 = detection_boxes['bottom'][i]
    char = detection_boxes['char'][i]
    prev = detection_boxes['char'][i-1]
    print("on",i)
    x1next = detection_boxes['left'][i+1]
    y1next = detection_boxes['top'][i+1]
    x2next = detection_boxes['right'][i+1]
    y2next = detection_boxes['bottom'][i+1]
    charnext = detection_boxes['char'][i+1]
    # Adjust y-coordinates to fit OpenCV's coordinate system
    y1 = height - y1
    y2 = height - y2
    # Store bounding boxes
    boxes.append((x1, y1, x2, y2,char))

    if x2<x1next:
      difference = x1next-x2 
      if difference>20:
        print("character to add symbol")
        print(char,i)
        charactertoaddsymbol.append(i)


split_indices = sorted(charactertoaddsymbol)
print("split indices",split_indices)
parts = []
previous_index = 0

# Iterate over the split indices
for index in split_indices:
    # Ensure index + 1 is within bounds
    if index <= len(temptext):
        # Append the substring from previous_index to index + 1
        parts.append(''.join(temptext[previous_index:index + 1]))
        previous_index = index + 1

# Append the final part after the last split index
if previous_index < len(temptext):  # Ensure there's remaining text to append
    parts.append(''.join(temptext[previous_index:]))
# Print the results

print("after second iteration")
print("Split parts:", parts)

# Determine significant whitespace areas
# for i in range(len(boxes) - 1):
#     x1, y1, x2, y2 = boxes[i]
#     x1_next, y1_next, x2_next, y2_next = boxes[i + 1]
#     # Identify significant whitespace between characters
#     print("all text")
#     print(text[i])
#     if x2 < x1_next: # There is a gap
#         space_width = x1_next - x2
#         print("spacewidth",space_width)
#         if space_width > 20:  # Adjust threshold for whitespace (lower value for more sensitivity)
#             print("text char")
#             print(text[i])
#             print("greater than 20")
#             print("all values box 1")
#             print(x1, y1, x2, y2)
#             print("all values box 2")
#             print(x1_next,y1_next, x2_next, y2_next)
# Display the result
print("resultant text")
print(text)
cv2.imshow('Whitespace Rectangles', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# space_x1 = x2
# space_y1 = min(y1, y1_next)
# space_x2 = x1_next
# space_y2 = max(y2, y2_next)
# # Append detected whitespace area to list
# space_rectangles.append((space_x1, space_y2, space_x2, space_y1))



# print("text char")
# print(text[i])
# print("all values box 1")
# print(x1, y1, x2, y2)
# print("all values box 2")
# print(x1_next,y1_next, x2_next, y2_next)
# print("x2",x2)
# print("y2",x1_next)