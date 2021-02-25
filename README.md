# pythonDeeplearningPytorch

week3  

Q1. 사용자 정의 activation function
https://stackoverflow.com/questions/55765234/pytorch-custom-activation-functions
- custom으로 만드는 경우 numpy 연산을 섞어쓰면 안 됨 (pytorch tensor로 만들고 pytorch 연산 써야 함.)
- torch는 객체 하나하나를 .to(DEVICE)로 올려준다. (numpy는 cpu에서 돌아가는 연산이라 그런 듯)
