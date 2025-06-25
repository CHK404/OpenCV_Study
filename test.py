import cv2

img = cv2.imread('500px-Lenna.png')

if img is None:
    print('이미지를 찾을 수 없습니다. 파일이 있는지 확인해주세요.')
    exit()
    
