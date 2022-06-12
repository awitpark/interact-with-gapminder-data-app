import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout = 'wide')
st.title('Interact with Gapminder Data')

df = pd.read_csv('Data/gapminder_tidy.csv')

continent_list = list(df['continent'].unique())
metric_list = list(df['metric'].unique())

metric_labels = {'gdpPercap':'GDP Per Capita','pop':'Population','lifeExp':'Average Life Expectancy'}



def format_metric(metric_raw):
    return metric_labels[metric_raw]

with st.sidebar:
    st.subheader('Configure the plot')
    continent = st.selectbox(label = 'Choose a continent', options = continent_list)
    metric = st.selectbox(label = 'Choose a metric', options = metric_list, format_func = format_metric)
    #The function input should be the value being selected from the list. 
    show_data = st.checkbox(label = 'Show the data used to generate this plot', value = False)


query = f"continent == '{continent}' & metric == '{metric}'"
df_filtered = df.query(query)
country_list = list(df_filtered['country'].unique())

countries = st.sidebar.multiselect('Which countries should be plotted', options = country_list, default = country_list)

df_filtered = df_filtered[df_filtered.country.isin(countries)]

year_min = int(df_filtered['year'].min())
year_max = int(df_filtered['year'].max())

years = st.sidebar.slider('What years show be plotted', min_value = year_min, max_value = year_max, value = (year_min, year_max))

st.write(years)

df_filtered = df_filtered[(df_filtered.year >= years[0]) & (df_filtered.year <= years[1])]

title = f'{metric_labels[metric]} for countries in {continent}'

fig = px.line(df_filtered, x= 'year', y= 'value', color = 'country', title = title, labels = {'value':f'{metric_labels[metric]}'})

st.plotly_chart(fig, use_container_width = True)
plot_desc = f'This plot shows the {metric_labels[metric]} for countries in {continent}.'
st.markdown(plot_desc)

if show_data:
    st.dataframe(df_filtered)