from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji as e

def fetch_stats(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    #1 . fetch no of messages
    num_messages = df.shape[0]

    #2. fetch no of media messages
    num_media = df[df['message'].str.strip() == '<Media omitted>'].shape[0]

    #3. fetch no of links shared
    num_links = df['message'].apply(lambda x: URLExtract().find_urls(x)).apply(len).sum()

    #4. fetch total words
    num_words = df['message'].apply(lambda x: len(x.split())).sum()

    #5. fetch total characters
    num_chars = df['message'].apply(len).sum()

    return num_messages,num_media,num_links,num_words,num_chars


def most_busy_user(df):
    
    temp = df[df['user']!= 'group_notification'] 
    temp = temp[temp['message'] != '<Media omitted>\n'] 

    x =temp['user'].value_counts().head()
    temp = round((temp['user'].value_counts()/temp.shape[0])*100,2).reset_index().rename(columns={'user':'user','count':'percent'})
    return x,temp


def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user']!= 'group_notification'] 
    temp = temp[temp['message'] != '<Media omitted>\n'] 

    text = ' '.join(temp['message'])
    wc = WordCloud(width=800,height=400).generate(text)
    return wc 


def most_common_words(selected_user,df): 
    f = open('stop_hinglish.txt','r') 
    stopwords = f.read().split('\n') 
    if selected_user != 'Overall': 
        df = df[df['user'] == selected_user] 
    temp = df[df['user']!= 'group_notification'] 
    temp = temp[temp['message'] != '<Media omitted>\n'] 
    words=[] 
    for i in temp['message']: 
        for word in i.lower().split(): 
            if word not in stopwords: 
                words.append(word) 
        
    most_common_df = pd.DataFrame(Counter(words).most_common(20)) 
    return most_common_df


# def emoji_helper(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#     emojis = []
#     for i in df['message']:
#         emojis.extend([c for c in i if c in e.UNICODE_EMOJI['en']])

#     emojis_df =pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))).rename(columns={0:'emoji',1:'count'})
    
#     return emojis_df

def emoji_helper(selected_user, df):
    # Filter the DataFrame if a specific user is selected
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Check if the DataFrame is empty after filtering
    if df.empty:
        print("No data found for the selected user.")
        return pd.DataFrame(columns=['emoji', 'count'])

    # List to hold extracted emojis
    emojis = []

    # Loop through the 'message' column and extract emojis
    for message in df['message']:
        emojis.extend([c for c in message if c in e.UNICODE_EMOJI['en']])

    # Count the occurrences of each emoji
    emoji_counts = Counter(emojis)

    # Convert to DataFrame
    emojis_df = pd.DataFrame(emoji_counts.items(), columns=['emoji', 'count'])

    # Debugging: Check columns of the DataFrame
    print("Columns of emoji_df:", emojis_df.columns)

    # Ensure the 'count' column exists and is numeric
    if 'count' in emojis_df.columns:
        emojis_df['count'] = pd.to_numeric(emojis_df['count'], errors='coerce')
    else:
        print("The 'count' column is missing. Adding a default 'count' column.")
        emojis_df['count'] = 0  # Or handle accordingly if 'count' is missing

    return emojis_df


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year','month_num','month'])['message'].count().reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daywise_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_of_week'].value_counts()

def monthly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    user_heatmap = df.pivot_table(index='day_of_week',columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap