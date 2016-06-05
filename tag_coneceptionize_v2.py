# encoding=utf8
import json
import codecs
import csv
import pandas as pd
from  collections import defaultdict


df = pd.read_csv('./input.csv', encoding='big5')

df = df.drop_duplicates(subset='fieldDescription', keep='last')
df = df[(df['category']==u'求學及進修') | (df['category']==u'交通及通訊') | (df['category']==u'生活安全及品質') | (df['category']==u'就醫') | (df['category']==u'休閒旅遊')]
#df = df[df['category']==u'生活安全及品質']
description = df['fieldDescription']

# create dictionary
field_dataset_dict = defaultdict(list)    # field name -> dataset name
tag_field_dict = defaultdict(list)        # field name -> tag name
tag_dataset_dict = defaultdict(list)      # tag name   -> dataset name
tag_dict = defaultdict(list)
dataset_dict = defaultdict(list)
field_dict = defaultdict(list)

for idx, row in df.iterrows(): 
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
  
  try:
    split_result = field_description.split(u'`'.encode('big5'))
    for field in split_result:
      try:
        dataset_name = row['title'].encode('big5')
        field = field.decode('big5')
        #field_dataset_dict[field].append(dataset_name.decode('big5'))
        field_dataset_dict[field].append(dataset_name)
      except:
        print '\t\t\t\ttag:', type(field), field

  except SyntaxError:
    print 'SyntaxError:', row['title']

  except AttributeError:
    print 'AttributeError:', row['title']

  except UnicodeEncodeError:
    print 'UnicodeEncodeError:', row['title']


##########################################

geo_def_list = [u'緯度',u'經度',u'經緯度',u'地址',u'區域',u'座標',u'位置']
price_def_list = [u'價錢',u'權利金',u'利息',u'費用',u'收入']
  
##########################################


#field_dataset_dict[field].append(dataset_name.decode('big5'))
#field_dataset_df = pd.DataFrame(field_dataset_dict.items())
#field_dataset_df.to_csv('field_dataset.csv', encoding='utf8')

def createTag(tag_name='geo', tag_defs=geo_def_list):
  for tag in tag_defs:
    fields = field_dataset_dict.keys()
    for field in fields:
      if tag in field:

        '''
        no doing 
        if tag in fields
          do somthing
        because the word of the tag may not match the word in the field exactly 
        '''

        #print 'field_dataset match'
        for val in field_dataset_dict[field]:
          tag_dataset_dict[tag_name].append(val)

  for field in field_dataset_dict:
    if field in tag_defs:
      tag_field_dict[tag_name].append(field)
      #tag_field_dict[tag_name].append(field.encode('big5'))
      #field_tag_dict[field].append(tag_name)
      #print 'tag_field match', field
    else:
      field_dict[field].append('nan')

createTag('geo', geo_def_list)
createTag('price', price_def_list)

#field_dataset_dict[field].append(dataset_name.decode('big5'))
#tag_dataset_df = pd.DataFrame(tag_dataset_dict.items(), columns=['tag','dataset'])
#tag_dataset_df.to_csv('tag_dataset.csv', encoding='utf8')
with open('tag_dataset.json', 'w') as fp:
  json.dump(tag_dataset_dict, fp, encoding='big5')

#tag_field_df = pd.DataFrame(tag_field_dict.items(), columns=['tag','field'])
#tag_field_df.to_csv('tag_field.csv', encoding='utf8')
with open('tag_field.json', 'w') as fp:
  json.dump(tag_field_dict, fp, encoding='utf8')

#for key in field_dataset_dict.keys():
#  print key.encode('utf8')
#print 'key of field_dataset_df:', field_dataset_dict.keys()
#print 'items of field_dataset_df:', field_dataset_dict.items()
#field_dataset_df = pd.DataFrame.from_dict(field_dataset_dict, orient='columns')
#field_dataset_df = pd.DataFrame(field_dataset_dict.items(), columns=['field','dataset'], header=False)
#field_dataset_df.to_csv('field_dataset.csv', encoding='utf8')

#s = pd.Series(field_dataset_dict, name='tttt')
#s.index_name = 'yyyyy'
#s.reset_index()
#s.to_csv('field_dataset.csv', encoding='utf8')
'''
# solution 1
import io
with io.open('field_dataset.json', 'w', encoding='utf-8') as fp:
  fp.write(json.dumps(field_dataset_dict, ensure_ascii=False))
'''

with open('field_dataset.json', 'w') as fp:
  json.dump(field_dataset_dict, fp, encoding='big5')

def createJsonFormat(input_dict=field_dataset_dict):
  output = [] 
  for key, val in input_dict.items():
    output_dict = dict()
    output_dict["name"] = key
    output_dict["size"] = 1
    output_dict["imports"] = val
    output.append(output_dict)
  return output
