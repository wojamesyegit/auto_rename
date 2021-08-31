# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 23:01:53 2021

@author: Mr. Wang
"""
import urllib.request
import urllib.parse
import json
import time
import base64
import os 

url_request="http://dm-58.data.aliyun.com/rest/160601/ocr/ocr_business_license.json"
url_idcard = "http://dm-51.data.aliyun.com/rest/160601/ocr/ocr_idcard.json"
path = './licenses'
AppCode = "13f1214aadc047d2999d4298d9a12091"
ecode = "{\"name\":\"!!Fail!!\"}"

headers = {
    'Authorization': 'APPCODE ' + AppCode,
    'Content-Type': 'application/json; charset=UTF-8'
}

my_dict = {}
old_names = os.listdir(path)
#success = 0  
fail = 0

def posturl(url,url_idcard, img_dict, idcard_dict):
  try:
    params=json.dumps(img_dict).encode(encoding='UTF8')
    req = urllib.request.Request(url, params, headers)
    print("- Start checking business license..")
    r = urllib.request.urlopen(req)
    html =r.read() 
    #print(html)
    r.close();
    return html.decode("utf8")
  except urllib.error.HTTPError as e:
      #print(e.code)
      print(" !"+ e.read().decode("utf8")+"!")
      try:
            params=json.dumps(idcard_dict).encode(encoding='UTF8')
            req = urllib.request.Request(url_idcard, params, headers)
            print("-- Now checking id card..")
            r = urllib.request.urlopen(req)
            html =r.read() 
            #print(html)
            r.close();
            return html.decode("utf8")    
      except urllib.error.HTTPError as e:
           print(" ! "+e.read().decode("utf8")+" !")
           fail = fail + 1
           return ecode    
  time.sleep(1)
  
def get_my_dict():
    success = 0
    for old_name in old_names:
        image_path = path+'/'+ old_name
        with open(image_path, 'rb') as f:  # 以二进制读取本地图片
            data = f.read()
            encodestr = str(base64.b64encode(data),'utf-8')
        img_dict = {'image': encodestr}
        idcard_dict = {'image': encodestr,
                       "configure": {
                          "side":"face", #身份证正反面类型:face/back}  
                        }
                      }
        success = success + 1
        print(str(success)+ " Reading "+old_name +"..")
        html = posturl(url_request,url_idcard, img_dict, idcard_dict) 
        #print(html)
        my_json = json.loads(html)
        new_name = my_json["name"]
        print("     The name of",old_name,"is: ", new_name)
        my_dict[old_name] = new_name
        rename_my_file(old_name, new_name)
    print("------Success: " + str(success) + " Fail: " + str(fail)+ " Total: " + str(success+fail))
    return my_dict

def rename_my_file(my_dict):
    
    print("---------------------------------------------")
    print("Start renaming..")
    flag = 1
    for old_name in old_names:
        new_name = my_dict[old_name]
        while((new_name+".jpg") in os.listdir(path)):
            new_name = new_name + "("+str(flag)+")"
            flag = flag+1   
        os.rename(os.path.join(path, old_name), os.path.join(path, new_name+".jpg")) 
        #print("     "+old_name+ "has been changed to:", new_name)

def rename_my_file(old_name, new_name):
    flag = 0
    my_new_name = new_name
    while((my_new_name+".jpg") in os.listdir(path)):
        flag = flag+1
        my_new_name = new_name + "("+str(flag)+")"   
    os.rename(os.path.join(path, old_name), os.path.join(path, my_new_name+".jpg")) 
    print("     Rename finished.")
    

def auto_rename():
    print("------------------Welcome---------------------")
    my_dict = get_my_dict()
   
    #pd.DataFrame(my_dict).to_csv('NameTable.csv')
    #rename_my_file(my_dict)
    print("---------------------Thank you-------------------------")
 
    
if __name__=="__main__":    
    auto_rename()
    
