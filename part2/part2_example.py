# -*- coding: utf-8 -*-
"""part2_example.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Pe1DBbKsp31l2q8AF1hfgmLGjGyJn2J6
"""

# 1. module import
import numpy as np
import matplotlib.pyplot as plt
import torch # pytorch의 기본 모듈
import torch.nn as nn # pytorch 모듈 중 딥러닝, 즉 인공신경망 모델을 설계할 때 필요한 함수 모아 놓은 모듈
import torch.nn.functional as F # torch.nn 모듈 중에서도 자주 이용되는 함수를 F로 지정
from torchvision import transforms, datasets # 컴퓨터비전 연구 분야에서 자주 이용하는 torchvision 모듈 내 transforms, datasets 함수

# 2. 딥러닝 모델 설계할 때 활용하는 장비 확인
if torch.cuda.is_available():
  DEVICE = torch.device('cuda') # GPU 사용 가능
else:
  DEVICE = torch.device('cpu')

print('Using PyTorch version : ', torch.__version__, 'Device : ', DEVICE)

BATCH_SIZE = 32 # MLP 모델 학습할 때 필요한 데이터 개수의 단위
EPOCHS = 10 # 미니배치 1개 단위, 존재하고 있는 미니배치를 전부 이용하는 횟수를 의미. 즉, 전체 데이터셋을 10번 반복해 학습

"""- 미니배치 1개 단위에 대해 데이터가 32개로 구성, 1개의 미니배치로 학습 1회 진행
- 1개의 미니배치를 이용해 학습하는 횟수 = Iteration
- 전체 데이터를 이용해 학습을 진행한 횟수 = Epoch
- (ex) 전체 데이터가 1만 개이고 1000개 데이터를 이용해 1개 미니배치를 구성한다면 1Epoch 당 10회의 Iteration이 발생한다.
- 참고  
: https://m.blog.naver.com/qbxlvnf11/221449297033
"""

# 3. MNIST 데이터 다운로드 (train set, test set 분리하기)
train_dataset = datasets.MNIST(root='../data/MNIST',
                               train = True,
                               download = True,
                               transform = transforms.ToTensor())
test_dataset = datasets.MNIST(root='../data/MNIST',
                              train = False,
                              transform = transforms.ToTensor())
# 다운로드한 MNIST 데이터셋을 미니배치 단위로 분리해 지정
# 이미지 데이터를 BATCH_SIZE만큼, 즉 32개만큼 묶어 1개의 미니배치를 구성하는 것을 DataLoader 함수를 이용해 진행할 수 있다.
train_loader = torch.utils.data.DataLoader(dataset = train_dataset,
                                           batch_size = BATCH_SIZE,
                                           shuffle = True)
test_loader = torch.utils.data.DataLoader(dataset = test_dataset,
                                           batch_size = BATCH_SIZE,
                                           shuffle = False)

"""- transform  
: 사람의 손글씨 데이터인 MNIST는 이미지 데이터이다. 데이터를 다운로드할 때, 이미지 데이터에 대한 기본적인 전처리를 동시에 진행할 수 있다.  
: 여기서는 torch 모듈로 설계한 MLP의 input으로 이용되기 때문에 ToTensor() 메서드를 이용해 tensor 형태로 변경.  
: 또한, 한 픽셀은 0 ~ 255 범위의 스칼라 값으로 구성돼 있는데, 이를 0 ~ 1 범위에서 정규화 과정이 진행.  
: MLP 모델이 포함된 인공신경망 모델은 input 데이터 값의 크기가 커질수록 불안정하거나 과적합되는 방향으로 학습이 진행될 우려가 있기 때문에 정규화 과정을 이용해 input으로 이용하는 것을 권장
"""

# 4. 데이터 확인하기 ①
for (X_train, y_train) in train_loader:
  print('X_train : ', X_train.size(), 'type : ', X_train.type())
  print('y_train : ', y_train.size(), 'type : ', y_train.type())
  break

"""- X_train  
: 32개의 이미지 데이터가 1개의 미니배치를 구성하고 있고, 가로 28 / 세로 28개의 픽셀로 구성돼 있으며 채널이 1이므로 gray scale로 이뤄진 이미지 데이터라는 것을 알 수 있다.  
: torch.FloatTensor 형태
- y_train  
: 32개의 이미지 데이터 각각에 label 값이 1개씩 존재하기 때문에 32개의 값을 갖고 있다.  
: torch.LongTensor 형태
"""

# 5. 데이터 확인하기 ②
pltsize = 1
plt.figure(figsize=(10 * pltsize, pltsize))
for i in range(10):
  plt.subplot(1, 10, i+1)
  plt.axis('off')
  plt.imshow(X_train[i, :, :, :].numpy().reshape(28,28), cmap='gray_r')
  plt.title('Class : ' + str(y_train[i].item()))

# 6. torch 모듈을 이용해 MLP 모델 설계
class Net(nn.Module): # nn.Module 클래스를 상속받는 Net 클래스 정의 (nn.Module 클래스가 이용할 수 있는 함수를 그대로 이용할 수 있기 때문에 자주 이용)
  def __init__(self): # Net 클래스의 인스턴스를 생성했을 때 지니게 되는 성질을 정의해주는 메서드
    super(Net, self).__init__() # nn.Module 내에 있는 메서드를 상속받아 이용
    self.fc1 = nn.Linear(28*28, 512) # 첫 번째 FC 정의 input : (W*H*C)
    self.fc2 = nn.Linear(512, 256) # 두 번째 FC 정의
    self.fc3 = nn.Linear(256, 10) # 세 번째 FC 정의

  def forward(self, x): # Net 클래스를 이용해 설계한 MLP 모델의 forward propagation 정의 (즉, input → hidden → output 계산 과정)
    x = x.view(-1, 28*28) # view 메서드로 '크기가 28*28인 2차원 데이터'를 '784 크기의 1차원 데이터'로 변환 (Flatten 한다.)
    x = self.fc1(x) # __init__ 메서드를 이용해 정의한 첫 번째 FC에 1차원으로 펼친 이미지 데이터 통과
    x = F.sigmoid(x) # torch.nn 모듈 중에서도 자주 이용되는 함수 F 내에 정의된 비선형 함수인 sigmoid() 이용해 두 번째 FC의 input으로 계산
    x = self.fc2(x) # __init__ 메서드를 이용해 정의한 두 번째 FC에 통과시킴
    x = F.sigmoid(x) 
    x = self.fc3(x)
    x = F.log_softmax(x, dim=1) # 함수 F 내의 log.softmax를 이용해 최종 output 계산
    return x

"""- 출력층에서 일반적 softmax 아닌 log_softmax 사용하는 이유?  
: MLP 모델이 back propagation 알고리즘을 이용해 학습을 진행할 때 loss 값에 대한 gradient를 좀 더 원활하게 계산할 수 있기 때문.  
: log 함수 그래프의 기울기가 부드럽게 변화하는 것을 상상해보면 직관적으로 이해할 수 있다.
"""

# 7. optimizer, objective function 설정
model = Net().to(DEVICE) # 위에서 정의한 MLP 모델을 기존에 선정한 DEVICE에 할당 (DEVICE 장비를 이용해 MLP 모델을 완성하기 위해)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.5) # back propagation을 이용해 파라미터를 업데이트할 때 이용하는 optimizer 정의 # momentum : optimizer의 관성을 나타냄
criterion = nn.CrossEntropyLoss() # MLP 모델의 output값과 원핫인코딩값과의 loss는 CrossEntropy를 이용해 계산하기 위해 설정

print(model)

# 8. MLP 모델 학습을 진행하며 학습 데이터에 대한 모델 성능을 확인하는 함수 정의
def train(model, train_loader, optimizer, log_interval):
  model.train() # 기존에 정의한 MLP 모델을 학습 상태로 지정
  for batch_idx, (image, label) in enumerate(train_loader): # 기존에 정의한 train_loader에는 학습에 이용되는 이미지 데이터와 레이블 데이터가 미니배치 단위로 묶여 저장돼 있음.
    image = image.to(DEVICE) # 미니배치 내에 있는 이미지 데이터를 이용해 MLP 모델을 학습시키기 위해 기존에 정의한 장비에 할당
    label = label.to(DEVICE) # 미니배치 내에 있는 이미지 데이터와 매칭된 레이블 데이터도 기존에 정의한 장비에 할당
    optimizer.zero_grad() 
    # 기존에 정의한 장비에 이미지 데이터, 레이블 데이터를 할당할 경우, 과거에 이용한 미니배치 내에 있는 이미지 데이터, 레이블 데이터를 바탕으로 계산된 loss의 gradient값이 optimizer에 할당 돼 있으므로 optimizer의 gradient 초기화
    output = model(image) # 장비에 할당한 이미지 데이터를 MLP 모델의 input으로 이용해 output 계산
    loss = criterion(output, label) # 계산된 output과 장비에 할당된 레이블 데이터를 기존에 정의한 CrossEntropy를 이용해 loss값 계산
    loss.backward() # loss값을 계산한 결과를 바탕으로 back propagation을 통해 계산된 gradient 값을 각 파라미터에 할당
    optimizer.step() # 각 파라미터에 할당된 gradient 값을 이용해 파라미터 값을 업데이트
    
    if batch_idx % log_interval == 0:
      print('Train Epoch : {} [{}/{}({:.0f}%)]\tTrain Loss : {:.6f}'.format(Epoch, batch_idx*len(image),
                                                                            len(train_loader.dataset), 100*batch_idx / len(train_loader), loss.item()))

# 9. 학습되는 과정 속에서 검증 데이터에 대한 모델 성능을 확인하는 함수 정의
# MLP 모델 학습 과정 또는 학습이 완료된 상태에서 MLP 모델의 성능을 평가하기 위해 evaluate 함수 정의
def evaluate(model, test_loader):
  model.eval() # 학습 과정 또는 학습이 완료된 MLP 모델을 학습 상태가 아닌, 평가 상태로 지정
  test_loss = 0 # 기존에 정의한 test_loader 내의 데이터를 이용해 loss 값을 계산하기 위해 임시로 0으로 설정
  correct = 0 # 학습 과정 또는 학습이 완료된 MLP 모델이 올바른 Class로 분류한 경우를 세기 위해 임시로 0으로 설정

  with torch.no_grad(): # MLP 모델을 평가하는 단계에서는 gradient를 통해 파라미터값이 업데이트되는 현상을 방지하기 위해 'gradient의 흐름을 억제'
    for image, label in test_loader: # 기존에 정의한 test_loader 내의 데이터도 미니배치 단위로 저장돼 있다.
      image = image.to(DEVICE) # 미니배치 내에 있는 이미지 데이터를 이용해 MLP 모델을 검증하기 위해 기존에 정의한 장비에 할당
      label = label.to(DEVICE) # 미니배치 내에 있는 이미지 데이터와 매칭된 레이블 데이터도 기존에 정의한 장비에 할당
      output = model(image) # 장비에 할당한 이미지 데이터를 MLP 모델의 input으로 output을 계산
      test_loss += criterion(output, label).item() # 계산된 output과 장비에 할당된 레이블 데이터를 기존에 정의한 CrossEntropy를 이용해 loss값 계산한 결과값을 test_loss에 더해 업데이트
      prediction = output.max(1, keepdim=True)[1] # MLP 모델의 output 값은 크기가 10인 벡터값이다. 계산된 벡터값 내 가장 큰 값인 위치에 대해 해당 위치에 대응하는 클래스로 예측했다고 판단.
      correct += prediction.eq(label.view_as(prediction)).sum().item() # MLP 모델이 최종으로 예측한 클래스값과 실제 레이블이 의미하는 클래스가 맞으면 correct에 더해 올바르게 예측한 횟수 저장

  test_loss /= len(test_loader.dataset) # 현재까지 계산된 test_loss값을 test_loader 내에 존재하는 미니배치 개수만큼 나눠 평균 loss값으로 계산
  test_accuracy = 100.*correct / len(test_loader.dataset) # test_loader 중 얼마나 맞췄는지를 계산해 정확도 계산
  return test_loss, test_accuracy

# 10. MLP 학습을 실행하면서 train, test set의 loss 및 test set accuracy 확인
for Epoch in range(1, EPOCHS+1):
  train(model, train_loader, optimizer, log_interval=200)
  test_loss, test_accuracy = evaluate(model, test_loader)
  print('\n[EPOCH : {}], \tTest Loss : {:.4f}, \tTest Accuracy: {:.2f} %\n'.format(Epoch, test_loss, test_accuracy))