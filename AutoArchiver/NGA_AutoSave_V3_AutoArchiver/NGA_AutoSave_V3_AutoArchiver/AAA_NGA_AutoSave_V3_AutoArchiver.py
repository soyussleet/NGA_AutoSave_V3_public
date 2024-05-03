"""
主程序
"""
from download_posts_thread_controller import download_posts_thread_controller
from utils import setting_manager
import threading  
import time
from datetime import datetime  
from utils.print_if import print_if
from expire_post_operate import expire_post_operate
  
  
# 这个函数会循环执行download_posts_thread_controller，并在每次执行后等待指定的时间间隔  
def run_download_posts_thread(): 
    
    interval=60
    while True:  
        download_posts_thread_controller()
        expire_post_operate()
        interval_arr=setting_manager.get("downloadLoopinterval")
        interval=interval_arr[datetime.now().hour]
        print_if(f"下次抓取间隔:{interval}s\n\n\n\n\n",5)
        time.sleep(interval)  
  
# 这个函数用于用户交互  
def user_input():  
    while True:  
        user_command = input("请输入命令 (输入'exit'退出): ")  
        if user_command.lower() == 'exit':  
            print("用户请求退出，程序将结束。")  
            break  
        # 这里可以添加更多的命令处理逻辑  
        print(f"收到命令: {user_command}")  
  
# 工程入口  
def main():  
    # 创建下载帖子的线程  
    download_thread = threading.Thread(target=run_download_posts_thread)  # 假设间隔是5秒  
    download_thread.daemon = True  # 设置为守护线程，主线程退出时它也会退出  
    download_thread.start()  
  
    # 创建用户输入的线程  
    input_thread = threading.Thread(target=user_input)  
    input_thread.start()  
  
    # 主线程等待用户输入线程结束（在真实情况下，您可能不需要这么做，因为user_input线程是无限循环的）  
    input_thread.join()  
  
    # 实际上，由于download_thread是守护线程，主线程退出时它也会退出  
    # 如果需要等待download_thread结束，需要取消daemon设置，并调用download_thread.join()  
  
# 运行主函数  
if __name__ == "__main__":  
    main()
