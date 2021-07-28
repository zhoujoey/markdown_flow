#!/usr/bin/python
# -*- coding: UTF-8 -*-
from notion.client import NotionClient
from notion.block import PageBlock, ImageBlock, HeaderBlock
import md2notion.upload as upload
import yaml

class Md2Notion:
    def __init__(self, page_url, token):
        self.__client = NotionClient(token_v2 = token)
        self.__page = self.__client.get_block(page_url)
    
    def uploadByHeader(self, path):
        mdFile = open(path, "r", encoding="utf-8")
        rendered = upload.convert(mdFile, upload.NotionPyRenderer)

        newPage = self.__page
        for idx, blockDescriptor in enumerate(rendered):
            pct = (idx+1)/len(rendered) * 100
            print(f"\rUploading {blockDescriptor['type'].__name__}, {idx+1}/{len(rendered)} ({pct:.1f}%)", end='')
            
            if blockDescriptor["type"] == HeaderBlock:
                print(blockDescriptor["title"])
                newPage = self.__page.children.add_new(PageBlock, title=blockDescriptor["title"])
            else:
                upload.uploadBlock(blockDescriptor, newPage, mdFile.name, None)



# if __name__ == "__main__":
#     yml = open("config.yaml", 'r', encoding='utf-8')
#     notionPram = yaml.safe_load(yml.read())["notion"]
#     md2notion = Md2Notion(notionPram["page_url"], notionPram["token"])
#     md2notion.uploadByHeader("VSLAM-Base.md")
