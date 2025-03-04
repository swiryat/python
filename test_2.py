import numpy as np
import pandas as pd
from tensorflow import keras
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Уровень 2 отключает предупреждения.

print("NumPy version:", np.__version__)
print("Pandas version:", pd.__version__)
print("Keras version:", keras.__version__)
