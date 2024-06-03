# NGA_AutoSave_V3_public
# NGA赛博史官**V3**

# 0.更新日志
[更新日志 V3.1](UpdateLog.md)

# 1.目的

为了解决NGA中一些大瓜爆出来之后，因为众所周知的社管删帖、孝子打滚等原因导致帖子被爆破，所以需要将帖子好好保存

# 2.功能

1.获取版面中的所有帖子  
2.将所有帖子保存到本地,**并隐去留档者的信息**  
3.数据库管理保存帖子的记录，并使用数据库进行一定分析  
4.坟贴处理，超过监控期限的帖子不再下载，超过保存期限的帖子不再保存（记录为已被删帖的除外）  
5.全篇帖子保留到markdown文档中，体积更小。**并且Markdown文档为按楼层更新储存而非按页储存**，不会出现某一楼的内容被修改后当最新一页重新下载抓取时楼层修改后的内容被抓取并保存从而丢失保存前的内容

# 3.配置方式（AutoArchiver自动留档机部分）

## 3.1.文件路径

自动留档机的路径在
```.\AutoArchiver\NGA_AutoSave_V3_AutoArchiver\NGA_AutoSave_V3_AutoArchiver```
主程序为```AAA_NGA_AutoSave_V3_AutoArchiver.py```。

## 3.2.配置python

**python运行环境为3.10.7**，其他版本没有测试过，可能存在需要更改配置的情况。  
在```.\AutoArchiver\NGA_AutoSave_V3_AutoArchiver\NGA_AutoSave_V3_AutoArchiver```中打开cmd（或cd到该文件夹），```pip3 install -r requirements.txt```安装需要的包。（也可以不cd过去，而将requirements.txt的完整绝对路径作为参数来pip install）。  
同样的，对DistributeServer也需要安装requirements.txt  

## 3.3.获取cookie

1.使用Edge或chrome浏览器，F12进入开发者模式，在```Application->Cookies->https://bbs.nga.cn```（这个链接也可以是nga.178.cn或其他的nga相关url）中，得到nga的cookies   
2.复制以"nga"开头的cookie    
![image](https://github.com/soyussleet/NGA_AutoSave_V3_public/assets/164469268/b337e4cf-5162-48d6-8c33-09fc5f210157)   
3.运行AAA_NGA_AutoSave_V3_AutoArchiver.py。因为当前没有记录cookie，所以会弹窗提示输入cookie，将上面复制的cookie粘贴进输入框中  
![image](https://github.com/soyussleet/NGA_AutoSave_V3_public/assets/164469268/e4340587-1fe8-406a-b698-3df83a26de0f)    
4.因为尚未进行配置数据库，所以会报错，请参看3.4进行配置  

## 3.4.设置文件

设置主要在根目录下```.\settings```文件夹中的```settings.json```文件。如无该文件，可以复制```settingsTemplate.json```并更名为```settings.json```。在直接运行AAA_NGA_AutoSave_V3_AutoArchiver.py时，会自动执行复制操作。下文中的查询服务器会共用同一个设置文件。     
**请不要修改```settingsTemplate.json```文件，更不要将修改后的该文件上传，除非你知道这个文件的作用**   
配置```setting.json```中的```DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, TABLE_NAME_monitoring_posts, TABLE_NAME_monitoring_boards```这些变量，这些是数据库的变量，参看3.5。   
其他设置可以直接看注释，或者直接使用默认值   
常见需要自己配置的设置条目为```monitoringBoards```。如果需要修改保存至的文件夹```saveFileBaseFolder```时，可以为相对路径或绝对路径，默认中为相对路径  

## 3.5.数据库

### 3.5.1.数据库配置

数据库使用mysql。你可以自行安装mysql，或使用phpStudy进行方便地安装。
导入```nga_autosave_db.sql```数据库文件
在```settings.json```中配置数据库的各个参数

### ~~3.5.1.已删除监控中的版面 monitoring_boards~~

~~记录了哪些版面需要被监控~~  
~~![image](https://github.com/soyussleet/NGA_AutoSave_V3_public/assets/164469268/98214881-6d3a-4fbc-a97c-074bdd73441d)~~  
~~注意版面id一定要带上"fid="或"stid="，单独只有id数字是无法访问到指定版面的，在配置setting.json同理~~
~~这个不一定被使用（```setting.json```中```monitoringBoardsUseDb```设置为```false```时即不使用）~~   


### 3.5.2.帖子记录 monitoring_posts

所有帖子的关键数据记录  
![image](https://github.com/soyussleet/NGA_AutoSave_V3_public/assets/164469268/882bea85-c29e-4f76-9741-cb42616aef3b)

### 3.5.3.帖子统计 post_stats

记录帖子的统计数据，以每天为单位统计当天的每个版面的发帖数和被删帖数

## 3.6.额外配置

可以配置开机启动。  
为```AAA_NGA_AutoSave_V3_AutoArchiver.py```创建快捷方式。按```win+R```打开运行窗口后输入```shell:startup```进入“启动”文件夹  。将创建的快捷方式移动到“启动”文件夹，即可配置为开机自启动。同样的，建议将mysql也设置开局自启动。

# 4.配置方式（DistributeServer查询服务器部分）

## 4.1.文件路径

查询服务器**是一个Django服务器**，路径在  
```DistributeServer\NGA_AutoSave_V3_DistributeServer\NGA_AutoSave_V3_DistributeServer```  
因为是Django服务器，所以使用命令行调用manage.py以启动  
``` cmd
python manage.py runserver 8080
```  
后文有启动方法

## 4.2.注意事项

查询服务器仍在开发中，目前功能暂不完善。

# 5.启动程序与记录查找

## 5.1.启动程序

根目录下的```启动自动下载器.cmd```即可启动下载器。在不需要查询的情况下启动这个即可完成留档功能。  
查询服务器不是必须打开。在```启动查询服务器.cmd```启动，或在查询服务器的文件路径内启动 ```manage.py```(见4.1)：  
``` cmd
python manage.py runserver 8080
```  
可以自行查询Django服务器的启动方式，以修改```启动查询服务器.cmd```或直接启动```manage.py```的启动参数。  

## 5.2.快速网页/数据库查询

当未打开查询服务器时，可以直接访问数据库，使用Navicat或VS Code的mysql插件等数据库管理软件打开。数据库配置以自动留档机的```setting.json```中的数据库配置为准。所有储存于数据库的内容都可以查询。  
当打开了查询服务器时，访问```http://127.0.0.1:8080/mainApp/dbGetAll```即可访打开查询网页。一般，在启动```启动查询服务器.cmd```时，会自动打开该网页。如果修改了```启动查询服务器.cmd```，那么查询网页的```IP:port```需要对应修改。  
查询服务器中目前支持查询（TID、标题、发帖人）和筛选已被删除的帖子。  
![image](https://github.com/soyussleet/NGA_AutoSave_V3_public/assets/164469268/0e323518-82ab-4420-97f4-55db2d950acf)

## 5.3.下载文件查找

默认的留档文件在```.\AutoArchiver\NGA_AutoSave_V3_AutoArchiver\NGA_AutoSave_V3_AutoArchiver\pageSaved```，如果修改了```setting.json```中的留档路径（```saveFileBaseFolder```），则需要对应的修改路径
可以在数据库中按帖子id、标题、发帖人等进行搜索。更方便的是，可以直接筛选```validState=2 or retryCnt>0```的记录，即可直接筛选得到已经被删或锁的帖子(validState=1为可用，validState=2为确认被锁/删的帖子，retryCnt为帖子无法访问时的重试次数，重试次数大于一定值（默认为5）时即会被记为validState=2)。你可以安装navicat等数据库管理软件进行数据库可视化管理。    
![image](https://github.com/soyussleet/NGA_AutoSave_V3_public/assets/164469268/68e8b669-5981-42a4-a3e4-af75676be785)    
在```pageSaved```文件夹中（如果```setting.json```配置了```saveFileBaseFolder```，则在对应文件夹中），可以找到保存的帖子网页    
![image](https://github.com/soyussleet/NGA_AutoSave_V3_public/assets/164469268/8f393d9e-5f0f-4ce3-a953-b9d9d737f5fd)  

# 6.特别注意
  
* 1.初次保留超高楼层的帖子的时候会因为服务器关闭session而出错，这时候需要在settings里添加标题过滤，或在数据库中手动添加相关记录，并将lastPage修改为当前真实的末页页码。  
* 2.查询服务器目前功能尚不完善，需要后续开发。  
  
# 7.ToDo
  
* 1.帖子词云分析  
* 2.每日版面发帖与删帖数量统计  
* 3.查询服务器功能增加 





