"""
多线程下载控制器
"""

import concurrent.futures  
from get_posts_in_boards import get_posts_in_boards  
import download_post  
from utils import setting_manager
from db_managers.monitoring_posts_db_manager import MonitoringPost
from db_managers import monitoring_posts_db_manager
from utils.print_if import print_if
from datetime import datetime  
import time  
  
ngaBaseUrl=setting_manager.get("ngaBaseUrl")
tidBaseUrl=setting_manager.get("tidBaseUrl")
def download_task(post:MonitoringPost):  
    url = f"{ngaBaseUrl}/{tidBaseUrl}{post.tid}"  
    try:  
        print_if(f"==========开始下载: {url}==========\n")  
        download_post_operator=download_post.DownloadPostOperator(post) 
        operated=download_post_operator.download()
        print_if(f"==========下载完成: {url}==========\n")  
        return operated
    except Exception as e:  
        print_if(f"下载失败: {url}, 原因: {e}\n",2) 
        post.validState=2
        monitoring_posts_db_manager.update_or_add_post(post)

  
def download_posts_thread_controller():  
    """
    多线程下载控制器
    """
    print_if("开始多线程下载帖子",5)
    start_timestamp=time.time()
    # 获取目标帖子  
    target_posts = get_posts_in_boards()  
  
    # 设置线程池的最大线程数  
    with concurrent.futures.ThreadPoolExecutor(max_workers=setting_manager.get("downloadThreadCnt")) as executor:  
        # 提交所有任务到线程池  
        future_to_post = {executor.submit(download_task, post): post for post in target_posts}  
  
        # 遍历futures，获取结果或异常  
        for future in concurrent.futures.as_completed(future_to_post):  
            post = future_to_post[future]  
            try:  
                # 获取任务结果  
                result = future.result()  # 这里添加了获取结果的代码  
                # 假设result是MonitoringPost类型的实例，调用toString方法并打印  
                if isinstance(result, MonitoringPost):  
                    pass
                    # print_if(result.toString())  # 这里貌似没法用，因为MonitoringPost.toString()在之前已经被从线程池里删了
                    # print_if(f"下载成功{result.tid}")
                    print_if(f"下载成功")
                else:  
                    pass
                    print_if(f"下载帖子返回了非预期的结果: {post.toString()}\n",2)  
            except Exception as exc:  
                print_if(f'生成帖子 {post.tid} 时出错: {exc}\n',2)
                ##### 这里要添加处理validState


    end_timestamp=time.time()
    print_if(f"帖子遍历完成，时间{datetime.now()}，用时{end_timestamp-start_timestamp}s\n",3)
# 运行主控制器函数  
 
    #download_posts_thread_controller()