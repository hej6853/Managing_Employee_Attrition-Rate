# Import libraries
import pandas as pd
import datetime
import numpy as np
import math
import matplotlib.pyplot as plt
from pandas import DataFrame as df
from sklearn import preprocessing

#import Data File to CSV
export30 = pd.read_csv('export30_drop_duplicated.csv')
export31 = pd.read_csv('export31_drop_duplicated.csv')
export32 = pd.read_csv('export32_drop_duplicated.csv')
export33 = pd.read_csv('export33_drop_duplicated.csv')
frames = [export30, export31, export32,export33]
state = pd.concat(frames).drop_duplicates()

state.groupby('PRTNR_ID').value_counts()

#Delete the employee whose active status is always 0
# Find employees whose active status is alwyas 0
state1 = pd.DataFrame(state.groupby(['PRTNR_ID'])['PRTNR_ACTIVE_FLG'].sum())
state1 = state1['PRTNR_ACTIVE_FLG'].reset_index()
state1 = state1[state1['PRTNR_ACTIVE_FLG'] == 0]
state1 = state1.drop(['PRTNR_ACTIVE_FLG'], axis=1).reset_index().drop(['index'], axis=1)
state1 =list(state1['PRTNR_ID'])


#drop the partners row whose active stats is always 0
to_drop = state1
state = state[~state['PRTNR_ID'].isin(to_drop)]

# Change time format
state['FiscalWeekBeginDate']=pd.to_datetime(state['FiscalWeekBeginDate'])

# Total # of Employees
len(state['PRTNR_ID'].unique())

#get a dataframe contains Unique Partner's ID
unique_prtnr_ID = pd.DataFrame(state['PRTNR_ID'].unique())
unique_prtnr_ID = unique_prtnr_ID.rename(columns = {0:'PRTNR_ID'})

#Each Employee's the earliest start date (=FiscalWeekBeginDate min_value)
earliest_FiscalWeekBeginDate = state.groupby(['PRTNR_ID'])['FiscalWeekBeginDate'].min()
earliest_FiscalWeekBeginDate = earliest_FiscalWeekBeginDate.reset_index()

# each employees' job count
employee_jobs = state[['PRTNR_ID','JOB_NM']].drop_duplicates()
the_number_of_jobs = employee_jobs.groupby(['PRTNR_ID'])['JOB_NM'].count().reset_index()
the_number_of_jobs = the_number_of_jobs.rename(columns={'JOB_NM': 'count_position'})

# Find the last job position name
last_position = state[['PRTNR_ID','FiscalWeekBeginDate', 'JOB_NM']]
last_position = last_position.groupby('PRTNR_ID').max().reset_index().drop(['FiscalWeekBeginDate'], axis=1)
last_position = last_position.rename(columns = {'JOB_NM':'last_position'})

# Collect the cols 'PRTNR_ID','FiscalWeekBeginDate', 'FSCL_WK_END_DT_JOB_TNUR' from the original dataset
FSCL_WK_END_DT_COM_TNUR = state[['PRTNR_ID','FiscalWeekBeginDate', 'FSCL_WK_END_DT_COM_TNUR','PRTNR_ACTIVE_FLG']]

#Employee whose last active flg = 0
FSCL_WK_END_DT_COM_TNUR_0 = FSCL_WK_END_DT_COM_TNUR[FSCL_WK_END_DT_COM_TNUR['PRTNR_ACTIVE_FLG'] == 0]
FSCL_WK_END_DT_COM_TNUR_0 =  FSCL_WK_END_DT_COM_TNUR_0.groupby(['PRTNR_ID','FSCL_WK_END_DT_COM_TNUR','PRTNR_ACTIVE_FLG'])['FiscalWeekBeginDate'].agg('min')
FSCL_WK_END_DT_COM_TNUR_0 = pd.DataFrame(FSCL_WK_END_DT_COM_TNUR_0).reset_index()

#Employee whose last active flg = 1
FSCL_WK_END_DT_COM_TNUR = state[['PRTNR_ID','FiscalWeekBeginDate', 'FSCL_WK_END_DT_COM_TNUR','PRTNR_ACTIVE_FLG']]
FSCL_WK_END_DT_COM_TNUR_1 = FSCL_WK_END_DT_COM_TNUR[FSCL_WK_END_DT_COM_TNUR['PRTNR_ACTIVE_FLG'] == 1]
FSCL_WK_END_DT_COM_TNUR_1 =  FSCL_WK_END_DT_COM_TNUR_1.groupby(['PRTNR_ID'])['FSCL_WK_END_DT_COM_TNUR','FiscalWeekBeginDate','PRTNR_ACTIVE_FLG'].agg('max')
FSCL_WK_END_DT_COM_TNUR_1 = pd.DataFrame(FSCL_WK_END_DT_COM_TNUR_1).reset_index()
# #drop the partners row whose active stats is always 0
to_drop = FSCL_WK_END_DT_COM_TNUR_0['PRTNR_ID']
FSCL_WK_END_DT_COM_TNUR_1['PRTNR_ID'] = FSCL_WK_END_DT_COM_TNUR_1[~FSCL_WK_END_DT_COM_TNUR_1['PRTNR_ID'].isin(to_drop)]
FSCL_WK_END_DT_COM_TNUR_1=FSCL_WK_END_DT_COM_TNUR_1.dropna()
print(FSCL_WK_END_DT_COM_TNUR_1)

#concat FSCL_WK_END_DT_COM_TNUR_0 and FSCL_WK_END_DT_COM_TNUR_1
FSCL_WK_END_DT_COM_TNUR =pd.concat([FSCL_WK_END_DT_COM_TNUR_0,FSCL_WK_END_DT_COM_TNUR_1], axis=0)
FSCL_WK_END_DT_COM_TNUR['Last_Month_Year'] = pd.to_datetime(FSCL_WK_END_DT_COM_TNUR['FiscalWeekBeginDate']).dt.to_period('M')
FSCL_WK_END_DT_COM_TNUR = FSCL_WK_END_DT_COM_TNUR.rename(columns = {'FiscalWeekBeginDate' : 'Last_FiscalWeekBeginDate',
                                                                   'FSCL_WK_END_DT_COM_TNUR': 'Last_FSCL_WK_END_DT_COM_TNUR'})

#the longest position holding period                                                               
the_longest_position_holding_period = state[['PRTNR_ID','FiscalWeekBeginDate', 'FSCL_WK_END_DT_JOB_TNUR']]
the_longest_position_holding_period = pd.merge(FSCL_WK_END_DT_COM_TNUR,the_longest_position_holding_period, how ='inner',
                                              left_on = ['PRTNR_ID','Last_FiscalWeekBeginDate'],
                                                         right_on = ['PRTNR_ID','FiscalWeekBeginDate']).drop_duplicates()

the_longest_position_holding_period = the_longest_position_holding_period.drop(['Last_FSCL_WK_END_DT_COM_TNUR', 'PRTNR_ACTIVE_FLG',
                                                                               'Last_FiscalWeekBeginDate',
                                                                               'Last_Month_Year','FiscalWeekBeginDate'], axis=1) 
the_longest_position_holding_period = the_longest_position_holding_period.rename(columns = {'FSCL_WK_END_DT_JOB_TNUR' : 'longest_position_holding_period'})

#generation group
generation = state[['PRTNR_ID','GEN_GRP_CD']].drop_duplicates()

#Average count_of_prtnrs by Quarter and Branch to calculate labor density
# Collect the cols 'PRTNR_ID','FiscalWeekBeginDate','PRTNR_ACTIVE_FLG','count_of_prtnrs' from the original dataset
count_of_prtnrs = state

#convert y-m-d to y-m
count_of_prtnrs['Month_Year']= pd.to_datetime(count_of_prtnrs['FiscalWeekBeginDate']).dt.to_period('M')
count_of_prtnrs['Qtr']= pd.to_datetime(count_of_prtnrs['FiscalWeekBeginDate']).dt.to_period('Q')

#Calculate Average Qtr by branch
Qtr_avg= round( pd.DataFrame(count_of_prtnrs.groupby(['Qtr','hashedstorenumber'])['count_of_prtnrs'].mean()).reset_index(),0)
Qtr_avg = Qtr_avg.rename(columns={'count_of_prtnrs' : 'Qtr_avg_count_of_prtnrs'})

#If 'Count of partners on employee's active week' < 'Qtr_avg_count_of_prtnrs', 'Labor Density = 1'
#Merge to count_of_prtnrs data-frame
count_of_prtnrs = pd.merge(count_of_prtnrs, Qtr_avg, how = 'left', left_on = ['Qtr','hashedstorenumber'],
                           right_on = ['Qtr','hashedstorenumber'])

count_of_prtnrs["labor density"] = [ 1 if x < y and z == 1 else 0 for x, y, z in zip(count_of_prtnrs["count_of_prtnrs"],
                                                                    count_of_prtnrs["Qtr_avg_count_of_prtnrs"],
                                                                                count_of_prtnrs["PRTNR_ACTIVE_FLG"])]

#labor density
labor_density = pd.DataFrame(count_of_prtnrs.groupby(['PRTNR_ID'])['labor density'].sum()).reset_index()

#'STATE_CODE','CITY_NAME', 'primary_venue', 'urbanity','store_type', 'hashedstorenumber'
# Collect the cols 'PRTNR_ID',STATE_CODE','CITY_NAME', 'primary_venue', 'urbanity','store_type', 'hashedstorenumber' from the original dataset
general = state[['PRTNR_ID','FiscalWeekBeginDate','STATE_CODE','CITY_NAME','urbanity','store_type', 'hashedstorenumber']].drop_duplicates()
general1 = general.groupby(['PRTNR_ID'])['FiscalWeekBeginDate'].max()
general2 = general[['PRTNR_ID','FiscalWeekBeginDate','STATE_CODE','CITY_NAME', 'urbanity','store_type', 'hashedstorenumber']]
general1 = pd.merge(general1,general2, how = 'left', left_on = ['PRTNR_ID','FiscalWeekBeginDate'] ,
                        right_on = ['PRTNR_ID','FiscalWeekBeginDate']).drop(['FiscalWeekBeginDate'], axis=1)

# benefitselig & benefitsused
# Collect the cols 'PRTNR_ID',STATE_CODE','CITY_NAME', 'primary_venue', 'urbanity','store_type',
benefit =state[['PRTNR_ID', 'FiscalWeekBeginDate', 'PRTNR_ACTIVE_FLG','benefitselig', 'benefitsused']] 
benefit = benefit.sort_values(by="FiscalWeekBeginDate")

#Find partners whose active flg is 0 and remain only the first 0
benefit_0 = benefit[benefit['PRTNR_ACTIVE_FLG']==0]
benefit_first_0 = pd.DataFrame(benefit_0.groupby(['PRTNR_ID'])['FiscalWeekBeginDate','PRTNR_ACTIVE_FLG','benefitselig','benefitsused'].agg('first')).reset_index()

benefit_second_0 = pd.merge(benefit_0, benefit_first_0, on=['PRTNR_ID','FiscalWeekBeginDate'],how='left', indicator=True).query("_merge=='left_only'").drop('_merge', 1)
benefit_second_0 = benefit_second_0.drop(['PRTNR_ACTIVE_FLG_y','benefitselig_y','benefitsused_y'], axis=1)
benefit_second_0 = benefit_second_0.rename(columns={'PRTNR_ACTIVE_FLG_x':'PRTNR_ACTIVE_FLG',
                                                   'benefitselig_x':'benefitselig',
                                                   'benefitsused_x':'benefitsused'})

benefit = pd.merge(benefit, benefit_second_0, on=['PRTNR_ID','FiscalWeekBeginDate'],how='left', indicator=True).query("_merge=='left_only'").drop('_merge', 1)
benefit = benefit.drop(['PRTNR_ACTIVE_FLG_y','benefitselig_y','benefitsused_y'], axis=1)
benefit = benefit.rename(columns={'PRTNR_ACTIVE_FLG_x':'PRTNR_ACTIVE_FLG',
                                                   'benefitselig_x':'benefitselig',
                                                   'benefitsused_x':'benefitsused'})

# Convert True and False to 1 and 0
benefit['benefitselig'].replace({False: 0, True: 1}, inplace=True)
benefit['benefitsused'].replace({False: 0, True: 1}, inplace=True)

# aggregate in a line for each 'PRTNR_ID'
benefitselig_sum= benefit.groupby(['PRTNR_ID'])['benefitselig'].sum().reset_index().round()
benefitsused_sum = benefit.groupby(['PRTNR_ID'])['benefitsused'].sum().reset_index()

#Obtaining pctpay
state['FSCL_WK_END_DT_JOB_TNUR'] = round(state['FSCL_WK_END_DT_JOB_TNUR']/365,6)
pctpay_min = state[['PRTNR_ID','FiscalWeekBeginDate','FSCL_WK_END_DT_JOB_TNUR' ,'pctpay','pulse']].groupby(['PRTNR_ID'])['FiscalWeekBeginDate','FSCL_WK_END_DT_JOB_TNUR','pctpay','pulse'].min().reset_index().drop(['FiscalWeekBeginDate','pulse'], axis=1)
pctpay_max = state[['PRTNR_ID','FiscalWeekBeginDate', 'FSCL_WK_END_DT_JOB_TNUR','pctpay','pulse']].groupby(['PRTNR_ID'])['FiscalWeekBeginDate','FSCL_WK_END_DT_JOB_TNUR' ,'pctpay','pulse'].max().reset_index().drop(['FiscalWeekBeginDate','pulse'], axis=1)

pctpay_max = pctpay_max.rename(columns={'FSCL_WK_END_DT_JOB_TNUR':'MAX_FSCL_WK_END_DT_JOB_TNUR',
                                        'pctpay':'max_pctpay'})
pctpay_min = pctpay_min.rename(columns={'FSCL_WK_END_DT_JOB_TNUR':'MIN_FSCL_WK_END_DT_JOB_TNUR',
                                        'pctpay':'min_pctpay'})

pctpay_min_max = pctpay_min.merge(pctpay_max, how='left', on='PRTNR_ID')

pctpay_min_max['max-min_tnur'] = round((pctpay_min_max['MAX_FSCL_WK_END_DT_JOB_TNUR'] - pctpay_min_max['MIN_FSCL_WK_END_DT_JOB_TNUR'])/365,6)
pctpay_min_max['max-min_pctpay'] = pctpay_min_max['max_pctpay'] - pctpay_min_max['min_pctpay']

pctpay_min_max['anual_average_Wage_increase'] = round(pctpay_min_max['max-min_tnur']/pctpay_min_max['max-min_pctpay'],4)*100
pctpay_min_max = pctpay_min_max.drop(['MAX_FSCL_WK_END_DT_JOB_TNUR','max-min_tnur','max-min_pctpay'],axis =1)

# Create a new data-frame
# # Merge the data-frame
new_df = earliest_FiscalWeekBeginDate.merge(the_number_of_jobs, how='inner', on='PRTNR_ID')
new_df = new_df.merge(last_position, how='inner', on='PRTNR_ID')
new_df = new_df.merge(FSCL_WK_END_DT_COM_TNUR, how='inner', on='PRTNR_ID')
new_df = new_df.merge(the_longest_position_holding_period, how='inner', on='PRTNR_ID')
new_df = new_df.merge(generation, how='inner', on='PRTNR_ID')
new_df = new_df.merge(labor_density, how='inner', on='PRTNR_ID')
new_df = new_df.merge(general1, how='inner', on='PRTNR_ID')
new_df = new_df.merge(benefitselig_sum, how='inner', on='PRTNR_ID')
new_df = new_df.merge(benefitsused_sum, how='inner', on='PRTNR_ID')
new_df = new_df.merge(pctpay_min_max, how='inner', on='PRTNR_ID').replace([np.inf, -np.inf], 0).dropna()

#Job Position Changed
new_df["Job Position Changed"] = [ 1 if x > y else 0 for x, y in zip(new_df["Last_FSCL_WK_END_DT_COM_TNUR"],
                                                                                   new_df["longest_position_holding_period"])]

#Fromating Columns
new_df['FiscalWeekBeginDate'] = pd.to_datetime(count_of_prtnrs['FiscalWeekBeginDate']).dt.to_period('M')
new_df['Last_FSCL_WK_END_DT_COM_TNUR'] = round(new_df['Last_FSCL_WK_END_DT_COM_TNUR']/365,2)
new_df['longest_position_holding_period'] = round(new_df['longest_position_holding_period']/365,2)
new_df[['MIN_FSCL_WK_END_DT_JOB_TNUR', 'min_pctpay','max_pctpay']] = round(new_df[['MIN_FSCL_WK_END_DT_JOB_TNUR', 'min_pctpay','max_pctpay']],2)
new_df = new_df.drop(['FiscalWeekBeginDate','count_position','Last_FiscalWeekBeginDate'], axis=1)
print(new_df)

print(list(new_df))

#Re-ordering Columns
new_df = new_df[['PRTNR_ID','Last_FSCL_WK_END_DT_COM_TNUR','MIN_FSCL_WK_END_DT_JOB_TNUR','longest_position_holding_period',
                 'last_position','Job Position Changed','labor density','PRTNR_ACTIVE_FLG', 'Last_Month_Year', 'GEN_GRP_CD',
                 'STATE_CODE','CITY_NAME','urbanity','store_type', 'hashedstorenumber', 'benefitselig','benefitsused',
                 'min_pctpay','max_pctpay','anual_average_Wage_increase'
                ]]

#Change cols' name
new_df = new_df.rename(columns = {'PRTNR_ID':'Prtnr_ID',
                                  'Last_FSCL_WK_END_DT_COM_TNUR': 'Tenure_Com',
                                  'MIN_FSCL_WK_END_DT_JOB_TNUR' :'Min_Tenure_Position',
                                  'longest_position_holding_period': 'Longest_Position',
                                  'last_position':'Last_Position',
                                  'Job Position Changed':'Job_changed',
                                  'labor density':'Labor_Density',
                                  'PRTNR_ACTIVE_FLG' :'Last_Active_Flg',
                                  'Last_Month_Year':'Last_Status_Month_Year',  
                                  'GEN_GRP_CD':'Gen',
                                  'STATE_CODE': 'State',
                                  'CITY_NAME' : 'City',
                                  'urbanity':'Urbanity',
                                  'store_type':'Store_Type',
                                  'hashedstorenumber':'Store_Num',
                                  'benefitselig':'Benefit_Selling',
                                  'benefitsused': 'Benefit_Used',
                                  'min_pctpay':'Min_Pctpay',
                                  'max_pctpay':'Max_Pctpay',
                                  'anual_average_Wage_increase':'Yearly_Wage_Increase(%)'
                                 })

#Get Dummies
#Position dummies
position_dummy = pd.get_dummies(new_df['Last_Position'])
new_df= pd.concat([new_df,position_dummy], axis=1)

#GEN_GRP_CD dummies
gen_dummy = pd.get_dummies(new_df['Gen'])
new_df= pd.concat([new_df,gen_dummy], axis=1)

#state_code dummies
state_code_dummy = pd.get_dummies(new_df['State'])
new_df= pd.concat([new_df,state_code_dummy], axis=1)

#City dummies
city_dummy = pd.get_dummies(new_df['City'])
new_df= pd.concat([new_df,city_dummy], axis=1)

#Urbanity
u_dummy = pd.get_dummies(new_df['Urbanity'])
new_df = pd.concat([new_df,u_dummy], axis=1)

#Store_Type
store_type_dummy = pd.get_dummies(new_df['Store_Type'])
new_df= pd.concat([new_df,store_type_dummy], axis=1)
print(new_df)

#drop employees who quit the job several times
new_df =new_df.drop_duplicates()
duplicated = new_df[new_df['Prtnr_ID'].duplicated()]
duplicated = list(duplicated['Prtnr_ID'].drop_duplicates())

to_drop = duplicated
new_df = new_df[~new_df['Prtnr_ID'].isin(to_drop)]

#Export Data File to CSV
# # Export Data File to CSV
# new_df.to_csv("starbucks(12208)_FINAL.csv", index=None)