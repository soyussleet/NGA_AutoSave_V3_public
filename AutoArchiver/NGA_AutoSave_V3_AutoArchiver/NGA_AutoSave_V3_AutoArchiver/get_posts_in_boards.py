'''
获取监控中的版面中的帖子，并且获得一些基础信息
主要调用get_posts_in_boards()
'''


from datetime import datetime
from bs4 import BeautifulSoup
from db_managers.monitoring_posts_db_manager import query_by_tid,query_all_posts,MonitoringPost
from utils import setting_manager
from utils.print_if import print_if
from utils.m_requests import MRequests

filter_title=setting_manager.get("tidFilterTitle")
filter_state=setting_manager.get("tidFilterValidState")
ngaBaseUrl=setting_manager.get("ngaBaseUrl")
  
def get_posts_in_boards()->list[MonitoringPost]:
    '''获取监控中的版面的帖子'''
    
    # 数据库中现有的帖子，先行查询用于避免重复获取发帖人IP
    posts_in_db=query_all_posts()

    # 获取所有的 fid 或 stid，去setting查。
    fid_or_stid_list:list=[]
    fid_or_stid_list = list(setting_manager.get("monitoringBoards").keys())

    # 将记录作为列表元素
    posts_in_boards_list:list[MonitoringPost]=[]
    post_cnt=0

    # 遍历 fid 或 stid 列表  
    for fid_or_stid in fid_or_stid_list:  
        # 构造 URL  
        url = f"{ngaBaseUrl}/thread.php?{fid_or_stid}"  
      
        # 发送 GET 请求  
        response = MRequests(url).easy_get()
      
        # 检查请求是否成功  
        if response.status_code == 200:  
            # 打印响应内容  
            #print(response.text)  
            posts_in_boards_page1=extract_post_info(response.text,fid_or_stid)
            post_cnt+=len(posts_in_boards_page1)
            print_if(f"版面{fid_or_stid}已添加{len(posts_in_boards_page1)}条帖子")
            posts_in_boards_list.append(posts_in_boards_page1)
        else:  
            print_if(f"Failed to access {url}. Status code: {response.status_code}",2)

    # 加入原数据库记录的posts_in_boards
    
    post_cnt+=len(posts_in_db)
    print_if(f"数据库中原已添加{len(posts_in_db)}条帖子")
    posts_in_boards_list.append(posts_in_db)
    # post去除重复和不可用帖子
    posts_in_boards=posts_in_boards_list_deduplicat(posts_in_boards_list)
    print_if(f"监控版面和数据库中原有{post_cnt}条帖子，去除重复和不可用后有{len(posts_in_boards)}条帖子\n",3)

    # print_if (posts_in_boards,4)
    return posts_in_boards

def filter_dictionary(post, **kwargs):  
    """  
    过滤字典，检查是否包含任何与给定关键字参数值相同的字段。  
      
    :param dictionary: 要检查的字典  
    :param kwargs: 要过滤的关键字-过滤值数组参数  
    :return: 如果字典不包含任何与关键字参数值相同的字段，则返回True；否则返回False。  
    
    使用样例: 
    exclude_tids = ['exclude_tid0', 'exclude_tid1', 'exclude_tid2'] # 待过滤的值
    exclude_posters = ['exclude_poster0', 'exclude_poster1']
    if filter_dictionary(post, tid=exclude_tids, poster=exclude_posters): 
        post_info.append(new_dict)  
    """   
    for key, value_list in kwargs.items():  
        if getattr(post,key) is not None:
            field_value = str(getattr(post,key))  # 确保字段值是字符串类型以便进行子串检查  
            if any(str_value in field_value for str_value in value_list):  
                return False  # 如果找到匹配项（即字段值是某个值的子串），则不添加字典  
    return True  # 如果没有找到匹配项，则添加字典  

def extract_post_info(html,fid_or_stid="")->list[MonitoringPost]: 
    '''html解析'''

    soup = BeautifulSoup(html, 'html.parser')  
    post_rows = soup.find_all('tr', class_=['row1 topicrow', 'row2 topicrow'])  
    post_info = []  
  
    for post_row in post_rows:  
        '''
        # 查找回帖数量的<a>标签  ，因为需要保存至md，所以不在构建时赋值
        replies_elem = post_row.find('a', class_='replies')  
        replies_cnt = replies_elem.text if replies_elem else None  
        '''
  
        # 查找帖子标题的<a>标签  
        title_elem = post_row.find('a', class_='topic')  
        tid_title = title_elem.text.strip() if title_elem else None  
        tid_url = title_elem['href'] if title_elem else None
        tid_url=tid_url.split('&')[-1]
        tid = tid_url.split('=')[-1] if tid_url else None  
  
        # 查找发帖者的<a>标签  
        poster_elem = post_row.find('a', class_='author')  
        poster = poster_elem.text.strip() if poster_elem else None  
        # 获取发帖者的IP
        poster_url = poster_elem['href'] if poster_elem else ""
        
  
        # 查找首次发帖时间  
        first_post_time_elem = post_row.find('span', class_='silver postdate')  
        first_post_time_str = first_post_time_elem.text.strip() if first_post_time_elem else None    
        try:
            first_post_time_datetime=datetime.fromtimestamp(int(first_post_time_str)) 
        except:
            first_post_time_datetime=datetime.fromtimestamp(0)
  
        # 查找最后回复时间  
        final_replay_time_elem = post_row.find('a', class_='silver replydate')  
        final_replay_time_str = final_replay_time_elem.text.strip() if final_replay_time_elem else None 
        try:
            final_replay_time_datetime=datetime.fromtimestamp(int(final_replay_time_str)) 
        except:
            final_replay_time_datetime=datetime.fromtimestamp(0)
        
        # 是否匿名用户
        # anonymous_tag = post_row.find('b', class_='block_txt', attrs={'title': '这是一个匿名用户'})  
        # anonymous_poster = 1 if anonymous_tag else 0 
        anonymous_poster=False
        if poster.find("#anony")>=0:
            anonymous_poster=True
  
        # 收集信息  
        existing_post:MonitoringPost=query_by_tid(tid)
        if(existing_post==None):
            existing_post=MonitoringPost()
        existing_post.tid=tid if existing_post.tid is None else existing_post.tid
        existing_post.tidTitle=tid_title if existing_post.tidTitle is None else existing_post.tidTitle
        existing_post.savedFilePath="" if existing_post.savedFilePath is None else existing_post.savedFilePath
        existing_post.poster=poster if existing_post.poster is None else existing_post.poster
        existing_post.posterUrl=poster_url if existing_post.posterUrl is None else existing_post.posterUrl
        existing_post.validState=1 # if existing_post.validState is None else existing_post.validState # 当帖子出现在首页时，其必然为可用的（可能会被主动过滤），因此这里不采用数据库中记录的validState
        existing_post.lastPage=1 if existing_post.lastPage is None else existing_post.lastPage
        existing_post.repliesCnt=-1 if existing_post.repliesCnt is None else existing_post.repliesCnt # 因为帖子0楼也是有意义的，所以定义为-1以将其定为无意义
        existing_post.firstPostTime=first_post_time_datetime if existing_post.firstPostTime is None else existing_post.firstPostTime
        existing_post.finalReplayTime=final_replay_time_datetime if existing_post.finalReplayTime is None else existing_post.finalReplayTime
        existing_post.fidOrStid=fid_or_stid if existing_post.fidOrStid is None else existing_post.fidOrStid
        existing_post.retryCnt=0 if existing_post.retryCnt is None else existing_post.retryCnt
        existing_post.anonymousPoster=anonymous_poster if existing_post.anonymousPoster is None else existing_post.anonymousPoster
        
        if filter_dictionary(existing_post, tidTitle=filter_title, validState=filter_state):  
            post_info.append(existing_post)
            #print(f"帖子tid:{tid}, 标题:{tid_title}, 回帖数量:{replies_cnt}, 版面id:{fid_or_stid}")
    return post_info  


def posts_in_boards_list_deduplicat(post_list_list: list[list[MonitoringPost]]) -> list:  
    """
    post数组去重结合，并且去除validState不在useableValidArr的帖子
    输入参数为一个列表，列表的每一个元素为一个列表post_list
    post_list的每一个元素为一个post:MonitoringPost
    遍历post_list_list中的post_list中的post。
    当post.tid重复时，优先保留post_list_list下标靠前的post_list中的
    """
    post_operated = []  # 存储去重后的MonitoringPost对象  
    added_tid = set()  # 存储已经添加过的tid  

    useableValidArr=setting_manager.get("useableValidArr")
    
    # 遍历post_list_list中的每个post_list  
    for post_list in post_list_list:  
        # 遍历post_list中的每个MonitoringPost对象  
        for post in post_list:  
            # 如果post的tid不在added_tid中，并且validState在允许下载的useableValidArr中，则添加到post_operated和added_tid  
            if (post.tid not in added_tid) and (post.validState in useableValidArr) and filter_dictionary(post, tidTitle=filter_title, validState=filter_state):  
                post_operated.append(post)  
                added_tid.add(post.tid)  
  
    return post_operated  

#aaa=get_posts_in_boards()
#print(aaa)