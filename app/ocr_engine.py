import pytesseract
from PIL import Image
import os
from pytesseract import Output


def read_image(image_path: str) -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError("Image not found", image_path)
    
    img = Image.open(image_path)
    # preprocess image convert to grayscale and binarization
    grayscale_v = img.convert("L")
    binarized_v = grayscale_v.point(lambda x: 255 if x > 128 else 0)

    response = pytesseract.image_to_data(image=binarized_v, output_type=Output.DICT)

    # calculate confidence score and build the valid string
    valid_strings = []
    confidence_score = 0

    for i in range(len(response["text"])):
        if response["conf"][i] != -1:
            if response["text"][i] != "":
                valid_strings.append(response["text"][i])
                confidence_score += response["conf"][i]

    average_confidence = confidence_score // len(valid_strings)
    final_string = " ".join(valid_strings)

    return {"OCR Extracted Text": final_string, "Average Confidence": average_confidence}


if __name__ == "__main__":
    print("Starting engine...")