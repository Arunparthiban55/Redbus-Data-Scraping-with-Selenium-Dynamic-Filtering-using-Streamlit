import streamlit as st
import mysql.connector
import pandas as pd

#backkground color setings
pag_bg_img=""" 
<style>
[data-testid="stAppViewContainer"]{
background-color: #F7595E }
[data-testid="stHeader"]{
background-color: #F7595E }
[data-testid="stToolbar"]{
right: 2rem;}
[data-testid="stSidebarContent"]{
background-color:#F9787C}
<\style>
"""
st.markdown(pag_bg_img,unsafe_allow_html=True)
#\backkground color setings

#msql connection
mydb = mysql.connector.connect(    
 host=st.secrets["host"],
 user=st.secrets["user"],
 password=st.secrets["password"],
 autocommit = True
)
cursor = mydb.cursor(buffered=True)
#\msql connection

#dataframe defining
cursor.execute("SELECT * FROM redbus_mdte11.entire_transport_routes")
data = cursor.fetchall()
df=pd.DataFrame(data,columns=cursor.column_names)
cursor.execute("SELECT * FROM redbus_mdte11.entire_bus_details")
data = cursor.fetchall()
df2=pd.DataFrame(data,columns=cursor.column_names)
#data correction for time data 
df2["departing_time"]=df2["departing_time"].astype('str')
df2["reaching_time"]=df2["reaching_time"].astype('str')
df2['departing_time']=df2['departing_time'].str.replace('0 days ','')
df2['reaching_time']=df2['reaching_time'].str.replace('0 days ','')
#\dataframe defining

#sidebar
st.sidebar.markdown("<h1 style='text-align: centre; color: white;'>redBus</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align: centre justified; color: #F6F26D;'>Apno ko, sapno ko kareeb laye</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align: left; color: white;'>Select your Preference</h3>", unsafe_allow_html=True)


state=st.sidebar.selectbox("**State Transport**",list(df["state_transport"].unique()),placeholder="Choose an option")
route=st.sidebar.selectbox("**Trip Route**",list(df["routes_name"][df["state_transport"]==state]),placeholder="Choose an option")

lin=df['route_link'][df["routes_name"]==route].item()

ty=list(df2["bus_type"][df2["route_link"]==lin].unique())
bus=[]
for i in ty:
    if "SEEPER" in i or 'Sleeper' in i:
        bus.append('SLEEPER') 
    if "AC" in i or 'A/C' in i or 'A.C' in i:
        bus.append('AC')
    if 'NON' in i or 'Non' in i:
        bus.append('NON-AC')                    
type=st.sidebar.selectbox("**Bus Type**",set(bus),placeholder="Choose an option")
# grouping all bus type by ac,non ac , sleeper since data bus type is is different
if type=='SLEEPER':
    bus_ty=[i for i in ty if "SEEPER" in i or 'Sleeper' in i]
elif type=='AC':
    bus_ty=[]
    for i in ty:
        if 'NON' not in i or 'Non' not in i:
            if "AC" in i or 'A/C' in i or 'A.C' in i:
                bus_ty.append(i)
elif type=='NON-AC':
    bus_ty=[j for j in ty if 'NON' in j or 'Non' in j]                

rat_lis=list(df2["star_rating"][(df2["route_link"]==lin) & (df2["bus_type"].isin(bus_ty))].unique())
rat_lis.sort()
rating=st.sidebar.selectbox("**Star Rating**",rat_lis)

pr_lis=list(df2["price"][(df2["route_link"]==lin) & (df2["bus_type"].isin(bus_ty)) | (df2["star_rating"]>=rating)])
pr_lis.sort()
pr_lis=[int(i) for i in pr_lis]
a=min(pr_lis)
for i in range(1,1000):
    if (a-i)%100==0:
        a=int(a-i)
        break
b=max(pr_lis)
for i in range(1,1000):
     if (b-i)%100==0:
        b=int(b-i)
        break
pr_range=[]
for i in range(a,b,500):
    if (b-a)>100:
        pr_range.append(f'{i}-{i+500}')
    elif (b-a)<=100:
        pr_range.append(f'{b}') 
    elif a==b:
        pr_range.append(f'{b}')
   
price=st.sidebar.selectbox("**Price Range**",pr_range)
if '-' in price:
    a,b=map(int,price.split('-'))
else:
    a=0

st_lis=list(set(df2["departing_time"][(df2["route_link"]==lin) & (df2["bus_type"].isin(bus_ty)) & (df2["star_rating"]>=rating) & (df2['price'] >= a) & (df2['price'] <= b) ]))
st_lis.sort()
depart=st.sidebar.selectbox("**Departing Time**",st_lis,placeholder="Choose an option")

re_lis=list(set(df2["reaching_time"][(df2["route_link"]==lin) & (df2["bus_type"].isin(bus_ty)) & (df2["star_rating"]>=rating) & (df2['price'] >= a) & (df2['price'] <= b) & (df2['departing_time']>=depart)]))
re_lis.sort()
reach=st.sidebar.selectbox("**Reaching Time**",re_lis,placeholder="Choose an option")

bus_button=st.sidebar.button("**Find Buses**")
#\sidebar


if bus_button:
    start=df['first_bus'][df["routes_name"]==route].item()
    last=df['last_bus'][df["routes_name"]==route].item()
    min_fare=df['Starting_Price'][df["routes_name"]==route].item()
    
    outdf = df2[(df2['route_link']==lin) & (df2['bus_type'].isin(bus_ty)) & (df2['price'] >= a) & (df2['price'] <= b) & (df2['star_rating']>=rating) & (df2['departing_time']>=depart) & (df2['reaching_time']>=reach)]
    tot_bus=len(outdf)

    st.markdown(f"<h3 style='text-align: center; color: white;'>Since your route is {route} try to plan your trip between {start}am to {last}pm </h3>", unsafe_allow_html=True)
    col1,col2=st.columns((1,1))
    with col1:
        st.markdown(f"<h5 style='text-align: center; color: #F6F26D;'>Your trip's fare starts from  {min_fare} </h5>", unsafe_allow_html=True)
        st.markdown(f"<h5 style='text-align: center; color: #F6F26D;'>Total of {tot_bus} Buses found by your preference. </h5>", unsafe_allow_html=True)
    with col2:
        st.link_button("Book your ticket now",lin) 
    
    st.dataframe(outdf[['bus_name', 'departing_time', 'duration', 'reaching_time',
    'star_rating', 'price', 'seat_availability',
    'vacant_type']],hide_index=True)

    
    

else:
    #title wordings
    st.markdown("<h1 style='text-align: centre; color: white;'>redBus</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: centre justified; color: #F6F26D;'>Apno ko, sapno ko kareeb laye</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white;'>India's No. 1 Online Bus Ticket Booking Site</h3>", unsafe_allow_html=True)
    #\title wordings
    st.divider()
    st.markdown(f"<h4 style='text-align: centre; color: #F6F26D;'>Find your bus by selecting</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: centre; color: #F6F26D;'>your preferred options at sidebar of this page for your trip</h4>", unsafe_allow_html=True)
