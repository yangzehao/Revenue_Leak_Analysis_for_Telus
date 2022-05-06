import pandas as pd
import policy
import numpy as np

# load the dataset
dataframe = pd.read_excel('ROAM_OVERAGE.xlsx', sheet_name=['Read me','Revenue_Overage','Segment','Credits'],engine="openpyxl")

df_revenue_overage=dataframe['Revenue_Overage']
df_segment=dataframe['Segment']
df_credits=dataframe['Credits']

# clean data in revenue overage worksheet and calculate the maximum policy credit. The maximum policy credit
# is the largest allowed credit without generating the leakage. It is equal to policy(overage). policy is
# the policy module, which is a function
df_revenue_max_policy_credit=df_revenue_overage.fillna(0).drop(df_revenue_overage.columns[[-1,-2]],axis=1)
df_revenue_max_policy_credit['Max_Policy_Credit']=df_revenue_max_policy_credit.iloc[:,3:].applymap(lambda x: policy.credit_Policy(x)).sum(axis=1)

# join relational tables to put the max policy credit, real credit and segments into one table, and the account
# number is the primary key for the final table

## group revenue table using "account number" and merge with segment table to get merge1 table
df_revenue_max_policy_credit_grouped=df_revenue_max_policy_credit.groupby('ACCOUNT_NUMBER')['Max_Policy_Credit'].sum().reset_index()
table_account_segment=pd.merge(df_segment,df_revenue_max_policy_credit_grouped,on='ACCOUNT_NUMBER',how='outer')

## group credit table using "mobile_phone_no"
df_credit_grouped=df_credits.groupby('MOBILE_PHONE_NO')['ACTV_AMT'].sum().reset_index()

## group revenue table using 'ACCOUNT_NUMBER' and 'MOBILE_PHONE_NO'
df_revenue_max_policy_credit_grouped2=df_revenue_max_policy_credit.loc[:,['ACCOUNT_NUMBER','MOBILE_PHONE_NO']].drop_duplicates()

## merge credit table and revenue table and group the new table (merge2) uisng "account number"
table_account_credit=pd.merge(df_credit_grouped,df_revenue_max_policy_credit_grouped2,on='MOBILE_PHONE_NO',how='outer')
bool_mobile_duplicated=table_account_credit.loc[:,'MOBILE_PHONE_NO'].duplicated(keep='first')
account_repeated_index=table_account_credit[bool_mobile_duplicated].index.values
table_account_credit.loc[account_repeated_index,"ACTV_AMT"]=0
## using the analyzed results in the data_initial_analysis module, deal with the phone number to several account number
phone_number_oneToMany=[1234573570, 1234580271, 1234584022, 1234584602, 1234586598,1234586874]
phone_number_oneToMany_ACTV_AMT_sum=table_account_credit[np.isin(table_account_credit['MOBILE_PHONE_NO'],phone_number_oneToMany)]['ACTV_AMT'].sum()
table_account_credit.loc[np.isin(table_account_credit['MOBILE_PHONE_NO'],phone_number_oneToMany),'ACTV_AMT']=0
table_account_credit_grouped=table_account_credit.fillna(0).groupby('ACCOUNT_NUMBER')['ACTV_AMT'].sum().reset_index()

## merge the merge1 table and merge2 table to get the final table containing credit, max policy credit and
## segments. Leakage = real credit return - max policy credit. max policy credit = policy(overage)
table_max_policy_credit_credit=pd.merge(table_account_segment,table_account_credit_grouped,on='ACCOUNT_NUMBER',how='outer')

# calculate the leakage for each segment
table_max_policy_credit_credit.loc[table_max_policy_credit_credit['ACCOUNT_NUMBER']==0,'ACTV_AMT']+=phone_number_oneToMany_ACTV_AMT_sum
leakage_total=table_max_policy_credit_credit.loc[:,'ACTV_AMT'].sum()-table_max_policy_credit_credit.loc[:,'Max_Policy_Credit'].sum()
leakage_small_bus_soln=table_max_policy_credit_credit.loc[table_max_policy_credit_credit['RPT_SVP']=='SMALL BUS SOLN','ACTV_AMT'].sum()-table_max_policy_credit_credit.loc[table_max_policy_credit_credit['RPT_SVP']=='SMALL BUS SOLN','Max_Policy_Credit'].sum()
leakage_telus_bus_soln=table_max_policy_credit_credit.loc[table_max_policy_credit_credit['RPT_SVP']=='TELUS BUS SOLN','ACTV_AMT'].sum()-table_max_policy_credit_credit.loc[table_max_policy_credit_credit['RPT_SVP']=='TELUS BUS SOLN','Max_Policy_Credit'].sum()
leakage_ent_soln=table_max_policy_credit_credit.loc[table_max_policy_credit_credit['RPT_SVP']=='ENT SOLN','ACTV_AMT'].sum()-table_max_policy_credit_credit.loc[table_max_policy_credit_credit['RPT_SVP']=='ENT SOLN','Max_Policy_Credit'].sum()
leakage_tq_ent_soln=table_max_policy_credit_credit.loc[table_max_policy_credit_credit['RPT_SVP']=='TQ - ENT SOLN','ACTV_AMT'].sum()-table_max_policy_credit_credit.loc[table_max_policy_credit_credit['RPT_SVP']=='TQ - ENT SOLN','Max_Policy_Credit'].sum()
leakage_tq_smb_soln=table_max_policy_credit_credit.loc[table_max_policy_credit_credit['RPT_SVP']=='TQ - SMB SOLN','ACTV_AMT'].sum()-table_max_policy_credit_credit.loc[table_max_policy_credit_credit['RPT_SVP']=='TQ - SMB SOLN','Max_Policy_Credit'].sum()
leakage_unknown=table_max_policy_credit_credit.loc[table_max_policy_credit_credit['RPT_SVP'].isna(),'ACTV_AMT'].sum()

# output. The unknown segment has been discussed in my report (initial analysis section)
print('The final joined relational table is: \n{}\nThe account number "0" means the unknown segment source. In the unknown '
      'segment, the corresponding mobile numbers in Credits table do not correspond to any accounts or '
      'segments. \nThe report has more detailed explanation.'.format(table_max_policy_credit_credit))
print('The leakage for all segments are: {} dollars.\n'.format(leakage_total))
print('The leakage for SMALL BUS SOLN segment is: {} dollars.\n'.format(leakage_small_bus_soln))
print('The leakage for TELUS BUS SOLN segment is: {} dollars.\n'.format(leakage_telus_bus_soln))
print('The leakage for ENT SOLN segment is: {} dollars.\n'.format(leakage_ent_soln))
print('The leakage for TQ - ENT SOLN segment is: {} dollars, and it means there is no leakage for this segment.\n'.format(leakage_tq_ent_soln))
print('The leakage for TQ - SMB SOLN segment is: {} dollars.\n'.format(leakage_tq_smb_soln))
print('The leakage for Unknown segment is: {} dollars.\n'.format(leakage_unknown))



