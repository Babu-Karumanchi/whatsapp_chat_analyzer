import streamlit as st
import whatsapp_chat_analyzer.preprocessor as p
import whatsapp_chat_analyzer.helper as h
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data= bytes_data.decode('utf-8')
    df = p.preprocess(data)

    # st.dataframe(df)

    # dropdown for user selection
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox('Show analysis', user_list)

    if st.sidebar.button('Show analysis'):

        num_messages,num_media,num_links,num_words,num_chars = h.fetch_stats(selected_user,df)

        st.title('Top Statistics')

        col1,col2,col3,col4,col5 = st.columns(5)

        with col1:
            st.subheader('Total Messages')
            st.title(num_messages)
        
        with col2:
            st.subheader('Total Media')
            st.title(num_media)
        
        with col3:
            st.subheader('Total Links')
            st.title(num_links)
        
        with col4:
            st.subheader('Total Words')
            st.title(num_words)
        
        with col5:
            st.subheader('Total Characters')
            st.title(num_chars)


        #Monthly TimeLine

        st.title('Monthly Timeline')
        timeline = h.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='r')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daywise Timeline
        st.title('Daily Timeline')
        daywise = h.daywise_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daywise['only_date'],daywise['message'],color='g')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.subheader('Most Active Day')
            most_active_day = h.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(most_active_day.index,most_active_day.values,color='b')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.subheader('Most Active Month')
            most_active_month = h.monthly_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(most_active_month.index,most_active_month.values,color='g')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #Activity Heatmap
        st.title('Activity Heatmap')
        user_heatmap = h.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap,cmap='coolwarm',fmt='g')
        st.pyplot(fig)



        # finding the busiest users in the group (group level)

        if selected_user == 'Overall':

            x,new_df = h.most_busy_user(df)
            fig, ax = plt.subplots()
            col1,col2 = st.columns(2)

            with col1:
                with st.container():
                    st.subheader('Busiest User')
                    ax.bar(x.index,x.values,color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
            
            with col2:
                with st.container():
                    st.subheader('Message Distribution')
                    # st.dataframe(new_df)
                    st.table(new_df.head(15).reset_index(drop=True))

        # Wordcloud

        wc = h.create_wordcloud(selected_user,df)
        st.title('WordCloud')
        st.image(wc.to_array(),use_container_width=True)


        # Most common words

        most_common_df = h.most_common_words(selected_user,df)
        st.title('Most Common Words')
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1],color='green')
        st.pyplot(fig)



        #Emoji Helper
        st.title('Emoji Analysis')
        emoji_df = h.emoji_helper(selected_user,df)
        col1,col2  = st.columns(2)

        with col1:
            st.subheader('Most used emojis')
            st.table(emoji_df.head(20).reset_index(drop=True))

        with col2:
            st.subheader('Emoji Distribution')
            fig, ax = plt.subplots()
            emoji_df['count'] = pd.to_numeric(emoji_df['count'], errors='coerce')

            emoji_df = emoji_df.dropna(subset=['count'])
            ax.pie(emoji_df['count'].head(),labels= emoji_df['emoji'].head(),autopct='%0.2f')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


else:
    with st.container():
        st.title('Upload a file to start analysis')
        st.image('whatsapp.png',width=1000)
