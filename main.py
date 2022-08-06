import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Survey Result', page_icon=":shark:")
st.header('Departments Performance-2021')
st.subheader('Interactive Data Visualization')

hide_menu_style = """
          <style>
           #Mainmenu {visibility:hidden;}
           footer {visibility:hidden;}
            </style>
            """
st.markdown(hide_menu_style, unsafe_allow_html=True)

### --- LOAD DATEFRAME
excel_file='Survey_Results.xlsx'
sheet_name='DATA'
df=pd.read_excel(excel_file,sheet_name,usecols='B:D',header=3)
st.dataframe(df)
df_participants=pd.read_excel(excel_file,sheet_name,usecols='F:G',header=3)
df_participants.dropna(inplace=True)

# Streamlit Selection
department=df['Department'].unique().tolist()
ages=df['Age'].unique().tolist()
age_selection=st.slider('Age:',
                        min_value=min(ages),
                        max_value=max(ages),
                        value=(min(ages),max(ages)))
department_selection=st.multiselect('Department:',
                                    department,
                                    default=department)

# Filter DataFrame Based on Selection
mask=(df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
number_of_result=df[mask].shape[0]
st.markdown(f'*Availabel Results:{number_of_result}*')

# ---- Group DataFrame After Selection
df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age':'Votes'})
df_grouped = df_grouped.reset_index()

# PLot Bar Chart
bar_chart=px.bar(df_grouped,
                x='Rating',
                y='Votes',
                text='Votes',
                color_discrete_sequence=['#F63366']*len(df_grouped),
                template='plotly_white')
st.plotly_chart(bar_chart)


# Display image & DataFrame
col1, col2 =st.columns(2)
image=Image.open('survey.jpg')
print(image)
col1.image(image,caption='Designed by Saiful Quadir', use_column_width=True)
col2.dataframe(df[mask])


# PLot Pie Chart
pie_chart =px.pie(df_participants,title='Total No. of Participant', values='Participants', names='Departments')
st.plotly_chart(pie_chart)
