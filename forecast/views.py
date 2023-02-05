from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,MinMaxScaler,MaxAbsScaler,RobustScaler
from keras.layers import LSTM
from keras.layers import Dense,Dropout
from keras.models import Sequential
import numpy as np

from django.core.mail import send_mail,EmailMessage
from django.conf import settings
# Create your views here.
def home(request):
    return render(request,'home.html')


def send_email_to_user(email):
    email_from=settings.EMAIL_HOST
    subject='12 weeks forecast'
    message='this mail contains the csv file of the forecast of your store'
    email_message=EmailMessage(subject,message,email_from,[email])
    email_message.attach_file('media/file1.csv')
    email_message.send()




def add(request):
    email=request.POST['email']
    data2=request.FILES['file']
    user=request.POST['user']
    print(data2)
    user=user.upper()
       
    df =pd.read_csv(data2)
    df['Date']=pd.to_datetime(df['Date'],infer_datetime_format=True)
    train_dates=df['Date']
    cols=list(df)[1:7]
    df=df[cols].astype(float)
    scaler=StandardScaler()
    scaler=scaler.fit(df)
    df_for_train=scaler.transform(df)
    trainX=[]
    trainY=[]
    n_future=1
    n_past=14
    for i in range(n_past,len(df_for_train)-n_future+1):
        trainX.append(df_for_train[i-n_past:i,0:df.shape[1]])
        trainY.append(df_for_train[i+n_future-1:i+n_future,0])
    model=Sequential()
    trainX=np.asarray(trainX)
    trainY=np.asarray(trainY)
    model.add(LSTM(64,activation='relu',input_shape=(trainX.shape[1],trainX.shape[2]),return_sequences=True))
    model.add(LSTM(32,activation='relu',return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(trainY.shape[1]))
    model.compile(optimizer='adam',loss='mse')
    n_fut=12
    forecast_period_dates=pd.date_range(list(train_dates)[-1],periods=n_fut,freq='7d').tolist()
    forecast=model.predict(trainX[-n_fut:])
    fore=np.repeat(forecast,df.shape[1],axis=-1)
    y_pred=scaler.inverse_transform(fore)[:,0]
    forecast_dates=[]
    for time_i in  forecast_period_dates:
        forecast_dates.append(time_i.date())
    df_forecast=pd.DataFrame({'Date':np.array(forecast_dates),'sales_in_thousands':y_pred})   
    df_forecast.to_csv('media/file1.csv')
    send_email_to_user(email)






    return render(  request,'result.html',{'email':email,'user':user})    