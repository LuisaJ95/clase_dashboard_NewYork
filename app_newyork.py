# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 16:25:52 2021

@author: Luisa
"""
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import base64



st.set_page_config(layout="wide")# Utilizar la p谩gina completa en lugar de una columna central estrecha

# T铆tulo principal, h1 denota el estilo del t铆tulo 1
st.markdown("<h1 style='text-align: center; color: #3C9AD0;'> 馃椊 Hist贸rico de disparos en Nueva York 馃椊 馃敨 </h1>", unsafe_allow_html=True)


# Funci贸n para importar datos
@st.cache(persist=True) # C贸digo para que quede almacenada la informaci贸n en el cache
def load_data(url):
    df = pd.read_csv(url) # leer datos
    df['OCCUR_DATE'] = pd.to_datetime(df['OCCUR_DATE']) # convertir fecha a formato fecha
    df['OCCUR_TIME'] = pd.to_datetime(df['OCCUR_TIME'], format='%H:%M:%S') # convertir hora a formato fecha
    df['YEAR'] = df['OCCUR_DATE'].dt.year # sacar columna con a帽o
    df['HOUR'] = df['OCCUR_TIME'].dt.hour # sacar columna con hora
    df['YEARMONTH'] = df['OCCUR_DATE'].dt.strftime('%y%m') # sacar columna con a帽o/mes
    df.columns = df.columns.map(str.lower) # convertir columnas a min煤scula
    
    return df


# Funci贸n para descargar base de datos
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv">Descargar archivo csv</a>'
    return href

# Aplicar funci贸n
df = load_data('NYPD_Shooting_Incident_Data__Historic_.csv')

c1, c2, c3, c4, c5= st.beta_columns((1,1,1,1,1))
c1.markdown("<h3 style='text-align: left; color: gray;'> Top sexo </h3>", unsafe_allow_html=True)

top_perp_name = df['perp_sex'].value_counts().index[0]
top_perp_num = (round(df['perp_sex'].value_counts()/df['perp_sex'].value_counts().sum(),2)*100) [0]
top_vic_name = df['vic_sex'].value_counts().index[0]
top_vic_num = (round(df['vic_sex'].value_counts()/df['vic_sex'].value_counts().sum(),2)*100) [0]

c1.text('Atacante: ' +str(top_perp_name)+ ',' +str(top_perp_num)+ '%')
c1.text('V铆ctimas: ' +str(top_vic_name)+ ',' +str(top_vic_num)+ '%')


c2.markdown("<h3 style='text-align: left; color: gray;'> Top raza </h3>", unsafe_allow_html=True)

top_perp_name = df['perp_race'].value_counts().index[0].capitalize()
top_perp_num = (round(df['perp_race'].value_counts()/df['perp_race'].value_counts().sum(),2)*100) [0]
top_vic_name = df['vic_race'].value_counts().index[0].capitalize()
top_vic_num = (round(df['vic_race'].value_counts()/df['vic_race'].value_counts().sum(),2)*100) [0]

c2.text('Atacante: ' +str(top_perp_name)+ ',' +str(top_perp_num)+ '%')
c2.text('V铆ctimas: ' +str(top_vic_name)+ ',' +str(top_vic_num)+ '%')


c3.markdown("<h3 style='text-align: left; color: gray;'> Top Edad </h3>", unsafe_allow_html=True)

top_perp_name = df['perp_age_group'].value_counts().index[0]
top_perp_num = (round(df['perp_age_group'].value_counts()/df['perp_age_group'].value_counts().sum(),2)*100) [0]
top_vic_name = df['vic_age_group'].value_counts().index[0]
top_vic_num = (round(df['vic_age_group'].value_counts()/df['vic_age_group'].value_counts().sum(),2)*100) [0]

c3.text('Atacante: ' +str(top_perp_name)+ ',' +str(top_perp_num)+ '%')
c3.text('V铆ctimas: ' +str(top_vic_name)+ ',' +str(top_vic_num)+ '%')


c4.markdown("<h3 style='text-align: left; color: gray;'> Top Barrio </h3>", unsafe_allow_html=True)

top_perp_name = df['boro'].value_counts().index[0].capitalize()
top_perp_num = (round(df['boro'].value_counts()/df['boro'].value_counts().sum(),2)*100) [0]

c4.text('Barrio: ' +str(top_perp_name)+ ',' +str(top_perp_num)+ '%')



c5.markdown("<h3 style='text-align: left; color: gray;'> Top Hora </h3>", unsafe_allow_html=True)

top_perp_name = df['hour'].value_counts().index[0]
top_perp_num = (round(df['hour'].value_counts()/df['hour'].value_counts().sum(),2)*100) [0]

c5.text('Hora: ' +str(top_perp_name)+ ',' +str(top_perp_num)+ '%')
#---------------------------------------------------------------------

# Dividir el layout en cuatro partes
c1, c2= st.beta_columns((1,1)) # Entre par茅ntesis se indica el tama帽o de las columnas


# Hacer c贸digo de la primera columna (Mapa sencillo):
c1.markdown("<h3 style='text-align: center; color: withe;'> 驴D贸nde han ocurrido disparos en Nueva York? </h3>", unsafe_allow_html=True)
year = c1.slider('A帽o en el que se presento el suceso', 2006,2020) # Crear variable que me almacene el a帽o seleccionado
c1.map(df[df['year']==year][['latitude', 'longitude']].dropna()) # Generar mapa

  
# Hacer c贸digo de la segunda columna:
c2.markdown("<h3 style='text-align: center; color: withe;'> 驴A qu茅 horas ocurren disparos en Nueva York? </h3>", unsafe_allow_html=True)
hora = c2.slider('Hora en la que se presento el suceso', 0,23) # Crear variable que me almacene la hora seleccionada
df2 = df[df['hour']==hora] # Filtrar DataFrame


c2.write(pdk.Deck( # C贸digo para crear el mapa
    
    # Set up del mapa
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state={
        'latitude' : df['latitude'].mean(),
        'longitude': df['longitude'].mean(),
        'zoom' : 9.5,
        'pitch': 50
        },
    
    # Capa con informaci贸n
    layers = [pdk.Layer(
        'HexagonLayer',
        data = df2[['incident_key','latitude','longitude']],
        get_position = ['longitude','latitude'],
        radius = 100,
        extruded = True,
        elevation_scale = 4,
        elevation_range = [0,1000])]
    ))

#---------------------------------------------------------------------

# T铆tulo de la siguiente secci贸n
st.markdown("<h3 style='text-align: center; color: withe;'> 驴C贸mo ha sido la evoluci贸n de disparos por barrio? </h3>", unsafe_allow_html=True)

# Organizar DataFrame
df2 = df.groupby(['yearmonth','boro'])[['incident_key']].count().reset_index().rename(columns = {'incident_key':'disparos'})

# Generar gr谩fica
fig = px.line(df2, x='yearmonth', y='disparos', color = 'boro', width=1100, height=450)

# Editar gr谩fica
fig.update_layout(
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        xaxis_title="<b>A帽o<b>",
        yaxis_title='<b>Cantidad de incidentes<b>',
        legend_title_text='',
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.8))

# Enviar gr谩fica a streamlit
st.plotly_chart(fig)

# Dividir siguiente secci贸n
c4, c5, c6, c7= st.beta_columns((1,1,1,1))

################ ---- Primera Gr谩fica

# Definir t铆tulo
c4.markdown("<h3 style='text-align: center; color: withe;'> 驴Qu茅 edad tienen los atacantes? </h3>", unsafe_allow_html=True)

# Organizar DataFrame
df2 = df.groupby(['perp_age_group'])[['incident_key']].count().reset_index().rename(columns = {'incident_key':'disparos'})

# Editar categor铆as mal escritas
df2['perp_age_group'] = df2['perp_age_group'].replace({'940':'UNKNOWN',
                              '224':'UNKNOWN','1020':'UNKNOWN'})

# Cambiar UNKNOWN por un nombre m谩s corto
df2['perp_age_group'] = df2['perp_age_group'].replace({
                              'UNKNOWN': 'N/A'})

# Crear categor铆a para organizar el orden de las edades
df2['perp_age_group2'] = df2['perp_age_group'].replace({'<18':'1',
                              '18-24':'2',
                              '25.44':'3',
                              '45-64':'4',
                              '65+':'5',
                              'UNKNOWN': '6'})
# Aplicar orden al DataFrame
df2= df2.sort_values('perp_age_group2',ascending = False)

# Hacer gr谩fica
fig = px.bar(df2, x="disparos", y="perp_age_group", orientation='h', width=340,  height=310)
fig.update_layout(xaxis_title="<b>Atacante<b>",
                  yaxis_title="<b>Edades<b>", template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')

# Enviar gr谩fica a streamlit
c4.plotly_chart(fig)

################ ---- Segunda Gr谩fica


# Definir t铆tulo
c5.markdown("<h3 style='text-align: center; color: withe;'> 驴Qu茅 edad tienen los v铆ctimas? </h3>", unsafe_allow_html=True)

# Organizar DataFrame
df2 = df.groupby(['vic_age_group'])[['incident_key']].count().reset_index().rename(columns = {'incident_key':'disparos'})

# Crear categor铆a para organizar el orden de las edades
df2['vic_age_group2'] = df2['vic_age_group'].replace({'<18':'1',
                              '18-24':'2',
                              '25.44':'3',
                              '45-64':'4',
                              '65+':'5',
                              'UNKNOWN': '6'})

# Cambiar UNKNOWN por un nombre m谩s corto
df2['vic_age_group'] = df2['vic_age_group'].replace({
                              'UNKNOWN': 'N/A'})

# Aplicar orden al DataFrame
df2= df2.sort_values('vic_age_group2',ascending = False)

# Hacer gr谩fica
fig = px.bar(df2, x="disparos", y="vic_age_group", orientation='h', width=340,  height=310)
fig.update_layout(xaxis_title="<b>V铆ctimas<b>",
                  yaxis_title="<b><b>", template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')

# Enviar gr谩fica a streamlit
c5.plotly_chart(fig)

################ ---- Tercera Gr谩fica

# Definir t铆tulo
c6.markdown("<h3 style='text-align: center; color: withe;'> 驴Cu谩l es el sexo del atacante? </h3>", unsafe_allow_html=True)

# Organizar DataFrame
df2 = df.groupby('perp_sex')[['incident_key']].count().reset_index().sort_values('incident_key', ascending = False)

# Hacer gr谩fica
fig = px.pie(df2, values = 'incident_key', names="perp_sex",
             width=300, height=300)
fig.update_layout(template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  legend=dict(orientation="h",
                              yanchor="bottom",
                              y=-0.4,
                              xanchor="center",
                              x=0.5))

# Enviar gr谩fica a streamlit
c6.plotly_chart(fig)

################ ---- Cuarta Gr谩fica

# Definir t铆tulo
c7.markdown("<h3 style='text-align: center; color: withe;'> 驴Cu谩l es el sexo de la v铆ctima? </h3>", unsafe_allow_html=True)

# Organizar DataFrame
df2 = df.groupby('vic_sex')[['incident_key']].count().reset_index().sort_values('incident_key', ascending = False)

# Hacer gr谩fica
fig = px.pie(df2, values = 'incident_key', names="vic_sex",
             width=300, height=300)
fig.update_layout(template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  legend=dict(orientation="h",
                              yanchor="bottom",
                              y=-0.4,
                              xanchor="center",
                              x=0.5))

# Enviar gr谩fica a streamlit
c7.plotly_chart(fig)


#---------------------------------------------------------------------

# Definir t铆tulo
st.markdown("<h3 style='text-align: center; color: Black;'> Evoluci贸n de disparos por a帽o en las horas con m谩s y menos sucesos </h3>", unsafe_allow_html=True)

# Organizar DataFrame
df2 = df[df['hour'].isin([23,9])].groupby(['year','hour'])[['incident_key']].sum().sort_values('incident_key', ascending = False).reset_index() 
df2['hour'] = df2['hour'].astype('category')


# Hacer gr谩fica
fig = px.bar(df2, x='year', y='incident_key', color ='hour', barmode='group', width=1150, height=450)
fig.update_layout(
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        legend_title_text = 'Hora',
        xaxis_title="<b>A帽o<b>",
        yaxis_title="<b>Cantidad de incidentes<b>")

# Enviar gr谩fica a streamlit
st.plotly_chart(fig)

#---------------------------------------------------------------------

# Hacer un checkbox
if st.checkbox('Obtener datos por fecha y barrio', False):
    
    # C贸digo para generar el DataFrame
    df2 = df.groupby(['occur_date','boro'])[['incident_key']].count().reset_index().rename(columns ={'boro':'Barrio','occur_date':'Fecha','incident_key':'Cantidad'})
    df2['Fecha'] = df2['Fecha'].dt.date
    
    # C贸digo para convertir el DataFrame en una tabla plotly resumen
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df2.columns),
        fill_color='lightgrey',
        line_color='darkslategray'),
        cells=dict(values=[df2.Fecha, df2.Barrio, df2.Cantidad],fill_color='white',line_color='lightgrey'))
       ])
    fig.update_layout(width=500, height=450)

# Enviar tabla a streamlit
    st.write(fig)

#Generar link de descarga

    st.markdown(get_table_download_link(df2), unsafe_allow_html=True) #df2 es la base que quiero que me descargue


