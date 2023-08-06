# dnn_cool_activations

Simple numpy actions, currently just sigmoid and softmax.


```python
import numpy as np

from dnn_cool_activations.base import sigmoid

sigmoid(np.array([0., -23, 51.]))
# array([0.5, 0. , 1. ])
```