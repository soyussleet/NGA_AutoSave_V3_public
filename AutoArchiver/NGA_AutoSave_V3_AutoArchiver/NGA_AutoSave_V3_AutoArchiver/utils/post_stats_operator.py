'''
每日统计器
'''
from datetime import date, datetime, timedelta
from db_managers import monitoring_posts_db_manager,post_stats_db_manager
from db_managers.monitoring_posts_db_manager import MonitoringPost
from utils import setting_manager
from utils.print_if import print_if
import time

stat_trace_back_days:int=setting_manager.get("stat_trace_back_days")
monitoring_boards:dict=setting_manager.get("monitoringBoards")
monitoring_boards_keys:list[str]=list(monitoring_boards.keys())[:10]
RUN_CYCLE_STAT=True

def static():
    '''帖子统计器'''
    print_if("帖子统计器开始运行",5)
    for i in range(stat_trace_back_days,-1,-1):
        date=datetime.now().date() - timedelta(days=i)
        list_of_new_posts:list[MonitoringPost]=monitoring_posts_db_manager.get_posts_by_first_post_time(target_date=date)
        list_of_invalid_posts:list[MonitoringPost]=monitoring_posts_db_manager.get_posts_by_valid_state_and_final_replay_time(target_date=date)

        # 判断为空，则直接break
        if (not list_of_new_posts) or (not list_of_invalid_posts):
            continue 

        # 整体记录
        cnt_of_new_posts=len(list_of_new_posts)
        cnt_of_invalid_posts=len(list_of_invalid_posts)

        # 分版面记录
        cnt_of_new_posts_in_board=[0]*11
        cnt_of_invalid_posts_in_board=[0]*11
        
        for new_post in list_of_new_posts:
            # 帖子的版面在监控中的版面的数组中的下标
            index:int=0
            try:
                # 如果查询到了，就将index+1，因为记录版面帖子数量是从1开始的，并且将index=0作为未查询到的帖子的计数
                index=monitoring_boards_keys.index(str(new_post.fidOrStid))+1
            except:
                index=0
            cnt_of_new_posts_in_board[index]=cnt_of_new_posts_in_board[index]+1 
            
        for invalid_post in list_of_invalid_posts:
            # 帖子的版面在监控中的版面的数组中的下标
            index:int=0
            try:
                # 如果查询到了，就将index+1，因为记录版面帖子数量是从1开始的，并且将index=0作为未查询到的帖子的计数
                index=monitoring_boards_keys.index(str(invalid_post.fidOrStid))+1
            except:
                index=0
            cnt_of_invalid_posts_in_board[index]=cnt_of_invalid_posts_in_board[index]+1

        post_stats=post_stats_db_manager.PostStats(
            date=date,total_new_posts=cnt_of_new_posts,total_deleted_posts=cnt_of_invalid_posts,
            board1_new_posts=cnt_of_new_posts_in_board[1],board1_deleted_posts=cnt_of_invalid_posts_in_board[1],
            board2_new_posts=cnt_of_new_posts_in_board[2],board2_deleted_posts=cnt_of_invalid_posts_in_board[2],
            board3_new_posts=cnt_of_new_posts_in_board[3],board3_deleted_posts=cnt_of_invalid_posts_in_board[3],
            board4_new_posts=cnt_of_new_posts_in_board[4],board4_deleted_posts=cnt_of_invalid_posts_in_board[4],
            board5_new_posts=cnt_of_new_posts_in_board[5],board5_deleted_posts=cnt_of_invalid_posts_in_board[5],
            board6_new_posts=cnt_of_new_posts_in_board[6],board6_deleted_posts=cnt_of_invalid_posts_in_board[6],
            board7_new_posts=cnt_of_new_posts_in_board[7],board7_deleted_posts=cnt_of_invalid_posts_in_board[7],
            board8_new_posts=cnt_of_new_posts_in_board[8],board8_deleted_posts=cnt_of_invalid_posts_in_board[8],
            board9_new_posts=cnt_of_new_posts_in_board[9],board9_deleted_posts=cnt_of_invalid_posts_in_board[9],
            board10_new_posts=cnt_of_new_posts_in_board[10],board10_deleted_posts=cnt_of_invalid_posts_in_board[10],
            )
        update_or_add_post_result=post_stats_db_manager.update_or_add_post(post_stats)
        print_if(f"帖子统计存档：{date}，新贴数量：{cnt_of_new_posts}，被删帖数量：{cnt_of_invalid_posts}。state: {update_or_add_post_result}",3 if update_or_add_post_result else 2    )


def cycle_static():
    '''循环帖子统计器'''
    while RUN_CYCLE_STAT:
        static()
        time.sleep(60)
