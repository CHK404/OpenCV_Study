#OpenCV 라이브러리 불러오기(네임스페이스처럼)
import cv2

#현재 작업 폴더에 있는 이미지를 읽어와 img변수에 저장
#이미지가 numpy.ndarray 형태로 저장
img = cv2.imread('500px-Lenna.png')

#이미지 파일이 없을 경우 경고 메세지 출력 후 프로그램 종료
if img is None:
    print('이미지를 찾을 수 없습니다. 파일이 있는지 확인해주세요.')
    exit()
    
drawing = False #마우스 왼쪽 버튼이 눌린 상태인지 확인하기 위한 불리언 변수 선언
ix, iy = -1, -1 #마우스 클릭 시작점의 x, y 좌표를 저장하는 변수(초기값 설정)

#마우스 클릭 했을 때 / 움직일 때 이벤트 발생할 때마다 호출
def draw_line(event, x, y, flags, param):
    global ix, iy, drawing #global 키워드는 함수 안에서 전역변수 ix, iy, drawing 사용하겠다는 뜻
    
    #마우스 왼쪽 버튼을 눌렀을 때 (EVENT_LBUTTONDOWN)
    #drawing 상태를 True로 바꿔서 그리기 시작을 표시
    #현재 마우스 위치 (x, y)를 시작점 좌표로 저장
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        
    #마우스를 움직일 때(EVENT_MOUSEMOVE)
    #만약 drawing 상태가 True(왼쪽 버튼이 눌린 상태)면
    #이전 좌표(ix, iy)부터 현재 마우스 좌표 (x, y)까지 검은색(RGB값) 선 두께 2로 그림
    #시작점을 현재 위치(x, y)로 업데이트해서 연속된 선을 그릴 수 있도록 함
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(img, (ix, iy), (x, y), (0, 0, 0), thickness=2)
            ix, iy = x, y
            
    #마우스가 왼쪽 버튼을 뗐을 때(EVENT_LBUTTONUP)
    #그리기 상태 종료(False)로 바꾸고
    #마지막 선을 이전 점부터 현재 점까지 그려서 그리기를 마무리
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(img, (ix, iy), (x, y), (0, 0, 0), thickness=2)
        
#Image라는 이름으로 OpenCV 창(Window)을 생성
#창 이름은 이후 마우스 콜백 함수 등록과 이미지 출력에서 사용
cv2.namedWindow('Image')

#Image창에 마우스 이벤트가 발생할 때 마다 draw_line 함수를 호출하도록 등록
#이 함수가 마우스 클릭, 이동, 뗌 모두 처리
cv2.setMouseCallback('Image', draw_line)

#무한 루프를 돌면서 매 프레임마다 Image창에 이미지를 출력
#이 부분에서 사용자가 그린 선이 실시간으로 반영
while True:
    cv2.imshow('Image', img)
    
    #Image창이 닫혔는지 체크
    #창이 닫히면 cv2.getWindowProperty가 0 이하를 반환, 루프를 종료
    if cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) < 1:
        break
    
    #키보드 입력을 1밀리초 대기하면서 확인
    #ESC 키(ASCII 27)를 누르면 루프를 종료
    #& 0xFF는 64비트 시스템에서도 하위 8비트만 확인하기 위한 일반적인 코드
    if cv2.waitKey(1) & 0xFF == 27:
        break
    #key = cv2.WaitKey(1)
    #if key == 27:
        #break - 위와 동일한 함수 (key 값을 직접 찍어오는 느낌)

#열린 모든 OpenCV 창을 닫고 프로그램 종료    
cv2.destroyAllWindows()