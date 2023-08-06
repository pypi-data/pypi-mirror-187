This package is used to store files in mongodb

Install the requirements files
Packages used :
******pymongo*******  
pip install pymongo
******gridfs******
pip install gridfs-fuse

import statement:
import mongoudaan as mu

Now add your mongourl to a variable
db = mu.mongo_conn()

To upload_files use the below command
mu.upload_file(Filepath,filename with extension,database object)

To download_files use the below command
mu.download_file(downloadpath,filename with extension,database object)