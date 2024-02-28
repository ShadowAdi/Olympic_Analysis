import pandas as pd
import streamlit as st
import numpy as np
import preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff


df=pd.read_csv("./data/athlete_events.csv")
events_df=pd.read_csv("./data/noc_regions.csv")
df=preprocessor.preprocess(df,events_df)

st.sidebar.header("Olympic Analysis")
user_menu=st.sidebar.radio("Select an option",("Medal Tally","Overall Analysis","Countrty Wise Analysis","Athlete Wise Analysis"))

if user_menu=="Medal Tally":
    st.sidebar.header("Medal Tally")
    year_list,country_list=helper.list_dropdown(df)
    year=st.sidebar.selectbox("Select A Year",year_list)
    country=st.sidebar.selectbox("Select A Country",country_list)

    if year=="Overall" and country =="Overall":
        st.header(f"Overall Tally")
    
    st.header(f"Analysis for {country} in {year}")

    medal_tally=helper.fetch_medal(df,year=year,name=country)
    st.table(medal_tally)

    
if user_menu=="Overall Analysis":
    editions=len(df["Year"].unique())-1
    cities=len(df["City"].unique())
    sport=len(df["Sport"].unique())
    event=len(df["Event"].unique())
    name=len(df["Name"].unique())
    regions=len(df["region"].unique())

    st.title("Overall Statistics")

    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sport)
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(event)
    with col2:
        st.header("Nations")
        st.title(regions)
    with col3:
        st.header("Athletes")
        st.title(name)

    st.divider()
    

    nation_over_time=helper.nations_over_time(df)
    st.header("Participating Nation Over The Years")
    fig=px.line(nation_over_time,x="Year",y="count")
    st.plotly_chart(fig)

    event_over_time=helper.events_over_time(df)
    st.header("Events Happening Over The Years")
    fig=px.line(event_over_time,x="Year",y="count")
    st.plotly_chart(fig)

    name_over_time=helper.name_over_time(df)
    st.header("Athletes Participating Over The Years")
    fig=px.line(name_over_time,x="Year",y="count")
    st.plotly_chart(fig)


    st.title("No. of Events over time (Every Sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(["Year","Sport","Event"])
    ax=sns.heatmap(x.pivot_table(index="Sport",columns="Year",values="Event",aggfunc="count").fillna(0).astype("int"),annot=True,cmap="Blues")
    st.pyplot(fig)

    st.divider()


    st.title("Most Successfull Athletes")
    sport_list=df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Overall")
    sport=st.selectbox("Select A Sport",sport_list)
    x=helper.most_successfull(df,sport)
    st.table(x)

   
if user_menu=="Countrty Wise Analysis":
    pass
    # region=st.sidebar.selectbox("Select A Country",df["region"].dropna().unique())
    # st.header(f"Medal Won By {region} On All Olymipcs")

    # df_year=helper.year_wise_medal(df,region)

    # fig=px.line(df_year,x="Year",y="Medal")
    # st.plotly_chart(fig)

    # pt=helper.country_best_medal(df,region)

    # st.header(f"{region} excels in Following Sports")

    # fig,ax=plt.subplots(figsize=(20,20))
    # ax=sns.heatmap(pt,annot=True,cmap="Blues")
    
    # ax.set_xticklabels(ax.get_xticklabels(), fontsize=22)
    # ax.set_yticklabels(ax.get_yticklabels(), fontsize=22)
    # st.pyplot(fig)

    # st.header(f"Best 10 Players of {region}")
    # player_df=helper.most_successfull_country(df,region)
    # st.table(df)

if user_menu=="Athlete Wise Analysis":
    st.header("Distribution based on Age for Medals")
    athlete_df=df.drop_duplicates(subset=["Name","region"])
    x1=athlete_df["Age"].dropna()
    x2=athlete_df[athlete_df["Medal"]=="Gold"]["Age"].dropna()
    x3=athlete_df[athlete_df["Medal"]=="Silver"]["Age"].dropna()
    x4=athlete_df[athlete_df["Medal"]=="Bronze"]["Age"].dropna()
    fig=ff.create_distplot([x1,x2,x3,x4],["Overall Age","Gold Medalist","Silver Medalist","Bronze Medalist"],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)


    st.divider()


    x=[]
    name=[]
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df=athlete_df[athlete_df["Sport"]==sport]
        x.append(temp_df[temp_df["Medal"]=="Gold"]["Age"].dropna())
        name.append(sport)

    fig=ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age with Sport")
    st.plotly_chart(fig)

    st.divider()


    st.header("Weight Vs Height Based On Medals")
    sport_list=df["Sport"].unique().tolist()
    sport_list.sort()
    sport=st.sidebar.selectbox("Select A Sport",sport_list)

    x_df=helper.weight_v_height(df,sport=sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(x=x_df["Height"],y=x_df["Weight"],hue=x_df["Medal"],style=x_df["Sex"],s=20)
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=6)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=6)
    st.pyplot(fig)

    st.divider()

    st.header("Male Vs Female Participation On Olympics")

    final=helper.men_v_women(df)
    fig=px.line(final,x="Year",y=["Male","Female"])
    fig.update_layout(autosize=False,width=1000,height=600)

    st.plotly_chart(fig)




