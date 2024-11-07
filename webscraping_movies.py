import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = "https://en.everybodywiki.com/100_Most_Highly-Ranked_Films"
db_name = 'Movies.db'
table_name = 'Top_50'
csv_path = '/home/kathung6/projects/helloworld/top_50_films.csv'
df = pd.DataFrame(columns=["Rank","Film","Year", "Rotten Tomatoes' Top 100"])
count = 0

html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

def extract_year(year_text):
    try:
        year =  int(year_text.strip())
        return year
    except ValueError:
        return None
    
#iterate over the contents of rows
for row in rows:
    if count < 25:
            col = row.find_all('td') #extracts all td data objects in the row and saves them to col
            #check if the length of the col is 0 (if there is no data in a current row)
            if len(col) != 0:
                year = extract_year(col[2].get_text(strip=True))
                
                if year and year >= 2000:
                    data_dict = {"Rank": col[0].contents[0],
                                 "Film": col[1].contents[0],
                                 "Year": col[2].contents[0],
                                 "Rotten Tomatoes' Top 100": col[3].contents[0]}
                    df1 = pd.DataFrame(data_dict, index = [0]) #convert the dict to a dataframe and concat with existing df
                    df = pd.concat([df, df1], ignore_index=True)
                    count += 1 #increment loop counter until the counter hits 50
    else:
        break
    
print(df)

df.to_csv(csv_path) #save the dataframe to a csv file

#save the data in a database

#initialize a connection to the database
conn = sqlite3.connect(db_name)
#save the df as a table
df.to_sql(table_name, conn, if_exists='replace',index=False)
# close the connection
conn.close()