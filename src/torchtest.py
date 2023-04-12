import torch
import sys
import numpy

print("Python Version:", sys.version)
print("Torch Version:", torch.__version__)
print("Numpy Version:", numpy.__version__)

# Should create a random 5 x 3 matrix
x = torch.rand(5, 3)
print(x)

print("CUDA version:", torch.version.cuda)

# Should print 'True'
print("CUDA is available:", torch.cuda.is_available())

# Should print AT LEAST 'sm_86'
print("Architectures available:", torch.cuda.get_arch_list())
