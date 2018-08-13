import csv
import pandas as pd
from Levenshtein import distance
import re
import pymysql
from sqlalchemy import create_engine

csvfilename_1 = 'exercise_part_1.csv'
csvfilename_2 = 'exercise_part_2.csv'

df1 = pd.read_csv(csvfilename_1, sep=';')
df2= pd.read_csv(csvfilename_2, sep=';')

address_list_1 = []
address_list_2 = []
abbrev_list = ['st', 'st.', 'rd']
var_ratio_list = []
match_num = 0

def string_replace(address, word):
    if word == 'st.':
        return address.replace('st.', 'street')
    elif word == 'st':
        if 'street' in address:
            return address
        else:
            return address.replace('st', 'street')
    elif word == 'rd':
        return address.replace('rd', 'road')

########################################
### Address String Matching Operations        

for i in range(len(df1)):
    # all lowercase
    address_1 = df1.address[i].lower()
    address_2 = df2.address[i].lower()

    # out with punctuation
    address_1 = re.sub(r'[^\w\s]','', address_1)
    address_2 = re.sub(r'[^\w\s]','', address_2)

    # standardize street/road naming
    for word in abbrev_list:
        if word in address_1:
            address_1 = string_replace(address_1, word)
        if word in address_2:
            address_2 = string_replace(address_2, word)

    # correct spacing
    address_1_words = address_1.split(' ')
    address_2_words = address_2.split(' ')

    address_1_words = [word.strip() for word in address_1_words]
    address_2_words = [word.strip() for word in address_1_words]

    address_1 = ' '.join(address_1_words) 
    address_2 = ' '.join(address_2_words)

    # Add to each list: Tuple with Adress and Variable
    address_list_1.append((address_1, df1.variable1[i]))
    address_list_2.append((address_2, df2.variable2[i]))

    var_ratio_list.append(round(df1.variable1[i]/df2.variable2[i], 2))



#########################################
### Find number of successful matches


for i in range(len(address_list_1)):
    if address_list_1[i][0] == address_list_2[i][0]:
        match_num +=1

print('Each CSV file has', len(df1),'addresses.')
print('Total matches:', match_num)
print('\n')
if match_num == len(df1):
    print('All address results have been matched successfully.')


# #######################################
# ### Join 2 Datasets using SQL 

# engine = create_engine('sqlite://', echo=False)
# df1.to_sql('results_1', con=engine)
# df2.to_sql('results_2', con=engine)

# print(engine.execute("SELECT * FROM results_1").fetchall())
# print(engine.execute("SELECT * FROM results_2").fetchall())

# """ ENTER SQL Merge, Join Commands here """
# """ Export to CSV """

###########################################
### Join 2 Datasets using Pandas


df_final =  pd.DataFrame({'id_store': df1.id_store,
                    'address': [adress[0] for adress in address_list_1],
                    'var1/var2': var_ratio_list,
                    'category': df1.category})

df_final.to_csv('exercise_solution.csv', encoding='utf-8')

        