import pandas as pd
import numpy as np
import pickle
import gib_detect_train

df = pd.read_csv("orig-data.csv")
model_data = pickle.load(open('../private/gib_model.pki', 'rb'))
model_mat = model_data['mat']
gib_score = lambda x : gib_detect_train.avg_transition_prob(x, model_mat)

df['name_len'] = df['display_name'].map(lambda x : len(x))

df['name_gibberish_score'] = df['display_name'].map(gib_score)

def vowel_ratio(x):
    count = 0
    for c in x.lower():
        if c in ['a', 'e', 'i', 'o', 'u']:
            count=count+1
    return float(count)/float(len(x))

df['name_vowel_ratio'] = df['display_name'].apply(vowel_ratio)

import datetime

def get_day_of_week(x):
    date_str = x[:10]
    datetime_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return datetime_obj.weekday()


df['day_of_week'] = df['receive_date'].apply(get_day_of_week)

def get_time_of_day(x):
    time_str = x[-8:-6] + x[-5:-3]
    return int(time_str)

df['time_of_day'] = df['receive_date'].apply(get_time_of_day)

df = df.drop(['id', 'receive_date', 'user_ip', 'display_name', 'server'], axis=1)

def is_nan(x):
    return int(np.isnan(x))

df['utm_filter_isnan'] = df['utm_filter'].apply(is_nan)
df['avs_filter_isnan'] = df['avs_filter'].apply(is_nan)
df['email_domain_filter_isnan'] = df['email_domain_filter'].apply(is_nan)
df['ip_filter_isnan'] = df['ip_filter'].apply(is_nan)
df['cvv_filter_isnan'] = df['cvv_filter'].apply(is_nan)
df['country_filter_isnan'] = df['country_filter'].apply(is_nan)
df['minfraud_filter_isnan'] = df['minfraud_filter'].apply(is_nan)

def impute_filter_values(x):
    if np.isnan(x):
        return 0
    else:
        return x

df['utm_filter'] = df['utm_filter'].apply(impute_filter_values)
df['avs_filter'] = df['avs_filter'].apply(impute_filter_values)
df['email_domain_filter'] = df['email_domain_filter'].apply(impute_filter_values)
df['ip_filter'] = df['ip_filter'].apply(impute_filter_values)
df['cvv_filter'] = df['cvv_filter'].apply(impute_filter_values)
df['country_filter'] = df['country_filter'].apply(impute_filter_values)
df['minfraud_filter'] = df['minfraud_filter'].apply(impute_filter_values)

# in case we want to one-hot encode
# df_categorical = pd.get_dummies(df[['financial_type_id', 'payment_instrument_id', 'currency', 'gateway', 'payment_method', 'country'
#                                   , 'utm_medium', 'utm_campaign']], dummy_na=True)


cat_cols = ['financial_type_id', 'payment_instrument_id', 'currency', 'gateway', 'payment_method', 'country'
                                   , 'utm_medium', 'utm_campaign']
label_mapping = {}
for c in cat_cols:
    df[c], label_mapping[c] = pd.factorize(df[c])
cols = list(df)
cols.insert(0, cols.pop(cols.index('label')))
df = df.loc[:, cols]

df.to_csv('data-eng.csv')
pickle.dump(label_mapping, open('../private/data-mappings.pkl', 'w'))

