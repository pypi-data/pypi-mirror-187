import os
import json
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
import pandas as pd
from pandasql import sqldf
import datetime as dt
from datetime import datetime
import requests
import boto3
import awswrangler as wr
from tqdm import tqdm
from tqdm import trange
from botocore.exceptions import ClientError
"""
#pip install PyQt5==5.9.2
plt.scatter(x, y)
plt.plot(myline, mymodel(myline))
plt.show()

"""


class data_processing_tools:
    def __init__(self,bucket_name:str=''):
        self.alphavantage = {}
        self.sta_bucket,self.environment = '','local'
        self.local_directory = os.getcwd()
        self.s3_bucket = 'dn-dev01/'
        if bucket_name != '':
            self.sta_bucket =  's3://' + bucket_name + '/'
            self.environment = bucket_name
        self.settings = self.sta_bucket + 'settings/'
        self.secrets = self.settings + 'secrets/'
        self.metadata = self.settings + 'metadata/'
        self.datalake = self.s3_bucket + 'datalake-demo01/'
        self.hive = self.s3_bucket + 'hive-demo01/'
        self.dl_crypto = self.datalake + 'crypto_currencies/'
        self.dl_crypto_intraday = self.dl_crypto + 'intraday/'

        self.api_key_path = self.secrets + 'alphavantage/api_key.txt'
        try:
            self.load_metadata()
        except:
            ...
    
    def domain_commands(self,domain_name:str=None):
        if domain_name != None:
            domain_name = domain_name.lower().strip()
            self.load_metadata()
            strx = ""
            for k,v in self.commands.items():
                for k1,v1 in v.items():
                    if strx != "":
                        strx += "\n"
                    this_command = v1
                    for k2,v2 in self.connection_details[domain_name].items():
                        this_command = this_command.replace("@" + k2, v2)
                    strx += this_command
            output_file = domain_name.replace('.','_') + '.txt'
            with open(output_file,'w') as output_file:
                output_file.write(strx)
                print("output_file:",output_file)
            print(strx)

    def create_bucket(self,bucket_name, region=None):
        """Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).

        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: True if bucket created, else False
        """

        # Create bucket
        try:
            if region is None:
                s3_client = boto3.client('s3')
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client = boto3.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)
                print("bucket:",bucket_name, " succesfully created!")
        except ClientError as e:
            print(e)
    def store_dict_as_json(self,dictionary_input:dict,writing_path:str,local:bool=True)->None:
        if local == True:
            with open(writing_path,'w') as out_file:
                json.dump(dictionary_input,out_file,sort_keys=False,indent=4)
    def date_time_id(self):
        date_id = int(datetime.now().strftime("%Y%m%d"))
        time_id = int(datetime.now().strftime("%H"))*60*60
        time_id += int(datetime.now().strftime("%M"))*60
        time_id += int(datetime.now().strftime("%S"))
        return date_id,time_id
    def load_metadata(self,cust_filename:str = None):
        if self.environment.lower().strip() == 'local':
            #print("self.metadata:",self.metadata)
            all_files_list = self.find_files_in_folder(self.metadata)
            dynamic_code = 'with open(self.metadata + "@json_file.json") as input_file:\n'\
                '\tself.@json_file = json.loads(input_file.read())'
        else:
            all_files_list = self.find_files_in_s3_folder(self.metadata)
            dynamic_code = 'self.@json_file = self.get_s3_file_content("@json_file",self.metadata)'   
        json_files = [f.lower().strip().replace('.json','') for f in all_files_list if f.lower().endswith('.json')]
        if cust_filename != None:
            cust_filename = cust_filename.lower().strip().replace('.json','')
            json_files = [f for f in json_files if f == cust_filename]
        for json_file in json_files:
            this_dynamic_code = dynamic_code.replace('@json_file',json_file)
            exec(this_dynamic_code)
        

    def find_files_in_folder(self,path:str=None, extension:str = None):
        #print("path:",path)
        if path == None:
            path = self.local_directory
        files = [f for f in os.listdir(path)]
        if extension != None:
            files = [f for f in files if f.endswith('.' + extension)]
        return files
            
    def store_str_as_file_in_s3_folder(self,strInput,fileName,s3FullFolderPath):
        s3FullFolderPath = s3FullFolderPath.replace("s3://","")
        if type(strInput) != str:
            strInput = str(strInput)
        s = s3FullFolderPath
        bucketName=s[0:s.index('/')]
        rp = s.replace(bucketName,'')
        relativePath = rp[1:len(rp)]
        client = boto3.client('s3')
        fileKey = relativePath + fileName
        try:
            client.put_object(Body=strInput,Bucket=bucketName,Key=fileKey)
            print('file successfully stored in:\ns3://' + s3FullFolderPath + fileName)
        except Exception as e:
            print(str(e))
    def fixed_size_int_to_str(self,intInput:int,size:int):
        rslt = str(intInput)
        while len(rslt) < size:
            rslt = "0" + rslt
        return rslt
    def standard_dict_to_json(self,jsonOrDictionary,fileName,folderPath):
        fileName = fileName.replace(".json","") + ".json"
        self.store_str_as_file_in_s3_folder(
            strInput=json.dumps(jsonOrDictionary,sort_keys=False,indent=4)
            ,fileName=fileName
            ,s3FullFolderPath=folderPath)
    def datetime_id_symbol_path(self,symbol:str,ext:str=None,date_id:int=None,big_data:bool=False):
        x,symbol,s3FullPath = '/date_id=',symbol.lower().strip(),self.dl_crypto_intraday
        if date_id == None: 
            date_id,time_id = self.date_time_id()
            s3FullPath += symbol + x + str(date_id) + '/'
            file_name = self.fixed_size_int_to_str(time_id,5) + "." + ext.replace(".","")
            return s3FullPath,file_name
        else:
            s3FullPath += symbol + x + str(date_id) + '/'
            return s3FullPath
        
    def get_s3_file_content(self,referenceName,s3FullFolderPath,exceptionCase=False):
        rslt_dict,fileContent,ext={},"",""
        if referenceName != "":
            s=s3FullFolderPath.replace('s3://','')
            filesFound=0
            bucketName=s[0:s.index('/')]
            rp=s.replace(bucketName,'')
            relativePath=rp[1:len(rp)]
            resource=boto3.resource('s3')
            my_bucket=resource.Bucket(bucketName)
            objectSumariesList=list(my_bucket.objects.filter(Prefix=relativePath))
            fileKeys=[]
            for obs in objectSumariesList:
                fileKeys.append(obs.key)
            for fileKey in fileKeys:
                a=fileKey[::-1]
                ext='.'+fileKey.lower()[::-1].split('.')[0][::-1]
                thisFile=fileKey.replace(relativePath,'').replace('/','')
                if(thisFile.lower()).replace(ext,'') == referenceName.lower().replace(ext,''):
                    filesFound+=1
                    obj=resource.Object(bucketName,fileKey)
                    fileContent=obj.get()['Body'].read().decode('utf-8')
                    if ext=='.json':
                        if exceptionCase==False:
                            fileContent=fileContent.replace("'",'"')
                        rslt_dict=json.loads(fileContent)
                    break
            if ext=='.json':
                return rslt_dict
            else:
                return fileContent
            
    def find_files_in_s3_folder(self,s3FullFolderPath):
        these_files =set()
        s=s3FullFolderPath.replace('s3://','')
        filesFound=0
        bucketName=s[0:s.index('/')]
        rp=s.replace(bucketName,'')
        relativePath=rp[1:len(rp)]
        resource=boto3.resource('s3')
        my_bucket=resource.Bucket(bucketName)
        objectSumariesList=list(my_bucket.objects.filter(Prefix=relativePath))
        fileKeys=[]
        for obs in objectSumariesList:
            fileKeys.append(obs.key)
        for fileKey in fileKeys:
            a=fileKey[::-1]
            ext='.'+fileKey.lower()[::-1].split('.')[0][::-1]
            thisFile=fileKey.replace(relativePath,'').replace('/','')
            these_files.add(thisFile)
        return these_files             
            
    def store_api_staging_data(self,symbol):
        symbol = symbol.lower().strip()
        s3FullPath,file_name = self.datetime_id_symbol_path(symbol,ext='json')
        if self.environment.lower().strip() == 'local':
            with open (self.api_key_path,'r') as input_file:
                api_key = input_file.read()
        else:
            referenceName = self.api_key_path[::-1].split('/')[0][::-1]
            s3FullFolderPath =  self.api_key_path.replace(referenceName,'')
            api_key = self.get_s3_file_content(referenceName=referenceName,s3FullFolderPath=s3FullFolderPath)
        this_url = self.alphavantage_config["cryptocurrencies"]["intraday"]["url"]\
        .replace("@symbol",symbol).replace("@api_key",api_key)
        data = requests.get(this_url).json()
        self.standard_dict_to_json(jsonOrDictionary=data
                                   ,fileName=file_name
                                   ,folderPath=s3FullPath)
        return file_name,s3FullPath
    
    def consolidate_staging_data(self,symbol:str,date_id:int):
        symbol = symbol.lower().strip()
        s3FullPath = self.datetime_id_symbol_path(symbol=symbol,date_id=date_id)
        list_of_files = list(self.find_files_in_s3_folder(s3FullPath))
        lx = len(list_of_files)
        if lx > 0:
            rslt = pd.DataFrame()
            print("s3FullPath:\n",s3FullPath)
            message = "Consolidating data for @symbol at @date_id"
            message = message.replace("@symbol",symbol).replace("@date_id",str(date_id))
            
            for i in tqdm(range(lx),desc=message):
                time_id_fileName = list_of_files[i]
                data = self.get_s3_file_content(
                    referenceName = time_id_fileName
                    ,s3FullFolderPath=s3FullPath)
                time_id = int(time_id_fileName.replace(".json",""))
                this_df = self.json_to_df_crypto(symbol,data,date_id,time_id)
                if i > 0:
                    rslt = pd.concat([rslt,this_df])
                else:
                    rslt = this_df
            return rslt
        else:
            print('No files were found in:\n',s3FullPath)
            
    def json_to_df_crypto(self,symbol:str,data:dict,date_id:int,time_id:int):
        df = pd.DataFrame(data["Time Series Crypto (5min)"]).transpose()
        df["date"] = df.index
        df['date'] = pd.to_datetime(df['date'])
        df['epoch'] = (df['date'] - dt.datetime(1970,1,1)).dt.total_seconds()
        df['date'] = df['date'].dt.strftime('%d/%m/%Y')
        df['epoch'] = df['epoch'].astype(int)
        df['capture_date_id'] = date_id
        df['capture_date_id'] = df['capture_date_id'].astype(int)
        df['capture_time_id'] = time_id
        df['capture_time_id'] = df['capture_time_id'].astype(int)
        q = """
        select row_number() over(order by a.[epoch] asc) [id],a.* from 
        (select distinct [epoch]
        ,round([1. open],4) [open]
        ,round([2. high],4) [high]
        ,round([3. low],4) [low]
        ,round([4. close],4) [close]
        ,[5. volume] [volume],[date],[capture_date_id],[capture_time_id] from df) a
        order by 1 asc;
        """
        rslt_df = sqldf(q)
        file_name = symbol.lower() + "_" + str(date_id) + "_"+ str(time_id) + ".parquet"
        rslt_df.to_parquet(file_name)
        return rslt_df
 