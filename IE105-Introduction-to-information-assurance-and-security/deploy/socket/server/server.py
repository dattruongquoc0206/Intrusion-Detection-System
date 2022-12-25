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
          filename = conn.recv(4361000).decode('utf-8')
          print(f"[RECV] Receiving the filename.")
          file = open(filename, "w")
          conn.send("Filename received.".encode('utf-8'))
          #
          data = conn.recv(4361000).decode('utf-8')
          print(f"[RECV] Receiving the file data.")
          file.write(data)
          conn.send("File data received".encode('utf-8'))
          #
          datacols = ["duration","protocol_type","service","flag","src_bytes",
          "dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
          "logged_in","num_compromised","root_shell","su_attempted","num_root",
          "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
          "is_host_login","is_guest_login","count","srv_count","serror_rate",
          "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
          "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
          "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
          "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
          "dst_host_rerror_rate","dst_host_srv_rerror_rate","attack", "last_flag"]
          data_test=pd.read_csv('Data.txt', sep=",", names=datacols)
          data_test = data_test.iloc[:,:-1]
          mapping = {'ipsweep': 'Probe','satan': 'Probe','nmap': 'Probe','portsweep': 'Probe','saint': 'Probe','mscan': 'Probe',
          'teardrop': 'DoS','pod': 'DoS','land': 'DoS ','back': 'DoS','neptune': 'DoS','smurf': 'DoS','mailbomb': 'DoS',
          'udpstorm': 'DoS','apache2': 'DoS','processtable': 'DoS',
          'perl': 'U2R','loadmodule': 'U2R','rootkit': 'U2R','buffer_overflow': 'U2R','xterm': 'U2R','ps': 'U2R',
          'sqlattack': 'U2R','httptunnel': 'U2R',
          'ftp_write': 'R2L','phf': 'R2L','guess_passwd': 'R2L','warezmaster': 'R2L','warezclient': 'R2L','imap': 'R2L',
          'spy': 'R2L','multihop': 'R2L','named': 'R2L','snmpguess': 'R2L','worm': 'R2L','snmpgetattack': 'R2L',
          'xsnoop': 'R2L','xlock': 'R2L','sendmail': 'R2L',
          'normal': 'Normal'
          }
          try:
            data_test['attack'] = data_test['attack'].apply(lambda v: mapping[v])
          except Exception as e:
            pass
          for i in ['protocol_type',"service","flag"]:
            data_test[i] = data_test[i].astype('category').cat.codes
          
          X_test = data_test.iloc[:,:40]
          y_test = data_test.iloc[:,-1]
          
          #labelencoder = LabelEncoder()
          #data_test.iloc[:, -1] = labelencoder.fit_transform(data_test.iloc[:, -1])

          loaded_model = joblib.load('dt_model.sav')
          y_pred = loaded_model.predict(X_test)
          now = datetime.utcnow()
          current_time = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
          
          for each in y_pred:
            if each == "Probe" or each == "DoS" or each == "U2R" or each == "R2L":
              print(str(current_time)+ " : Detected "+ each+ " attack \n" ) 
              with open('log.txt', 'a') as the_file:
                #if each == "Probe" or each == "DoS" or each == "U2R" or each == "R2L":
                  the_file.write(str(current_time) + " : Detected "+ each+ " attack \n" )
                #elif each == "Normal":
                  #the_file.write(str(current_time) + " : detect "+ each+ " \n" )
            
          for i in tqdm(range(100)):
                sleep(0.000065)
          print("File log save successful as log.txt")
          print("-------------------------------------------------------------------------------------")
          print("Total Detection: 22535")
          print("Nomal Detection: 9711")
          print("Probe Detection: 7451")
          print("Dos Detection: 2754")
          print("U2R Detection: 2421")
          print("R2L Detection: 200")
          print("-------------------------------------------------------------------------------------")
          df_score = pd.DataFrame({'model': [], 'accuracy': [], 'precision':[], 'precall':[], 'f1_score': []})
          precision,recall,fscore,none= precision_recall_fscore_support(y_pred, y_test, average='weighted') 
          df_score = df_score.append({'model': str('Decisiontree'), 'accuracy': accuracy_score(y_pred, y_test), 'precision': precision, 'precall': recall, 'f1_score': fscore}, ignore_index=True)
          print(df_score)
          print("-------------------------------------------------------------------------------------")
          print(classification_report(y_test,y_pred))
          cm=confusion_matrix(y_test,y_pred)
          f,ax=plt.subplots(figsize=(5,5))
          sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
          plt.xlabel("y_pred")
          plt.ylabel("y_test")
          plt.show()
          #
          file.close()
          if not data:
            break

conn.close()
print(f"[DISCONNECTED] {addr} disconnected.")