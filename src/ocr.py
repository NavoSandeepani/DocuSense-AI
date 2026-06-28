import cv2
import pytesseract
from PIL import Image

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def preprocess_image(image_path):

    img = cv2.imread(image_path)
    if img.shape[0] > img.shape[1]:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    processed_path = "processed.png"

    cv2.imwrite(processed_path, thresh)

    return processed_path


def extract_text(image_path):

    processed = preprocess_image(image_path)

    image = Image.open(processed)

    text = pytesseract.image_to_string(
        image,
        lang="eng+sin+tam"
    )

    return text