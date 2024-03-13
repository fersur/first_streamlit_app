
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
# fruit_choice = streamlit.text_input('What fruit would you like information about?')
# fruit_choice2 = streamlit.text_input('What fruit would you like to add?','Jackfruit') # has default value
# streamlit.write('The user entered ', fruit_choice)
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response)
#streamlit.text(fruityvice_response.json())
#normalized the json file from previous response
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#put the normalized result into data frame
#streamlit.dataframe(fruityvice_normalized)

# Snowflake database function
def get_fruityvice_data(fruit_data):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_data)  
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())  
    return(fruityvice_normalized)

def get_fruit_list():
    with my_cnx.cursor() as my_cur:
            my_cur.execute("Select * from fruit_load_list")
            return my_cur.fetchall()    

def insert_new_fruit(new_fruit):
    with my_cnx.cursor() as my_cur:
            my_cur.execute("insert into fruit_load_list values(new_fruit)")
            return "Thanks for adding " +  new_fruit + " to the list."

try:  
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error('Please enter a fruit name.')
    else:
        call_fruit_function =  get_fruityvice_data(fruit_choice)
        streamlit.dataframe(call_fruit_function)
        
except URLError as e:
  streamlit.error()

# streamlit.stop()

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_cur.execute("Select * from fruit_load_list")
#my_data_row = my_cur.fetchall()

streamlit.header("The fruity list contains: ")
# add a button
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
    my_data_row = get_fruit_list()
    streamlit.dataframe(my_data_row)


# streamlit.stop()

#allow user to add fruit to the list
fruit_choice2 = streamlit.text_input('What fruit would you like to add?')
# streamlit.write('Thanks for adding ', fruit_choice2)

# This will not work correctly
# my_cur.execute("insert into fruit_load_list values('from_streamlit')")
# add a button
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
    insert_fruit = insert_new_fruit(fruit_choice2)
    streamlit.dataframe(insert_fruit)


streamlit.stop()
