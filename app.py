import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

event = pd.read_csv('athlete_events.csv')
region = pd.read_csv('noc_regions.csv')

summer_df, winter_df = preprocessor.preprocess(event,region)

st.sidebar.header("Olympics Analysis")
st.sidebar.image('https://nextjuggernaut.com/wp-content/uploads/2016/08/o2.jpg')
season = st.sidebar.selectbox("Which Season Olympic data are you looking for?", ("Summer", "Winter"))
user_menu = st.sidebar.radio("Select an option",
                 ('Medal Tally', 'Overall Anylisis', 'Country wise Analysis', 'Athlete wise Analysis'))

# Filtering summer and winter data.
if season == 'Winter':
    data = winter_df
else:
    data = summer_df
# Code of Medal Tally
if user_menu == 'Medal Tally':
    Years, Country = preprocessor.country_year_list(data)
    st.sidebar.header("Medal Tally")
    selected_year = st.sidebar.selectbox("Select Year",Years)
    selected_country =st.sidebar.selectbox("Select Country",Country)
    if selected_country == 'Overall' and selected_year == 'Overall':
        st.title("Overall Tally")
    if selected_country != 'Overall' and selected_year == 'Overall':
        st.title((selected_country + 'Medal Tally'))
    if selected_country == 'Overall' and selected_year!= 'Overall':
        st.title(('Medal Tally in ') + str(selected_year))
    if selected_country != 'Overall' and selected_year != 'Overall':
        st.title((selected_country + ' Performance in' + str(selected_year)+ " Olympics"))
    medal_tally = helper.fetch_medal_tally(data,selected_year,selected_country)
    st.table(medal_tally)
# Code of Overall Anylisis
if user_menu == 'Overall Anylisis':
    edition = data['Year'].unique().shape[0] - 1
    cities = data['City'].unique().shape[0]
    sports = data['Sport'].unique().shape[0]
    event = data['Event'].unique().shape[0]
    athletes = data['Name'].unique().shape[0]
    nations = data['region'].unique().shape[0]
    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(edition)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Event")
        st.title(event)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)

    nations_over_time = helper.participation_nation_over_time(data,'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title("Participating Nations over the Year")
    st.plotly_chart(fig)

    event_over_time = helper.participation_nation_over_time(data,'Event')
    fig = px.line(event_over_time, x='Edition', y='Event')
    st.title("Events over the Year")
    st.plotly_chart(fig)

    athlete_over_time = helper.participation_nation_over_time(data, 'Name')
    fig = px.line(athlete_over_time, x='Edition', y='Name')
    st.title("Athlete over the Year")
    st.plotly_chart(fig)

    st.title("No of Event over time(Sport)")
    fig, ax, = plt.subplots(figsize = (20,20))
    x = data.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)

    st.title('Most successful Athletes')
    sport_list = data['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Overall")
    selected_sport = st.selectbox("Select a Sport", sport_list)
    x = helper.most_wom(data,selected_sport)
    st.table(x)

# Code of Country wise Analysis
if user_menu == 'Country wise Analysis':
    # Medals Tally Over the Years
    country_list = data['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select Country",country_list)
    country_data = helper.yearwise_medal_tally(data,selected_country)
    fig2 = px.line(country_data, x='Year', y='Medal')
    st.title(selected_country + " Medals Tally Over the Years")
    st.plotly_chart(fig2)

    # Top 10 Athelets of
    st.title(selected_country + " excels in the following Sports")
    pt = helper.country_event_heatmap(data,selected_country)
    fig, ax, = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)
    st.title("Top 10 Athelets of " + selected_country)
    top10_df = helper.most_successful_player_countrywise(data,selected_country)
    st.table(top10_df)

# Code of Athlete wise Analysis
if user_menu == 'Athlete wise Analysis':
    # Distribution Of Age
    athlete_data = data.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_data['Age'].dropna()
    x2 = athlete_data[athlete_data['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_data[athlete_data['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_data[athlete_data['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medal', 'Silver Medal', 'Bronze Medal'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width = 1000,height = 600)
    st.title('Distribution Of Age')
    st.plotly_chart(fig)

    # # Distribution of Age wrt Sports(Gold Medalist)
    # x = []
    # name = []
    # famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
    #                  'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
    #                  'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
    #                  'Water Polo', 'Hockey', 'Rowing', 'Fencing',
    #                  'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
    #                  'Tennis', 'Golf', 'Softball', 'Archery',
    #                  'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
    #                  'Rhythmic Gymnastics', 'Rugby Sevens',
    #                  'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    # for sport in famous_sports:
    #     temp_df = athlete_data[athlete_data['Sport'] == sport]
    #     x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
    #     name.append(sport)
    # fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    # fig.update_layout(autosize=False, width=1000, height=600)
    # st.title("Distribution of Age wrt Sports(Gold Medalist)")
    # st.plotly_chart(fig)

    # Height Vs Weight
    st.title('Height Vs Weight')
    sport_list = data['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    selected_sport = st.selectbox("Select a Sport", sport_list)
    temp_df = helper.weight_hight(data,selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=100)
    st.pyplot(fig)

    # Men Vs Women Participation Over the Years
    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(data)
    fig = px.line(final, x='Year', y=['Men', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
