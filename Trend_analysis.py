import pandas as pd
import policy
import matplotlib.pyplot as plt

# load the dataset
dataframe = pd.read_excel('ROAM_OVERAGE.xlsx', sheet_name=['Read me','Revenue_Overage','Segment','Credits'],engine="openpyxl")

df_revenue_overage=dataframe['Revenue_Overage']
df_segment=dataframe['Segment']
df_credits=dataframe['Credits']

#Service_max_policy_credit = policy(overage), max_policy_credit is nearly proportional to overage

## clean data in revenue overage worksheet and calculate the max policy credit based on the policy function
df_revenue_overage=df_revenue_overage.fillna(0).drop(df_revenue_overage.columns[[-1,-2]],axis=1)
df_revenue_max_policy_credit=df_revenue_overage.copy()
df_revenue_max_policy_credit.iloc[:,3:]=df_revenue_max_policy_credit.iloc[:,3:].applymap(lambda x: policy.credit_Policy(x))

## rename the original column service names to abbreviated service names
dict={'VOICE_ROAM_USA_AIR_CHRG_AMT':'VRUACA','VOICE_ROAM_USA_LD_CHRG_AMT':'VRULCA',
      'VOICE_ROAM_INTL_AIR_CHRG_AMT':'VRIACA','VOICE_ROAM_INTL_LD_CHRG_AMT':'VRILCA','DATA_BILLED_AMT_CDA':'DBAC'
    ,'DATA_ROAM_AMT_USA':'DRAU','DATA_ROAM_AMT_INTL':'DRAI','SMS_TOTAL_AMOUNT':'STA','SMS_ROAM_AMOUNT':'SRA'}
df_revenue_max_policy_credit.rename(columns=dict,inplace=True)
df_revenue_overage.rename(columns=dict,inplace=True)

## Calculate the overage of each service and combined service each month (monthly trend)
df_month_revenue_overage=df_revenue_overage.groupby('CCYYMM')['VRUACA','VRULCA','VRIACA','VRILCA','DBAC','DRAU','DRAI','STA','SRA'].sum().reset_index()
df_month_revenue_overage['Total Overage']=df_month_revenue_overage.iloc[:,1:].sum(axis=1)


## Calculate the max policy credit of each service and combined service each month (monthly trend)
df_month_revenue_max_policy_credit=df_revenue_max_policy_credit.groupby('CCYYMM')['VRUACA','VRULCA','VRIACA','VRILCA','DBAC','DRAU','DRAI','STA','SRA'].sum().reset_index()
df_month_revenue_max_policy_credit['Total Max Policy Credit']=df_month_revenue_max_policy_credit.iloc[:,1:].sum(axis=1)

## Plot the max policy credits of the combined service vs. time (month trend)
time=list(df_month_revenue_max_policy_credit.loc[:,'CCYYMM']-201400)
max_policy_credits_combined=list(df_month_revenue_max_policy_credit.loc[:,'Total Max Policy Credit'])
plt.plot(time,max_policy_credits_combined)
plt.xlabel('Time (months)')
plt.ylabel('Max Policy Credit (dollars)')
plt.show()


#Service_real_credit

##1. dayly trend (pivot the table to transform)
df_date_code_group=df_credits.groupby(['ADJ_CREATION_DATE','ACTV_REASON_CODE'])['ACTV_AMT'].sum().reset_index()
df_daily_credit=df_date_code_group.pivot(index='ADJ_CREATION_DATE',columns='ACTV_REASON_CODE', values='ACTV_AMT').reset_index().fillna(0.0)
df_daily_credit=df_daily_credit.rename_axis(None, axis=1) # remove the axis name after the pivot

##2. monthly trend
df_daily_credit['MM']=df_daily_credit['ADJ_CREATION_DATE'].dt.strftime('%m')
df_month_credit=df_daily_credit.iloc[:,1:].groupby('MM').sum().reset_index()
df_month_credit['Total Credit']=df_month_credit.iloc[:,1:].sum(axis=1)

## output
print('The table for monthly overage is:\n{}\n\n'.format(df_month_revenue_overage))

print('The table for monthly max policy credit is:\n{}\nThe relationship between '
      'overage and max policy credit is: max policy credit = '
      'policy(overage). \nThe max policy credit can offer more information when '
      'it is compared with real credit return. \nrevenue leakage = real credit '
      'return - max policy credit\n\n'.format(df_month_revenue_max_policy_credit))

print('The table for daily real credit return is:\n{}\n\n'.format(df_daily_credit))

print('The table for monthly real credit return is:\n{}\n'.format(df_month_credit))