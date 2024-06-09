# UpdateLog.md
# 更新日志

## V3.1

* 1.新增下载卡死重置，现在在卡死后会自动重启下载线程了  
* 2.新增初步的服务端，distribute_server，使用django编写。目前能获取记录中的帖子了，并且能对TID、标题、发帖人进行搜索，并且能筛选被ban的帖子。访问链接为[http://127.0.0.1:8080/mainApp/dbGetAll](http://127.0.0.1:8080/mainApp/dbGetAll)，可以自行修改启动文件以修改ip:port
* 3.在根目录新增启动文件
  
## V3.2

* 1.新增查询服务器，现在可以查询帖子列表，获取发帖删帖数量统计，获取存档文件
* 2.**更改了存档文件的位置**和设置文件的位置，现在在根目录里了
![image](https://github.com/soyussleet/NGA_AutoSave_V3_public/assets/164469268/38a86bdc-c996-495a-9f02-a99900661331)
![image](https://github.com/soyussleet/NGA_AutoSave_V3_public/assets/164469268/a0abefce-0ed3-4e86-83ba-9d47d7113a58)
![image](https://github.com/soyussleet/NGA_AutoSave_V3_public/assets/164469268/9dd028ba-089f-4927-b6b5-c260c68f7e7b)
