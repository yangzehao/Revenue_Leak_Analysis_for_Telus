import pandas as pd
import numpy as np
# load the dataset
dataframe = pd.read_excel('ROAM_OVERAGE.xlsx', sheet_name=['Read me','Revenue_Overage','Segment','Credits'],engine="openpyxl")

df_revenue_overage=dataframe['Revenue_Overage']
df_segment=dataframe['Segment']
df_credits=dataframe['Credits']

overage_phone=set(df_revenue_overage['MOBILE_PHONE_NO'])
credit_phone=set(df_credits['MOBILE_PHONE_NO'])

# mobile numbers only in overage table not in credit table and only in credit table not in overage table
overage_phone_unique=overage_phone-(overage_phone&credit_phone)
print('The mobile numbers ({}) only in overage table not in credit table '
      'are:\n{}\n\n'.format(len(overage_phone_unique),overage_phone_unique))
credit_phone_unique=credit_phone-(overage_phone&credit_phone)
print('The mobile numbers ({}) only in credit table not in overage table '
      'are:\n{}\n\n'.format(len(credit_phone_unique),credit_phone_unique))

# mobile numbers corresponding to several account numbers
table_overage_groupby_AN_MP=df_revenue_overage.loc[:,['ACCOUNT_NUMBER','MOBILE_PHONE_NO']].drop_duplicates()
u,c=np.unique(table_overage_groupby_AN_MP['MOBILE_PHONE_NO'].to_numpy(),return_counts=True)
phone_number_to_multiple_accounts=u[c>1]
print('The mobile numbers ({}) corresponding to multiple accounts '
      'are:\n{}\n\n'.format(len(phone_number_to_multiple_accounts),phone_number_to_multiple_accounts))

# account numbers corresponding to several mobile numbers
u,c=np.unique(table_overage_groupby_AN_MP['ACCOUNT_NUMBER'].to_numpy(),return_counts=True)
account_number_to_multiple_phones=u[c>1]
print('The account numbers ({}) corresponding to multiple moible numbers '
      'are:\n{}\n\n'.format(len(account_number_to_multiple_phones),account_number_to_multiple_phones))

# mobile numbers corresponding to several account numbers and belonging to different segments
table_mobile_rpt=pd.merge(table_overage_groupby_AN_MP,df_segment,on='ACCOUNT_NUMBER',how='inner').loc[:,['MOBILE_PHONE_NO','RPT_SVP']].drop_duplicates()
u,c=np.unique(table_mobile_rpt['MOBILE_PHONE_NO'].to_numpy(),return_counts=True)
phone_number_to_multiple_accounts_ms=u[c>1]
print('The mobile numbers ({}) corresponding to multiple accounts and belonging to different segments '
      'are:\n{}\n\n'.format(len(phone_number_to_multiple_accounts_ms),phone_number_to_multiple_accounts_ms))



