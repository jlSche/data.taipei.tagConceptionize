# encoding=utf8
import json
import codecs
import pandas as pd
from  collections import defaultdict


df = pd.read_csv('./input.csv', encoding='big5')

df = df.drop_duplicates(subset='fieldDescription', take_last=True)
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


def createTag(tag_name='geo', tag_defs=geo_def_list):
  for tag in tag_defs:
    fields = field_dataset_dict.keys()
    for field in fields:
      if tag in field:
        print 'field_dataset match'
        for val in field_dataset_dict[field]:
          tag_dataset_dict[tag_name].append(val)

  for field in field_dataset_dict:
    if field in tag_defs:
      tag_field_dict[tag_name].append(field.encode('big5'))
      #field_tag_dict[field].append(tag_name)
      print 'tag_field match', field
    else:
      field_dict[field].append('nan')

createTag('geo', geo_def_list)
createTag('price', price_def_list)

def createJsonFormat(input_dict=field_dataset_dict):
  output = [] 
  for key, val in input_dict.items():
    output_dict = dict()
    output_dict["name"] = key
    output_dict["size"] = 1
    output_dict["imports"] = val
    output.append(output_dict)
  return output

def printall(output, str1, str2):
  for obj in output:
    f.write('{')
    for key, val in obj.items():
      f.write('\"'+key+'\":')
      if type(val) is list:
        f.write('[')
        for idx in range(0, len(val)-1):
          try:
            f.write(str2)
            f.write(val[idx].decode('big5'))
            f.write('>\",')
          except:
            #print val[idx].decode('utf8')
            print '2', type(val[idx]),
        f.write(str2)
        f.write(val[len(val)-1].decode('big5'))
        f.write('>\"')
        f.write('],')

      elif type(val) is int:
        f.write(str(val).decode('utf8')+'},\n')
      elif isinstance(val, unicode):
        try:
          f.write(str1)
          f.write(val)
          f.write('>\",')
        except:
          print 'not work'
      else:
          print 'in elese2'
          f.write(str1)
          f.write(val)
          f.write('>\",')


def printsome(output, str1):
  for obj in output:
    f.write('{')
    for key, val in obj.items():
      f.write('\"'+key+'\":')
      if type(val) is list:
        f.write('[],')
      elif type(val) is int:
        f.write(str(val).decode('utf8')+'},\n')
      elif isinstance(val, unicode):
        try:
          f.write(str1)
          f.write(val)
          f.write('>\",')
        except:
          print 'not work'
      else:
          #print 'in elese1'
          f.write(str1)
          f.write(val.decode('big5'))
          #if isinstance(val, str):
          #  print str(val)
          
          f.write('>\",')


def createNetwork():
  for key, val_list in field_dataset_dict.items():
    for val in val_list:
      dataset_dict[val].append('nan')

  for key, val_list in tag_field_dict.items():
    for val in val_list:
      field_dict[val].append('nan')
      '''
      if val not in tag_dataset_dict:
        tag_dict[val].append('nan')
      '''
  for key, val_list in tag_dataset_dict.items():
    for val in val_list:
      dataset_dict[val].append('nan')

dataset = [field_dataset_dict, tag_field_dict, tag_dataset_dict, tag_dict, dataset_dict, field_dict]
f = codecs.open('./readme-flare-imports.json', 'w',encoding='utf8')
f.write('[')
for idx in range(0, len(dataset)):
  createNetwork()
  output = createJsonFormat(dataset[idx])
  if idx == 0:
    print 'len0', len(output)
    printall(output, '\"flare.attri.<', '\"flare.data.<')
  '''
  elif idx == 1:
    print 'len1', len(output)
    printall(output, '\"flare.usertag.<', '\"flare.attri.<')
  '''
  if idx == 2:
    print 'len2', len(output)
    printall(output, '\"flare.usertag.<', '\"flare.data.<')
  
  elif idx == 3:
    print 'len3', len(output)
    printsome(output, '\"flare.usertag.<')
  elif idx == 4:
    print 'len4', len(output)
    printsome(output, '\"flare.data.<')
  elif idx == 5:
    print 'len5', len(output)
    printsome(output, '\"flare.attri.<')
f.write(']')

f.close()
