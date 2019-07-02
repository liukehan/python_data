from os import path, makedirs
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import json
import requests
import shutil

def image_download(url, file_path):
    r = requests.get(url, stream=True)
    if r.status_code == 200: # if request is successful
        with open(file_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        
class street_view:
 
    def __init__(
    self,
    params,
    site_api='https://maps.googleapis.com/maps/api/streetview',
    site_metadata='https://maps.googleapis.com/maps/api/streetview/metadata'):
    
        # (params) Set default params
        defaults = {
          'size': '640x640'
        }
        for i in range(len(params)):
            for k in defaults:
                if k not in params[i]:
                    params[i][k] = defaults[k]
        self.params = params
    
        # (image) Create image api links from parameters
        self.links = [site_api + '?' + urlencode(p) for p in params]
    
        # (metadata) Create metadata api links and data from parameters
        self.metadata_links = [site_metadata + '?' + urlencode(p) for p in params]
        
        #create metadata
        self.metadata = [requests.get(url, stream=True).json() for url in self.metadata_links]
      
    def download_images(self, dir_path, image_name ='pic', metadata_file='metadata.json', metadata_status='status', status_ok='OK'):
        """Download Google Street View images from parameter queries if they are available.    
        Args:
          dir_path (str):
            Path of directory to save downloads of images from :class:`api.results`.links
          metadata_file (str):
             Name of the file with extension to save the :class:`api.results`.metadata
          metadata_status (str):
            Key name of the status value from :class:`api.results`.metadata response from the metadata API request.
          status_ok (str):
            Value from the metadata API response status indicating that an image is available.
        """
        metadata = self.metadata
        if not path.isdir(dir_path):
            makedirs(dir_path)
    
        # (download) Download images if status is ok
        for i, url in enumerate(self.links):
            if metadata[i][metadata_status] == status_ok:
                if i == 0:
                    file_path = path.join(dir_path, 'google_street_view_' + image_name + '.jpg')
                else:
                    file_path = path.join(dir_path, 'google_street_view_' + image_name + str(i+1) + '.jpg')
                metadata[i]['_file'] = path.basename(file_path) # add file reference
                image_download(url, file_path)

                
#Search Image
import pandas as pd
data = pd.read_csv('D:\\Clients\\Cincinnati Financial\\input 5 02052019\\INPUT FILE - google.csv', encoding = 'utf-8')
data['add'] = data['LOC_STREET1'] + ", " + data['LOC_CITY'] + ", " + data["LOC_STATE"] + ", " + data['COUNTRY']
for i in range(3):
    params = [{
	'size': '600x300', # max 640x640 pixels
	'location': str(data.iloc[i,:]['add']),
	'heading': '151.78',
	'pitch': '-0.76',
	'key': 'AIzaSyD6abYckbgTesmrT_9Q1nbCR_3mElUhmQg'
              }]
    results = street_view(params)
    results.download_images('D:\Clients\Cincinnati Financial\output (input 5)\google_street_view', image_name = str(data.iloc[i,:]['CLIENT_ID']))
    
