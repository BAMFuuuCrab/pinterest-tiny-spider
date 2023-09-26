# pinterest-spider ✨pintrest批量化下载图片的简易爬虫



## 项目说明

- [ ] 初版使用读取本地target.txt文件获取配置信息

target.txt
```
line1: 874402083881249459  //第一行填写目标ID，例如 https://www.pinterest.com/pin/`874402083881249459`/ 
line2: 2000  //第二行填写单次最大爬虫数量
```

- [ ] 下载的图片存放于download目录，并且会根据在target.txt文件line1所填写的id自动创建文件夹