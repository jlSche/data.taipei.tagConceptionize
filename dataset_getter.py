# encoding=utf8
import json
import codecs
import pandas as pd
import sys
from  collections import defaultdict

df = pd.read_csv('./input.csv', encoding='big5')

df = df.drop_duplicates(subset='fieldDescription', take_last=True)
df = df[(df['category']==u'求學及進修') | (df['category']==u'交通及通訊') | (df['category']==u'生活安全及品質') | (df['category']==u'就醫') | (df['category']==u'休閒旅遊')]

def matchAttri(tag_defs):
  #counter = 0
  for idx, row in df.iterrows():          # iterate all datasets
    try:
      field_description = row['fieldDescription'].encode('big5')
      field_description = field_description.replace(', ', '`')
      field_description = field_description.replace(',', '`')
      field_description = field_description.replace('\r', '')
      field_description = field_description.replace('\n', '')
      field_description = field_description.replace('，', '`')
      field_description = field_description.replace('、 ', '`')
      field_description = field_description.replace('、', '`')
      field_description = field_description.replace(' ', '`')
      field_description = field_description.replace(' ', '`')

    except:
      print 'error when encode row to big5'
    
    split_result = field_description.split('`')
    for field in split_result:            # iterate all attribute in a dataset
      for tag in tag_defs:
        # tag is now unicode, encode('utf8')
        # field is now string  encode('utf8') or decode('big5')
        
        try:
          if tag in field.decode('big5'):
            #counter += 1
            f.write(row['title'])
            f.write(',')
            f.write(row['data_link'])
            f.write(',')
            f.write(field.decode('big5'))
            f.write('\n')
        except:
          print 'error'
  #print counter, 'attributes matched'
##########################################

geo_def_list = [u'緯度',u'經度',u'經緯度',u'地址',u'區域',u'座標',u'位置','lat','latitude','Lat','Latitude','lng','longitude','Lng','Longitude']
price_def_list = [u'價錢',u'權利金',u'利息',u'費用',u'收入']
  
##########################################
f_r = codecs.open('./wish_list', 'r', encoding='utf8')
input_str = f_r.read()
wish_list = [ele for ele in input_str.split(',')]
for ele in wish_list:
  print ele.encode('utf8'),
print '\n'

#'''
f = codecs.open('./tagMatchingResult.csv', 'w', encoding='utf8')
f.write('dataset_title,dataset_link,attri_matched\n')
matchAttri(wish_list)
f.close()

temp_df = pd.read_csv('./tagMatchingResult.csv')
temp_df = temp_df.drop_duplicates()
temp_df.to_csv('./tagMatchingResult.csv',index=False)
#'''


