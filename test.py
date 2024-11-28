import torch
print(torch.cuda.is_available())  # 如果返回 False，说明当前环境不支持 GPU
print(torch.version.cuda)