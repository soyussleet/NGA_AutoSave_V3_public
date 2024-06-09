"""
主程序
"""
from download_posts_thread_controller import download_posts_thread_controller
from utils import setting_manager
import threading  
import time
from datetime import datetime  
from utils.print_if import print_if,print_passed_time
from utils.post_stats_operator import static,cycle_static

download_should_stop = threading.Event()
is_downloading=False
deadlock_timeout=setting_manager.get("downloadThreadDeadlockTimeout",30)
  
def run_download_posts_thread(): 
    '''循环执行download_posts_thread_controller，并在每次执行后等待指定的时间间隔'''
    global is_downloading
    while not download_should_stop.is_set():  
        is_downloading=True
        download_posts_thread_controller()
        interval_arr=setting_manager.get("downloadLoopinterval",60)
        interval=interval_arr[datetime.now().hour]
        print_if(f"下次抓取间隔:{interval}s\n\n\n\n\n",5)
        is_downloading=False
        time.sleep(interval)  
   
def run_monitor_thread():  
    '''监控线程，检查并可能重启 download_posts_'''
    global is_downloading
    while True:  
        time.sleep(5)  # 每5秒检查一次  
        # 不在下载中时不检测卡死
        if not is_downloading:
            continue
        
        current_pass_time = print_passed_time()  
        print_if(f"====================current_pass_time: {current_pass_time}",0,False)
        if current_pass_time > deadlock_timeout:  
            print_if("下载线程卡死，准备重启",2,False)  
            download_should_stop.set()  
            time.sleep(1)  # 假设线程在1秒内会响应停止信号  
              
            # 清除停止标志并启动新线程（或重用旧线程对象）  
            download_should_stop.clear()  
            download_thread = threading.Thread(target=run_download_posts_thread)  
            download_thread.daemon = True  # 根据需要设置  
            download_thread.start()  


# 工程入口  
def main():  
    '''创建下载帖子的线程'''  
    # 启动下载线程
    download_thread = threading.Thread(target=run_download_posts_thread)  # 假设间隔是5秒  
    download_thread.daemon = True  # 设置为守护线程，主线程退出时它也会退出  
    download_thread.start()  
    #download_thread.join()  
    
    # 启动监控线程
    monitor_thread = threading.Thread(target=run_monitor_thread)  
    monitor_thread.start()  
    #monitor_thread.join()  

    # 启动统计线程
    cycle_static_thread = threading.Thread(target=cycle_static)  
    cycle_static_thread.start()  
    cycle_static_thread.join() 

# 运行主函数  
if __name__ == "__main__":  
    main()
