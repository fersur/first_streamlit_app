
import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach, and Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#Let's put a pick list here
#streamlit.multiselect("Pick some fruits: ",list(my_fruit_list.index),['Avocado','Strawberries'])

#Let's add a sample picklist here
fruits_selected = streamlit.multiselect("Pick some fruits: ",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")

# adding text field and notify user
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response)
#streamlit.text(fruityvice_response.json())

# normalized the json file from previous response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# put the normalized result into data frame
streamlit.dataframe(fruityvice_normalized)

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("Select * from fruit_load_list")
my_data_row = my_cur.fetchall()
# streamlit.text("Hello from Snowflake:")
streamlit.header("The fruity list contains: ")
streamlit.dataframe(my_data_row)

#allow user to add fruit to the list
fruit_choice2 = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('The user entered ', fruit_choice2)

# This will not work correctly
my_cur.execute("insert into fruit_load_list values('from_streamlit')")
