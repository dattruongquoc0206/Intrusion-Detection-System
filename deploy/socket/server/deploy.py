import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

X_test="0,1,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,229,10,0.00,0.00,1.00,1.00,0.04,0.06,0.00,255,10,0.04,0.06,0.00,0.00,0.00,0.00,1.00"
X_test=X_test.split(",")
X_test=np.array(X_test)

print(len(X_test))
print(X_test[0:41])
#labelencoder = LabelEncoder()
#X_test[0] = labelencoder.fit_transform(X_test[0])
#X_test=X_test.split(",")
#for i in [X_test[1],X_test[2],X_test[3]]:
            #X_test[i] = X_test[i].astype('category').cat.codes
#print(X_test[1:4])
loaded_model = joblib.load('dt_model.sav')
y_pred = loaded_model.predict(X_test.reshape(1, -1))
print(y_pred)

#print(y_pred)