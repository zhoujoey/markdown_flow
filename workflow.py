#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import notion_upload as notion
import fs2md as fs
import yaml

if __name__ == "__main__":

    file_path = "VSLAM-Base.md"
    yaml_path = "config.yaml"
    yml = open(yaml_path, 'r', encoding='utf-8')
    myParam = yaml.safe_load(yml.read())
    yml.close()

    ## feishu image url to git 
    gitParam = myParam["git"]
    fs.fsURL2git(file_path, gitParam)


    ## markdown to notion
    notionParam = myParam["notion"]
    md2notion = notion.Md2Notion(notionParam["page_url"], notionParam["token"])
    md2notion.uploadByHeader(file_path)