def medal_tally(df):
    medal_tally = df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby(['NOC']).sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')

    return medal_tally


def fetch_medal_tally(data,year, country):
    medal_df = data.drop_duplicates(['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_data = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_data = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_data = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_data = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]

    if flag == 1:
        x = temp_data.groupby(['Year']).sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                        ascending=True).reset_index()
    else:
        x = temp_data.groupby(['region']).sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                          ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Silver'] = x['Silver'].astype('int')
    x['Gold'] = x['Gold'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')

    return x
def participation_nation_over_time(data,column):
    data_over_time = data.drop_duplicates(['Year', column])['Year'].value_counts().reset_index().sort_values('index')
    data_over_time.rename(columns={'index': 'Edition', 'Year': column}, inplace=True)
    return data_over_time

def most_wom(data,sport):
    temp_df = data.dropna(subset = ["Medal"])
    if sport != "Overall":
        temp_df = temp_df[temp_df['Sport']==sport]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(data,left_on = 'index',right_on = 'Name',how = 'left')[['index','Name_x','Sport','region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medels'}, inplace=True)
    return x
def yearwise_medal_tally(data,country):
    data.dropna(subset=['Medal'])
    data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],
                                 inplace=True)
    new_data = data[data['region'] == country]
    final_data = new_data.groupby('Year').count()['Medal'].reset_index()
    return final_data
def country_event_heatmap(data,country):
    data.dropna(subset=['Medal'])
    data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],
                         inplace=True)
    new_data = data[data['region'] == country]
    pt = new_data.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_player_countrywise(data,country):
    temp_df = data.dropna(subset = ["Medal"])
    temp_df = temp_df[temp_df['region']==country]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(data,left_on = 'index',right_on = 'Name',how = 'left')[['index','Name_x','Sport']].drop_duplicates('index')
    x.rename(columns = {'index':'Name','Name_x':'Medels'},inplace = True)
    return x
def weight_hight(data,sport):
    athlete_data = data.drop_duplicates(subset=['Name', 'region'])
    athlete_data['Medal'].fillna('No Medals', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_data[athlete_data['Sport'] == sport]
        return temp_df
    else:
        return athlete_data
def men_vs_women(data):
    athlete_data = data.drop_duplicates(subset=['Name', 'region'])
    men = athlete_data[athlete_data['Sex'] == 'M'].groupby('Year').count()['Sex'].reset_index()
    women = athlete_data[athlete_data['Sex'] == 'F'].groupby('Year').count()['Sex'].reset_index()
    final = men.merge(women, on='Year')
    final.rename(columns={'Sex_x': 'Men', 'Sex_y': 'Female'}, inplace=True)
    final.fillna(0,inplace=True)
    return final