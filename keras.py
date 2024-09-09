import keras_ocr
import matplotlib.pyplot as plt
import cv2

# Load Keras OCR detector and recognizer
pipeline = keras_ocr.pipeline.Pipeline()

def extract_text_from_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    # Use Keras OCR to detect and recognize text
    prediction_groups = pipeline.recognize([image_rgb])
    # Extract text from predictions
    texts = [text for text, box in prediction_groups[0]]
    return texts

# Example usage
image_path = 'D:/demoimage/image1.jpg'  # Replace with your image path
extracted_text = extract_text_from_image(image_path)

# Print the extracted text
print("Extracted Text:")
for text in extracted_text:
    print(text)
