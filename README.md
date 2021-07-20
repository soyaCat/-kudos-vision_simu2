# -kudos-vision_simulator

쿠도스 쿠봇 비전 시뮬레이터 입니다.

---
# 현재 의존 패키지 버전

- unity용 ml_agent: 1.9.0
- 파이썬용 ml_agent: 0.25.0
- cuda 10.0
- tensorflow 1.15.0
- unity버전 20.4.22f

---

# 내부 파일들 설명
- build, Linux_build
  >시뮬레이션 실행 파일이 들어가 있습니다.

- CustomFunctionFor_mlAgent.py
  >ml_agent 제어에 사용되는 함수들을 모아둔 코드파일입니다.
  
- get_data_from_ENV.py
  >시뮬레이터를 데이터 받아오기 모드로 작동시킵니다.
  >내부 파라미터를 조절하여 딥러닝 학습에 필요한 학습 데이터들을 시뮬레이터로부터 받아올 수 있습니다.

- made_data_from_avi.py
  >현실 영상 프레임으로부터 딥러닝 학습에 필요한 데이터를 얻을 수 있습니다.  
  >프레임단위의 사진과 총 데이터 개수 정보가 담긴(yolo학습에 필요) 데이터만을 주기 때문에 데이터 후처리가 요구될 수도 있습니다.  
