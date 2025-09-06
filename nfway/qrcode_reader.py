import cv2
from pathlib import Path


def read_qrcode(image_path: Path) -> str | None:
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    return data if data else None
