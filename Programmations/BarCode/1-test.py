import cv2


"""
https://note.nkmk.me/en/python-opencv-barcode/
https://docs.opencv.org/4.x/d6/d25/tutorial_barcode_detect_and_decode.html
"""
img = cv2.imread('Programmations/BarCode/barcode.jpg')
img = cv2.imread('Programmations/BarCode/wikipedia.png')
img = cv2.imread('Programmations/BarCode/Triton.png')
img = cv2.imread('Programmations/BarCode/EAN8.jpg')
img = cv2.imread('Programmations/BarCode/EAN13.jpg')
img = cv2.imread('Programmations/BarCode/UPCA.jpg')
img = cv2.imread('Programmations/BarCode/UPCE.jpg')


bd = cv2.barcode.BarcodeDetector()
bardet = cv2.barcode_BarcodeDetector()

res = bd.detectAndDecode(img)
print(res)
res = bardet.detectAndDecode(img)
print(res)

cv2.imshow('img', img)
cv2.waitKey(0)


"""
print(retval, decoded_info, decoded_type, points)

img = cv2.polylines(img, points.astype(int), True, (0, 255, 0), 3)

for s, p in zip(decoded_info, points):
    img = cv2.putText(img, s, p[1].astype(int),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

cv2.imwrite('data/dst/barcode_opencv.jpg', img)
"""