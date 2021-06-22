import numpy as np
import pandas as pd
from glob2 import iglob
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

"""stats = pd.read_csv(r"C:\Users\AcerMX\Documents\Escuela\S7\Big data redes sociales\Unidad 3\Hololive Insights\chat_stats.csv")
sc_stats = pd.read_csv(r"C:\Users\AcerMX\Documents\Escuela\S7\Big data redes sociales\Unidad 3\Hololive Insights\superchat_stats.csv")
channels = pd.read_csv(r"C:\Users\AcerMX\Documents\Escuela\S7\Big data redes sociales\Unidad 3\Hololive Insights\channels.csv")

# select only active Hololive-affiliated channels
channels = channels[(channels['affiliation'] == 'Hololive') &
                    (channels['group'] != 'INACTIVE')]
channels['group'].fillna('No Group', inplace=True)

# exclude official/secondary channels
officialChannels = [
    'UCJFZiqLMntJufDCHc6bQixg',
    'UCfrWoRGlawPQDQxxeIDRP0Q',
    'UCotXwY6s8pWmuWd_snKYjhg',
    'UCWsfcksUUpoEvhia0_ut0bA',
]
subChannels = [
    'UCHj_mh57PVMXhAUDphUQDFA',
    'UCLbtM3JZfRTg8v2KGag-RMw',
    'UCp3tgHXw_HI0QMk1K8qh3gQ',
]
channels = channels[~channels['channelId'].isin(officialChannels + subChannels)]

# merge stats columns
stats_all = pd.merge(stats, sc_stats, on=['channelId', 'period'], how='left')
numeric_columns = stats_all.select_dtypes(include=['number']).columns
stats_all[numeric_columns] = stats_all[numeric_columns].fillna(0).astype(
        'int')

channels = pd.merge(channels, stats_all, on=['channelId'], how='left')

# sex
channels['sex'] = channels['group'].apply(lambda g: 'Male' if g.startswith('Holostars') else 'Female')

# language
def langmatch(g):
    if g.startswith('English'):
        return 'English'
    elif g.startswith('Indonesia'):
        return 'Indonesian'
    return 'Japanese'
channels['language'] = channels['group'].apply(langmatch)

# aggregate data
overall = channels.groupby('name.en').agg({
    'subscriptionCount': 'first',
    'videoCount': 'first',
    'chatCount': 'sum',
    'chatNunique': 'mean',
    'banCount': 'sum',
    'banNunique': 'mean',
    'deletionCount': 'sum',
    'scCount': 'sum',
    'scNunique': 'mean',
    'scTotalJPY': 'sum',
    'scMeanJPY': 'last',
    'affiliation': 'first',
    'group': 'first',
    'name': 'first',
}).reset_index()
overall['chatCountPerUser'] = overall['chatCount'] / overall['chatNunique']

#Canales con mas suscriptores
fig = px.bar(overall.sort_values(by='subscriptionCount', ascending=False),
       x='name.en',
       y='subscriptionCount',
       color='videoCount',
       hover_name='name',
       hover_data=['videoCount', 'group'],
       labels={
           'subscriptionCount': '# of Subscribers',
           'videoCount': '# of Videos',
           'name.en': 'Name',
           'group': 'Group',
       },
       title='Most Subscribed Channels')
#fig.show()

#Canales con mas sucriptores por grupo
fig = px.bar(overall.sort_values(by='subscriptionCount', ascending=False),
       x='name.en',
       y='subscriptionCount',
       color='group',
       hover_name='name',
       hover_data=['videoCount'],
       labels={
           'sub_count': '# of Subscribers',
           'video_count': '# of Videos',
           'name_en': 'Name',
           'group': 'Group',
       },
       title='Most Subscribed Channels per Group')
#fig.show()

fig = px.treemap(overall, path=['group', 'name'], values='subscriptionCount')
#fig.show()

#Canales mas activos respecto a la cantidad de videos
fig = px.bar(overall.sort_values(by='videoCount', ascending=False),
       x='name.en',
       y='videoCount',
       color='subscriptionCount',
       hover_name='name',
       hover_data=['videoCount', 'subscriptionCount', 'group'],
       labels={
           'subscriptionCount': '# of Subscribers',
           'videoCount': '# of Videos',
           'name.en': 'Name',
           'group': 'Group',
       },
       title='Most Active Channels in terms of Number of Videos')
#fig.show()

#Intensidad de los chats en vivo
fig = px.bar(overall.sort_values(by='chatCount', ascending=False),
       x='name.en',
       y='chatCount',
       color='chatCountPerUser',
       hover_name='name',
       labels={
           'chatCountPerUser': 'Average chats per user',
           'videoCount': '# of Videos',
           'name.en': 'Name',
           'chatCount': '# of Chat',
       },
       title='Live Chat Intensity (Whole-period)'
    ).update_layout(xaxis={'categoryorder': 'total descending'})
#fig.show()

#Baneos
fig = px.bar(overall.sort_values(by='banCount', ascending=False),
       x='name.en',
       y='banCount',
       log_y=True,
       color='chatCount',
       hover_name='name',
       hover_data=['chatCount', 'subscriptionCount'],
       labels={
           'chatCount': "# of Chats",
           'subscriptionCount': '# of Subscribers',
           'videoCount': '# of Videos',
           'name.en': 'Name',
           'banCount': '# of Ban',
       },
       title='Ban Events (y-axis is log-scaled)'
    )
#fig.show()

#Correlacion entre el numero de suscriptores y baneos
#Los que estan en la esquina inferior derecha se consideran como menos "trolleados"
fig = px.scatter(overall,
       x='subscriptionCount',
       y='banCount',
       log_y=True,
       color='subscriptionCount',
       trendline='ols',
       hover_name='name',
       hover_data=['videoCount', 'group'],
       labels={
           'subscriptionCount': '# of Subscribers',
           'name.en': 'Name',
           'group': 'Group',
           'banCount': '# of Ban',
       },
       title='Correlation between # of Subscriptions and Ban Events')
#fig.show()

#Correlacion entre numero de suscriptores y chats
#Aquellos arriba de la linea tienen buen rendimiento
fig = px.scatter(overall,
       x='subscriptionCount',
       y='chatCount',
       color='chatCountPerUser',
       trendline='ols',
       hover_name='name',
       hover_data=['videoCount', 'group'],
       labels={
           'subscriptionCount': '# of subscribers',
           'chatCountPerUser': 'avg. # of chats per user',
           'name.en': 'Name',
           'group': 'Group',
           'banCount': '# of ban',
           'chatCount': '# of chats'
       },
       title='Correlation between # of Subscriptions and Chats')
#fig.show()

#Correlacion entre numero de suscriptores y usuarios unicos
#Aquellos arriba de la linea tienen buen rendimiento
fig = px.scatter(overall,
       x='subscriptionCount',
       y='chatNunique',
       color='subscriptionCount',
       trendline='ols',
       hover_name='name',
       hover_data=['group', 'chatNunique'],
       labels={
           'chatNunique': '# of unique users',
           'chatCountPerUser': 'avg. # of chats per user',
           'subscriptionCount': '# of subscribers',
           'name.en': 'Name',
           'group': 'Group',
           'banCount': '# of ban',
           'chatCount': '# of chats'
       },
       title='Correlation between # of Subscriptions and Unique Users')
#fig.show()

#Correlacion entre el numero de suscriptores y cantidad total de superchats
fig = px.scatter(overall,
       x='chatCount',
       y='scTotalJPY',
       color='subscriptionCount',
       hover_name='name',
       hover_data=['scTotalJPY', 'chatNunique'],
       labels={
           'chatNunique': '# of unique users',
           'chatCountPerUser': 'avg. # of chats per user',
           'subscriptionCount': '# of subscribers',
           'name.en': 'Name',
           'group': 'Group',
           'banCount': '# of ban',
           'chatCount': '# of chats',
           'scTotalJPY': 'Total amount (JPY)'
       },
       title='Correlation between # of chats and total amount of superchats')
#fig.show()

#Canales con mas superchats
fig = px.bar(overall.sort_values(by='scTotalJPY', ascending=False),
       x='name.en',
       y='scTotalJPY',
       color='chatCount',
       hover_name='name',
       hover_data=['chatCount', 'subscriptionCount'],
       labels={
           'chatCount': '# of Chats',
           'subscriptionCount': '# of Subscribers',
           'videoCount': '# of Videos',
           'name.en': 'Name',
           'banCount': '# of Ban',
           'scTotalJPY': 'Total amount (JPY)'
       },
       title='Most superchatted channels')
#fig.show()

#Distribucion de ganancias por superchat
channels['qScTotalJPY'] = pd.qcut(channels['scTotalJPY'], 3, labels=['Lower', 'Medium', 'Higher'])
channels['qScTotalJPY_N'] = pd.qcut(channels['scTotalJPY'], 3, labels=False)

fig = px.parallel_categories(channels,
       color='qScTotalJPY_N',
       color_continuous_scale=px.colors.sequential.Inferno,
       labels={
           'scTotalJPY': 'Total amount (JPY)',
           'qScTotalJPY': 'Income Level',
           'language': 'Language',
           'sex': 'Sex',
           'group': 'Group',
       },
       dimensions=['sex', 'language', 'qScTotalJPY', 'group'],
       title='Superchat <b>income distribution</b>'
).update_layout(coloraxis_showscale=False)
#fig.show()

#Intensidad de los chats por mes
monthly = channels[channels['period'] >= '2021-03'].groupby(['period', 'group']).agg({
    'chatCount': ['sum', 'mean', 'median'],
    'chatNunique': ['mean', 'median'],
    'banCount': ['sum', 'mean', 'median'],
    'banNunique': ['mean', 'median'],
    'deletionCount': ['sum', 'mean', 'median'],
    'scCount': ['sum', 'mean', 'median'],
    'scNunique': ['mean', 'median'],
    'scTotalJPY': ['sum', 'mean', 'median'],
    'affiliation': 'max',
})
monthly.columns = ["_".join(c) for c in monthly.columns.to_flat_index()]

sectorMap = {
    'Hololive': ['1st Generation', '2nd Generation', '3rd Generation', '4th Generation', '5th Generation', 'GAMERS', 'No Group'],
    'Holostars': ['Holostars 1st Gen', 'Holostars 2nd Generation', 'Holostars 3rd Gen'],
    'HoloEN': ['English 1st Gen'],
    'HoloID': ['Indonesia 1st Gen', 'Indonesia 2nd Gen', 'Indonesia 3rd Gen']
}

sector = pd.DataFrame()
for k, v in sectorMap.items():
    aggsec = channels[(channels['period'] >= '2021-03') & (channels['group'].isin(v))].groupby('period').agg({
        'chatCount': 'sum',
        'chatNunique': 'mean',
        'banCount': 'sum',
        'banNunique': 'mean',
        'deletionCount': 'sum',
        'scCount': 'sum',
        'scNunique': 'mean',
        'scTotalJPY': 'sum',
    }).reset_index()
    aggsec['sector'] = k
    sector = sector.append(aggsec, ignore_index=True)

fig = px.bar(sector,
       x='period',
       y='chatCount',
       color='sector',
       labels={
           'chatCount': 'Total number of <b>chats</b>',
           'sector': 'Sector',
           'period': 'Period',
       },
       title='<b>Chats</b> intensity',
).update_xaxes(dtick='M1')
#fig.show()

#Ganancias mensuales de super chats
#Tome en cuenta que YouTube se lleva alrededor del 30% del total de los super chats
fig = px.scatter(sector,
       x='period',
       y='scTotalJPY',
       color='sector',
       log_y=True,
       labels={
           'scTotalJPY': 'Total amount of <b>super chats</b>',
           'sector': 'Sector',
           'period': 'Period',
       },
       title='Monthly <b>super chats</b> income',
).update_xaxes(dtick='M1').update_traces(mode='markers+lines')"""
#fig.show()

superchats = pd.read_csv(r"C:\Users\AcerMX\Documents\Escuela\S7\Big data redes sociales\Unidad 3\Hololive Insights\superchats_2021-03.csv")

print(superchats.head())