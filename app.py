import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt
from PIL import Image
import plotly.graph_objects as go
brush = alt.selection_interval( bind='scales')

st.set_page_config(page_title='Impression Results')
st.header('Impression Results February - August 2022')
st.subheader('')

# excel_file = 'Extension Impression.csv'
df = pd.read_csv('Extension Impression1.csv', encoding='latin-1')
df2 = pd.read_csv('Twitter_ALL.csv')
df = df.astype({"Extension install": int}, errors='raise')
df = df.astype({"Extension uninstall": int}, errors='raise')
# df.dtypes
# print(df2)

# st.dataframe(df)
# st.line_chart(df)
# test = df.astype(str)
df = df.melt('Ngày', var_name='name', value_name='value')
df['Ngày'] = df['Ngày'].apply(pd.to_datetime)
df = df.sort_values(by='Ngày')
#
#
# print(type(df['Ngày'][0]))
# st.write(df)
zoom = alt.selection_interval(
    bind='scales',
    on="[mousedown[!event.shiftKey], mouseup] > mousemove",
    translate="[mousedown[!event.shiftKey], mouseup] > mousemove!",
)

selection = alt.selection_interval(
    on="[mousedown[event.shiftKey], mouseup] > mousemove",
    translate="[mousedown[event.shiftKey], mouseup] > mousemove!",
)
chart = alt.Chart(df).mark_line().encode(
  x=alt.X('Ngày:T',  axis=alt.Axis(labelOverlap="greedy",grid=False)),
  y=alt.Y('value:Q',impute=alt.ImputeParams(value=None)),
  color=alt.Color("name:N")
).properties(title="EXTENSION").add_selection(zoom, selection)


chart
#
# # load the data
# # source = pd.read_csv("test.csv")
#
# # specify the type of selection, here single selection is used
# selector = alt.selection_single(encodings=['x', 'color'])
#
# # use mark_bar function to plot a stacked bar and specify x and y axis
# chart = alt.Chart(df2).mark_are().encode(
#     x='Date:T',
#     y='sum(Vote %)',
#     color=alt.condition(selector, 'Party', alt.value('lightgray'))
# ).add_selection(
#     selector
# )
# # initializer altair_viewer to display the interactive chart
# alt.renderers.enable('altair_viewer')
# chart.show()

import altair as alt
from vega_datasets import data

source = data.iowa_electricity()
# df_retweet = df2.filter(['Date','retweets'],axis =1)
# df_retweet['Source'] = 'retweet'
# print(df_retweet)

def createdf(name):
    df_new = df2.filter(['Date', name], axis=1)
    df_new['Source'] = name
    df_new.rename({name: 'click'}, axis=1, inplace=True)
    return df_new
df_retweet = createdf('retweets')
df_replies = createdf('replies')
df_likes = createdf('likes')
df_user = createdf('user profile clicks')
df_url = createdf('url clicks')
df_hashtag  = createdf('hashtag clicks')
df_detail  = createdf('detail expands')
df_media  = createdf('media engagements')
#
df3 = df_retweet.append([df_media,df_detail,df_hashtag,df_url,df_user,df_likes,df_replies], ignore_index=True)

click_list = ['retweets','replies', 'likes','user profile clicks','url clicks',
              'hashtag clicks','detail expands','media engagements']
click_select = st.multiselect("Engagement source", click_list, default=click_list)

twitter = alt.Chart(df3[df3['Source'].isin(click_select)]).mark_area().encode(
    x=alt.X('Date:T',  axis=alt.Axis(labelOverlap="greedy",grid=False)),
    y="click:Q",
    color="Source:N"
).interactive().add_selection(zoom, selection)
twitter
#
# barr = alt.Chart( df2.filter(['Date', 'engagement']).mark_bar().encode(
#     x=alt.X('Date:T',  axis=alt.Axis(labelOverlap="greedy",grid=False)),
#     y='engagement'
# ).add_selection(zoom, selection)
#
# barr

df4 = df2.filter(['Date','Tweets published','engagement rate'],axis =1)
df4['engagement rate'] = df4['engagement rate']*100
df4.rename({'Tweets published': 'number of tweets published - BLUE'}, axis=1, inplace=True)
df4.rename({'engagement rate': 'engagement rate (%) - RED'}, axis=1, inplace=True)

chart_base = alt.Chart(df4).encode(
    alt.X('Date:T',
    axis=alt.Axis(),
    scale=alt.Scale(zero=False)
    )
).properties(width=800, height=400)

line_prec = chart_base.mark_line(color='blue', size=1).encode(y='mean(number of tweets published - BLUE)')
combi = alt.layer(line_prec, line_temp).resolve_scale(y='independent')
combi
