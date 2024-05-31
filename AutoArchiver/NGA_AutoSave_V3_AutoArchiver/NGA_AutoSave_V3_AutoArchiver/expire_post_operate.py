"""
超时帖子处理，包括记为"确认超时"前的最后一次访问，和确认超时后的记录文件的删除
"""

from db_managers import monitoring_posts_db_manager
from utils.print_if import print_if
from utils import setting_manager
from datetime import datetime
from shutil import rmtree

saveFileExpire:dict[str:int] = setting_manager.get("saveFileExpire")
current_time = datetime.now()  
fid_file_expire_default:int=saveFileExpire["default"]
saveFileBaseFolder:str=setting_manager.get("saveFileBaseFolder")# 基础存档文件夹
needDelPostExpireInDb:bool=setting_manager.get("needDelPostExpireInDb")# 基础存档文件夹

def expire_post_operate():
    '''遍历删除已过期帖子'''
    print_if("开始遍历删除已过期帖子",5)
    posts = monitoring_posts_db_manager.query_all_posts()
    for post in posts:
        
        # 帖子保存文件的超时时间
        fid_file_expire:int=saveFileExpire[post.fidOrStid] if post.fidOrStid in saveFileExpire else fid_file_expire_default

        # 设计版面为为不删除时，不进行后续处理
        if fid_file_expire==-1:
            continue 
        # 超过保存期限  
        if (current_time - post.finalReplayTime).total_seconds()>fid_file_expire :
            # 如果帖子仍然正常监控中或已过期不再监控但是仍然暂存文件时，设置为即将删除（validState=4）
            # 设为validState=4的帖子在download_post里会再次尝试一次下载，如果仍然超过时，会设为validState=5以确认删除
            if post.validState==1 or post.validState==3:
                post.validState=4
                monitoring_posts_db_manager.update_or_add_post(post)
                print_if(f"过期帖子删除前最后重访tid={post.tid}",1)
            # validState=5以确认删除
            if post.validState==5:
                
                savedFilePath=post.savedFilePath
                folder_name=f"{saveFileBaseFolder}/{savedFilePath}"
                try:
                    rmtree(folder_name)
                except Exception as e:
                    print_if(f"无法删除{folder_name}，{e}")
                if needDelPostExpireInDb:
                    try:
                        monitoring_posts_db_manager.delete_post(post.tid)
                    except Exception as e:
                        print_if(f"无法删除数据库记录：tid={post.tid}，{e}")
                    print_if(f"已经删除tid={post.tid}的保存文件和数据库记录",1)
                else:
                    print_if(f"已经删除tid={post.tid}的保存文件",1)
                post.validState=6
                monitoring_posts_db_manager.update_or_add_post(post)


