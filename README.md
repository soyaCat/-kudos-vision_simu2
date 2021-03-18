# -kudos-vision_simulator

쿠도스 쿠봇 비전 시뮬레이터 입니다.

---
# 현재 의존 패키지 버전

- unity용 ml_agent: 1.9.0
- 파이썬용 ml_agent: 0.23.0
- cuda 10.0
- tensorflow 1.15.0
- unity버전 20.4.22f

---

# 내부 파일들 설명
- build, Linux_build
  >시뮬레이션 실행 파일이 들어가 있습니다.

- vision_ex
  >시뮬레이션 빌드를 위한 유니티 파일들이 들어있습니다.

- CustomFunctionFor_mlAgent.py
  >ml_agent 제어에 사용되는 함수들을 모아둔 코드파일입니다.

- zmqnumpy.py
  >행렬 통신을 위한 함수들을 모아둔 코드 파일입니다.
 
- get_data_from_ENV.py
  >시뮬레이터를 데이터 받아오기 모드로 작동시킵니다.
  >내부 파라미터를 조절하여 딥러닝 학습에 필요한 학습 데이터들을 시뮬레이터로부터 받아올 수 있습니다.

- play_game_ENV.py
  >시뮬레이터를 테스트 모드로 작동시킵니다.
  >zeorMQ에 기반한 tcp/ip 통신으로 이 코드에 연결하여 만든 코드를 시뮬레이터 상에서 작동시켜볼 수 있습니다.
  >kudos_vision.py를 보면 어떻게 연결했는지 확인할 수 있습니다.
