pia-cloud
=========

初期开发中（这个分支只是一个最原始的demo，主要用来试试看项目的大致效果）

一个通用的数据服务，提供文件存储（类似百度云存储，七牛，Swift等），格式化数据存储（类似Google的DataStore和BlobStore），离线文件下载和上传(提交一个下载或上传请求，pia-cloud执行，执行完后调用各种hook)，提供一个统一的API接口

开源，可以使用官方提供的云服务(还未提供)，也可以自行部署，存储后端可以自选选择（HDFS, HBase, Swift，或者现成的七牛等云服务），pia-cloud提供统一的API


**[Trello Board](https://trello.com/b/9kU4JjKN/pia-cloud)**


**Collaborators**
* [zoowii](https://github.com/zoowii)
* [Dawn](https://github.com/dawn110110)
* [Sight4](https://github.com/Sight4)
* [mayflaver](https://github.com/mayflaver)
* [jusker](https://github.com/jusker)


**Demo说明**
* Demo只是为了试试效果，没有考虑任何扩展性，安全，性能等
* 主要包括离线下载和datastore服务
* 没有考虑mime类型，全部使用二进制
* Demo中datastore使用类sql语法，通过websocket协议传输命令和回复，不支持limit, offset, bson等高级特性
* 运行需要拷贝cloudweb/core/settings.py.bak 到cloudweb/core/settings.py，file_backend文件夹下同样操作
* 运行需要运行cloudweb中的server.py，以及后端下载程序file_backend/file_downloader.py