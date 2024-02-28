def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    medal_tally=medal_tally.groupby("region").sum()[["Gold","Bronze","Silver"]].sort_values(by="Gold",ascending=False).reset_index()
    medal_tally["Total"]=medal_tally["Gold"]+medal_tally["Silver"]+medal_tally["Bronze"]
    return medal_tally

def list_dropdown(df):
    year_list=sorted(df["Year"].unique().tolist())
    year_list.insert(0,"Overall")
    country_list=sorted(df["region"].dropna().unique())
    country_list.insert(0,"Overall")
    return year_list,country_list


def fetch_medal(df,name,year):
    medal_df=df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    flag=0
    if year=="Overall" and name=="Overall":
        temp_df=medal_df
        temp_df
    elif year !="Overall" and name == "Overall":
        temp_df=medal_df[medal_df["Year"]==int(year)]
        temp_df
    elif year =="Overall" and name!="Overall":
        flag=1
        temp_df=medal_df[medal_df["region"]==name]
    elif year !="Overall" and name !="Overall":
         temp_df=medal_df[medal_df["Year"]==int(year)]
         temp_df=temp_df[medal_df["region"]==name]
    if flag==1:
        x=temp_df.groupby(by="Year").sum()[["Gold","Silver","Bronze"]].sort_values("Year",ascending=False).reset_index()
    else:
        x=temp_df.groupby(by="region").sum()[["Gold","Silver","Bronze"]].sort_values("region",ascending=False).reset_index()

    x["total"]=x["Gold"]+x["Silver"]+x["Bronze"]
    return x


def nations_over_time(df):
    nation_over_time=df.drop_duplicates(["Year","region"])["Year"].value_counts().reset_index().sort_values(by="Year")
    return nation_over_time
    

def events_over_time(df):
    events_over_time=df.drop_duplicates(["Year","Event"])["Year"].value_counts().reset_index().sort_values(by="Year")
    return events_over_time
    

def name_over_time(df):
    name_over_time=df.drop_duplicates(["Year","Name"])["Year"].value_counts().reset_index().sort_values(by="Year")
    return name_over_time


def most_successfull(df,sport):
    temp_df=df.dropna(subset=["Medal"])
    if sport != "Overall":
        temp_df=temp_df[temp_df['Sport']==sport]
    x= temp_df["Name"].value_counts().reset_index().head(15).merge(df,left_on="Name",right_on="Name",how="left")[["Name","count","region","Sport"]].drop_duplicates("Name")
    x.rename(columns={"count":"Medal Counts"},inplace=True)
    return x

def year_wise_medal(df,region):
    temp_df=df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"],inplace=True)
    new_df=temp_df[temp_df["region"]==region]
    final_df=new_df.groupby("Year").count()["Medal"].reset_index()
    return final_df


def country_best_medal(df,region):
    temp_df=df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"],inplace=True)
    new_df=temp_df[temp_df["region"]==region]
    return new_df.pivot_table(index="Sport",columns="Year",values="Medal",aggfunc="count").fillna(0).astype("int")

def most_successfull_country(df,region):
    temp_df=df.dropna(subset=["Medal"])
    
    temp_df=temp_df[temp_df['region']==region]
    x= temp_df["Name"].value_counts().reset_index().head(10).merge(df,left_on="Name",right_on="Name",how="left")[["Name","count","region","Sport"]].drop_duplicates("Name")
    x.rename(columns={"count":"Medal Counts"},inplace=True)
    return x

def weight_v_height(df,sport):
    athlete_df=df.drop_duplicates(subset=["Name","region"])
    athlete_df["Medal"].fillna("No Medal",inplace=True)
    temp_df1=athlete_df[athlete_df["Sport"]==sport]
    return temp_df1


def men_v_women(df):
    athlete_df=df.drop_duplicates(subset=["Name","region"])
    men=athlete_df[athlete_df["Sex"]=="M"].groupby("Year").count()["Name"].reset_index()
    women=athlete_df[athlete_df["Sex"]=="F"].groupby("Year").count()["Name"].reset_index()
    men.sort_values(by="Year",inplace=True)
    women.sort_values(by="Year",inplace=True)
    final=men.merge(women,on="Year",how="left")
    final.rename(columns={"Name_x":"Male","Name_y":"Female"},inplace=True)
    final.fillna(0,inplace=True)
    return final