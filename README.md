# pythonDeeplearningPytorch

## week3  
Q1. 사용자 정의 activation function  
https://stackoverflow.com/questions/55765234/pytorch-custom-activation-functions
- custom으로 만드는 경우 numpy 연산을 섞어쓰면 안 됨 (pytorch tensor로 만들고 pytorch 연산 써야 함.)
- torch는 객체 하나하나를 .to(DEVICE)로 올려준다. (numpy는 cpu에서 돌아가는 연산이라 그런 듯)

## week4  
- 93 page #(2) 코드  
: apply 함수는 네트워크 내부의 모든 모듈을 재귀적으로 검색하고 각 모듈에서 함수를 호출함.
- (참고) https://discuss.pytorch.org/t/weight-initilzation/157/21 https://blogofth-lee.tistory.com/264  <br/><br/><br/>
- Auto**Encoder**라는 이름에서 Encoding 기능에 중점을 두었음을 알 수 있다. 단순히 입력을 넣어 출력하는 것이 목적이 아니라, 잘 학습된 Encoder 부분은 **특징 추출기**로 사용이 가능하다.
- 원본으로 복원이 가능한, 독특한 패턴을 지닌 압축된 정보의 덩어리(특징 벡터)를 활용하는 방식은 무궁무진하다. 
- 특징 벡터는 인간이 해석할 수는 없지만, 분명히 입력 데이터에 대한 어떤 법칙을 가진 특징이 추출된다.
- 학습된 Encoder 부분(특징 추출) + Fully connected Model(분류) =>  정답 레이블을 넣어 transfer learning
- (참고) https://wiserloner.tistory.com/1129 
- 참고로 규제 오토인코더 중 자주 쓰이는 SAE, DAE, CAE는 동작하는 중간에 확률적인 과정이 전혀 없어 같은 입력을 주면 항상 같은 출력이 나오는 **결정론적 오토인코더**이다.
- 이런 결정론적 오토인코더의 중간 과정에 확률 과정을 추가하여 확률 모델로 확장할 수 있다. (ex) RBM) -> 생성 모델로 활용 가능
