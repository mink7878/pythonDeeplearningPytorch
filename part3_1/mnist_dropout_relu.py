# -*- coding: utf-8 -*-
"""mnist_dropout_relu.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WNVvZ5sEXO733WYDuxVKJcWcsLR77GSz
"""

# 1. Module Import
import numpy as np
import matplotlib.pyplot as plt
import torch # 파이토치 기본 모듈
import torch.nn as nn # 딥러닝 모델 설계할 때 필요한 함수 모음
import torch.nn.functional as F # 자주 이용되는 함수들
from torchvision import transforms, datasets

# 2. 딥러닝 모델 설계할 때 활용하는 장비 확인
if torch.cuda.is_available():
  DEVICE = torch.device('cuda')
else:
  DEVICE = torch.device('cpu')

print('Using PyTorch version : ', torch.__version__, 'Device : ', DEVICE)

BATCH_SIZE = 32
EPOCHS = 30

# 3. MNIST 데이터 다운로드
train_dataset = datasets.MNIST(root='../data/MNIST',
                               train = True,
                               download = True,
                               transform = transforms.ToTensor()) # 이미지 전처리
test_dataset = datasets.MNIST(root='../data/MNIST',
                              train = False,
                              transform = transforms.ToTensor())
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                           batch_size = BATCH_SIZE,
                                           shuffle = True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                          batch_size = BATCH_SIZE,
                                          shuffle = False)

# 4. 데이터 확인 (1)
for (X_train, y_train) in train_loader:
  print('X_train : ', X_train.size(), 'type : ', X_train.type())
  print('X_train : ', y_train.size(), 'type : ', y_train.type())
  break

# 5. 데이터 확인 (2)
pltsize = 1
plt.figure(figsize=(10 * pltsize, pltsize))
for i in range(10):
  plt.subplot(1, 10, i+1)
  plt.axis('off')
  plt.imshow(X_train[i, :, :, :].numpy().reshape(28, 28), cmap='gray_r')
  plt.title('class : ' + str(y_train[i].item()))

# 6. MLP 모델 설계
class Net(nn.Module):
  def __init__(self):
    super(Net, self).__init__()
    self.fc1 = nn.Linear(28*28*1, 512)
    self.fc2 = nn.Linear(512, 256)
    self.fc3 = nn.Linear(256, 10)
    self.dropout_prob = 0.5 # 50%의 노드에 대해 가중값을 계산하지 않겠다.

  def forward(self, x):
    x = x.view(-1, 28*28*1) # flatten
    x = self.fc1(x)
    x = F.relu(x)
    x = F.dropout(x, training=self.training, p=self.dropout_prob) # self.training = 학습 상태이면 T / 검증 상태이면 F
    x = self.fc2(x)
    x = F.relu(x)
    x = F.dropout(x, training=self.training, p=self.dropout_prob) 
    x = self.fc3(x)
    x = F.log_softmax(x, dim=1)
    return x

# 7. Optimizer, Objective Function 설정
model = Net().to(DEVICE)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.5)
criterion = nn.CrossEntropyLoss()

print(model)

# 8. MLP 모델 학습을 진행하며 학습 데이터에 대한 모델 성능을 확인하는 함수 정의
def train(model, train_loader, optimizer, log_interval):
  model.train()
  for batch_idx, (image, label) in enumerate(train_loader):
    image = image.to(DEVICE)
    label = label.to(DEVICE)
    optimizer.zero_grad() # backward 메서드로 계산된 이전 gradient값 삭제
    output = model(image) # 장비에 할당한 이미지 데이터 input으로 넣기
    loss = criterion(output, label) # 기존에 정의한 CE 이용해 loss 계산
    loss.backward() # 계산한 loss 바탕으로 gradient값을 각 파라미터에 할당
    optimizer.step() # 할당된 gradient값 이용해 파라미터값 업데이트

# 9. 학습되는 과정 속에서 검증 데이터에 대한 모델 성능 확인하는 함수 정의
def evaluate(model, test_loader):
  model.eval()
  test_loss = 0
  correct = 0

 # 학습이 모두 끝나고 학습한 결과를 실행에 옮기는 inference 단계에서는 굳이 학습 모드로 사용할 필요가 없음.
 # gradient를 업데이트 하지 않고, dropout, batchnorm 등이 적용 x
  with torch.no_grad(): # 평가단계에서는 gradient 통해 파라미터값이 업데이트되는 현상을 막기 위해 흐름 억제
    for image, label in test_loader:
      image = image.to(DEVICE)
      label = label.to(DEVICE)
      output = model(image)
      test_loss += criterion(output, label).item()
      prediction = output.max(1, keepdim=True)[1]
      correct += prediction.eq(label.view_as(prediction)).sum().item()

  test_loss /= len(test_loader.dataset)
  test_accuracy = 100. * correct / len(test_loader.dataset)
  return test_loss, test_accuracy

# 10. MLP 학습을 실행하면서 train, test set의 loss 및 test set acc 확인
for Epoch in range(1, EPOCHS+1):
  train(model, train_loader, optimizer, log_interval=200)
  test_loss, test_accuracy = evaluate(model, test_loader)
  print('\n[EPOCH : {}], \tTest Loss : {:.4f}, \tTest Accuracy : {:.2f} %\n'.format(Epoch, test_loss, test_accuracy))