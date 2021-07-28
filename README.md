## 代码架构

### fs2md.py  

将markdown中图像连接由飞书或者其他链接, 转为git图床链接. 

链接新建文件名文件夹, 名称为Pic_目录级别 _ 图像序号 _ 上一级章节名称. 



### notion_upload.py

将mardown上传为当前页面url的block.  以Header为第一级目录新建子page. 

### notion/

官方notion-py库, 修正了limit导致的上传失败bug

参考:  https://github.com/jamalex/notion-py

### md2notion/

md2notion库, 强化了markdown的公式兼容性. 

参考:   https://github.com/Cobertos/md2notion



### config.yaml

用户git仓库与notion的参数

git 中 repo 为图床仓库, token为git的开发token , 

notion 中token为notion页面token, page_url为要添加的page的链接地址.

```yaml
git:

  repo: "you accont/your repo"

  token:  "xxx"

  name: "xxx"

  email: "xxx@xxx"

notion:

  token: "xxxxx"

  page_url: "https://www.notion.so/xxxxx"
```



### workflow.py

将mardown文件图像链接转为git图床 并 同步到notion.
