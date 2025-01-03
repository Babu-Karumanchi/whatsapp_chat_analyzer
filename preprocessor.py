import  re
import pandas as pd

def preprocess(data):
    pattern =r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    msg = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)

    df = pd.DataFrame({'user_messages':msg,'msgDate':dates})
    df['msgDate'] = pd.to_datetime(df['msgDate'], format="%m/%d/%y, %H:%M - ")
    df.rename(columns={'msgDate': 'date'},inplace=True)

    users = []
    msgs = []
    for msg in df['user_messages']:
        entry = re.split(r'(?<=\w):\s', msg)  
        if len(entry) > 1: 
            users.append(entry[0]) 
            msgs.append(entry[1])   
        else:
            users.append('group_notification')
            msgs.append(entry[0])   

    df['user'] = users
    df['message'] = msgs
    df.drop(columns=['user_messages'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year']=df['date'].dt.year
    df['month_num']=df['date'].dt.month
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['day_of_week']=df['date'].dt.day_name()
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    period= []
    for hour in df[['day_of_week','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+'-'+str(0))
        elif hour ==0:
            period.append(str('00')+'-'+str(hour+1))
        else:
            period.append(str(hour)+'-'+str(hour+1))

    df['period'] = period

    return df
