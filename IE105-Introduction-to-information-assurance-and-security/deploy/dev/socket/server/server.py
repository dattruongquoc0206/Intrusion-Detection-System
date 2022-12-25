import socket
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from datetime import datetime
from tqdm import tqdm
from time import sleep
import xgboost as xgb
import warnings
warnings.filterwarnings("ignore")
from functions import *
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,precision_recall_fscore_support, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
      print(f"Connected by {addr}")
      while True:
        data = conn.recv(100).decode('utf-8')
        print(f"[RECV] Receiving the data.")
        print(data)
        if not data:
          break
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
          continue
        else:
          break

conn.close()
print(f"[DISCONNECTED] {addr} disconnected.")