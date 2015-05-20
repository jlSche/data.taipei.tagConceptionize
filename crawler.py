import urllib
import datetime
import time
import os


NUM_OF_DATASET = 1340

currenttime = datetime.datetime.now()
#filename = str(currenttime.hour)+str(currenttime.minute)+'.csv'
filename = 'metadata_'

search_scale = 10
for idx in range(1290, NUM_OF_DATASET, search_scale):
  print 'idx: ', idx
  content = urllib.urlretrieve('http://data.taipei/opendata/datalist/apiAccess?scope=resourceMetadataSearch&limit='+str(search_scale)+'&offset='+str(idx), filename+str(idx))



