from .__version__ import __version__
import subprocess
import json
import os
from urllib.parse import urlparse
from b_hunters.bhunter import BHunters
from karton.core import Task
import tempfile
import requests
import re
class waybackm(BHunters):
    """
    Paths wayback scanner developed by Bormaa
    """

    identity = "B-Hunters-wayback"
    version = __version__
    persistent = True
    filters = [
        {
            "type": "subdomain", "stage": "new"
        }
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    def geturls(self,url):
        try:
            filename=self.generate_random_filename()
            output=subprocess.run(["/app/getpaths.sh",url,filename], capture_output=True, text=True,timeout=1200)
            data=""
            if os.path.exists(filename) and os.path.getsize(filename) > 0:  # Check if file exists and is not empty
                with open(filename, 'r') as file:
                    try:
                        data = file.read()
                        # print("data is ",data)
                    except Exception as e:
                        print("Error:",e)
                        result=""
            else:
                result=""
            if data!="":
                dataarr=data.split("\n")
                result=dataarr
                os.remove(filename)
        except Exception as e:
            self.log.error(e)
            raise Exception(e)
        return result
                
    def scan(self,url):

        result=self.geturls(url)
        if result !="":
            return result
        return []
        
    def process(self, task: Task) -> None:
        source = task.payload["source"]
        subdomain = task.payload["subdomain"]
        subdomain = re.sub(r'^https?://', '', subdomain)
        subdomain = subdomain.rstrip('/')
        if source == "producer":
            url = task.payload_persistent["domain"]
        else:
            url = task.payload["data"]
        self.log.info("Starting processing new url " +url)
        self.update_task_status(subdomain,"Started")
        url = re.sub(r'^https?://', '', url)
        url = url.rstrip('/')
        try:
            db = self.db

            result=self.scan(url)
            resarr=[]
            for i in result:
                if i != "":
                    resarr.append(i)
            
            if resarr !=[] and len(resarr)>2:
                # printupload_object(result)
                # resultdata='\n'.join(result)
                resultdata = "\n".join(map(lambda x: str(x), resarr)).encode()
                self.log.info("Uploading data of "+url)
                # self.log.info(resultdata)
                senddata=self.backend.upload_object("bhunters","wayback_"+self.encode_filename(url),resultdata)
                tag_task = Task(
                    {"type": "paths", "stage": "scan"},
                    payload={"data": url,
                             "subdomain":subdomain,
                    "source":"wayback",
                    "type":"file"

                    }
                )
                self.send_task(tag_task)
                domain = re.sub(r'^https?://', '', url)
                domain = domain.rstrip('/')
                domains_collection = db["domains"]
                domain_document = domains_collection.find_one({"Domain": domain})
                existing_links = domain_document.get("Links", {}).get(self.identity, [])
                new_links = [link for link in resarr if link not in existing_links]
                if new_links:
                    domains_collection.update_one({"Domain": domain}, {"$push": {f"Links.{self.identity}": {"$each": new_links}}})

                if domain_document:
                    domain_id = domain_document["_id"]

                for i in resarr:
                    try:
                        # self.log.info(i)
                        if ".js" in i:
                            if self.checkjs(i):
                                collection2 = db["js"]
                                existing_document = collection2.find_one({"url": i})
                                if existing_document is None:

                                    tag_task = Task(
                        {"type": "js", "stage": "new"},
                        payload={"domain_id": domain_id,
                        "file": i,
                        "subdomain":subdomain,
                        "module":"wayback"
                        }
                    )
                                    self.send_task(tag_task)
                            
                    except Exception as e:
                        self.log.error(e)
            self.update_task_status(subdomain,"Finished")
        except Exception as e:
            self.log.error(e)
            self.update_task_status(subdomain,"Failed")
            raise Exception(e)