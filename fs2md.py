#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import requests
import base64
import json
import re
import yaml

class ImageProcess:
    def __init__(self, image_path, file_name):
        self.image_path = image_path
        self.file_name = file_name
        self.__token = ""
        self.__repo = ""
        self.__msg = "add_" + file_name 
        self.__name = ""
        self.__email = ""
    
    def setGitParam(self, repo, token, name = "nobody", email = "xx@github.com"):
        self.__token = token
        self.__repo = repo
        self.__name = name
        self.__email = email

    def upload2git(self, b64Img):
        image_name = os.path.join(self.image_path, self.file_name)
        url = "https://api.github.com/repos/" + self.__repo + "/contents/" + image_name
        headers = {"Authorization": "token " + self.__token}
        data = {
            "message": self.__msg,
            "committer": {
                "name": self.__name,
                "email": self.__email
            },
            "content": b64Img 
        }
        data = json.dumps(data)
        req = requests.put(url = url, data = data, headers = headers)
        req.encoding = "utf-8"
        if req.status_code == 422:
            r = requests.get(url=url, headers=headers)
            r_data = json.loads(r.text)
            return r_data['download_url']
        elif req.status_code == 201:
            re_data = json.loads(req.text)
            return re_data['content']['download_url']
        else:
            print("Uncaught error in git api, erorr code : ", req.status_code)
            return json.loads(req.text)


    def download2local(self, b64Img):
        if not os.path.exists(self.image_path):
            os.makedirs(self.image_path)
        image_name = os.path.join(self.image_path, self.image_name)        
        f = open(image_name, 'wb')
        f.write(base64.b64decode(b64Img))
        f.close()
        return image_name 


def fsURL2git(file_name, gitPram):
    #read and write file 
    f = open(file_name, 'r')
    Lines = f.readlines()
    f.close()
    f = open(file_name, 'w')

    image_count = 1
    No_1_count = 0
    No_2_count = 0
    No_3_count = 0
    # Strips the newline character
    img_name  = file_name
    for line in Lines:
        line = line.strip()
        if re.match(r'\#\s.+',line):
            img_name = re.search('\w+',line).group()
            No_1_count += 1 
            No_2_count = 0
            No_3_count = 0
            image_count = 1

        if re.match(r'\#\#\s.+',line):
            img_name = re.search('\w+',line).group()
            No_2_count += 1
            No_3_count = 0
            image_count = 1
            
        if re.match(r'\#\#\#\s.+',line):
            img_name = re.search('\w+',line).group()
            No_3_count += 1
            image_count = 1
    
        # this is a image_url 
        if re.match(r'\!\[.+\]\(.+\)',line):
            # tag = re.search(r'\!\[.+\]',line).group()[2:-1]
            url = re.search(r'\(.+\)',line).group()[1:-1]
            tag = "Pic_" + str(No_1_count)
            tag += "." + str(No_2_count)
            tag += "." + str(No_3_count)
            tag += "." + str(image_count)

            image_name = tag + "_" +  img_name + ".png"
            try:
                req = requests.get(url)
                b64Img =  base64.b64encode(req.content).decode()

                wFlow = ImageProcess(file_name, image_name)
                wFlow.setGitParam(repo = gitPram["repo"],token =  gitPram["token"], \
                                  name = gitPram["name"], email = gitPram["email"]) 
                #if update image to git, use this
                url = wFlow.upload2git(b64Img) 
                #if download image to local use this
                #url = wFlow.download2local(b64Img)                             
            except:
                print("unable to download or update from url. ")
            print(url)
            line = "![" + tag + "]" + "(" + url + ")"
            image_count += 1
        f.write(line + "\n")
    f.close()

# if __name__ == "__main__":
#     # load params
#     yml = open(yaml_path, 'r', encoding='utf-8')
#     myPram = yaml.safe_load(yml.read())

#     fsURL2git("VSLAM-Base.md", myPram["git"])


