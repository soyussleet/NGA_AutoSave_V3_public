'''
帖子数据每日统计
'''

from utils import setting_manager as setting
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Boolean, DateTime, ForeignKey,Date,exc  
from sqlalchemy.orm import scoped_session, sessionmaker, relationship  
from sqlalchemy.ext.declarative import declarative_base  
from utils.print_if import print_if
import time
  
# 数据库连接信息  
DB_USER = setting.get('DB_USER')  
DB_PASSWORD = setting.get('DB_PASSWORD')  
DB_HOST = setting.get('DB_HOST')
DB_PORT = setting.get('DB_PORT')  
DB_NAME = setting.get('DB_NAME')  
TABLE_NAME = setting.get('TABLE_NAME_post_stats')
  
# 创建数据库引擎  
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")  
  
# 创建基类  
Base = declarative_base()  
# 创建所有未创建的表  
Base.metadata.create_all(engine)  
  
# 使用scoped_session来为每个线程创建独立的Session  
session_factory = sessionmaker(bind=engine)  
Session = scoped_session(session_factory)  


query_db_retry_cnt_limit:int=setting.get("queryDbRetryCntLimit")
#post_db_valid_state_retry_cnt_limit:int=setting.get("postDbValidStateRetryCntLimit")

# 定义monitoring_posts表的ORM模型  
class PostStats(Base):  
    __tablename__ = TABLE_NAME  
      
    id = Column(Integer, primary_key=True, autoincrement=True)  # 假设你有一个主键ID，这里添加了它  
    date = Column(Date, nullable=False, comment='日期')  
    total_new_posts = Column(Integer, nullable=False, comment='总新增帖子数')  
    total_deleted_posts = Column(Integer, nullable=False, comment='总被删除帖子数')  
    board1_new_posts = Column(Integer, comment='版面1的新增帖子数')  
    board1_deleted_posts = Column(Integer, comment='版面1的被删除帖子数')  
    board2_new_posts = Column(Integer, comment='版面2的新增帖子数')  
    board2_deleted_posts = Column(Integer, comment='版面2的被删除帖子数')  
    board3_new_posts = Column(Integer, comment='版面3的新增帖子数')  
    board3_deleted_posts = Column(Integer, comment='版面3的被删除帖子数')  
    board4_new_posts = Column(Integer, comment='版面4的新增帖子数')  
    board4_deleted_posts = Column(Integer, comment='版面4的被删除帖子数')  
    board5_new_posts = Column(Integer, comment='版面5的新增帖子数')  
    board5_deleted_posts = Column(Integer, comment='版面5的被删除帖子数')  
    board6_new_posts = Column(Integer, comment='版面6的新增帖子数')  
    board6_deleted_posts = Column(Integer, comment='版面6的被删除帖子数')  
    board7_new_posts = Column(Integer, comment='版面7的新增帖子数')  
    board7_deleted_posts = Column(Integer, comment='版面7的被删除帖子数')  
    board8_new_posts = Column(Integer, comment='版面8的新增帖子数')  
    board8_deleted_posts = Column(Integer, comment='版面8的被删除帖子数')  
    board9_new_posts = Column(Integer, comment='版面9的新增帖子数')  
    board9_deleted_posts = Column(Integer, comment='版面9的被删除帖子数')  
    board10_new_posts = Column(Integer, comment='版面10的新增帖子数')  
    board10_deleted_posts = Column(Integer, comment='版面10的被删除帖子数')  

    def __init__(self, date:Date, total_new_posts:int, total_deleted_posts:int,  
                 board1_new_posts=0, board1_deleted_posts=0,  
                 board2_new_posts=0, board2_deleted_posts=0,  
                 board3_new_posts=0, board3_deleted_posts=0,  
                 board4_new_posts=0, board4_deleted_posts=0,  
                 board5_new_posts=0, board5_deleted_posts=0,  
                 board6_new_posts=0, board6_deleted_posts=0,  
                 board7_new_posts=0, board7_deleted_posts=0,  
                 board8_new_posts=0, board8_deleted_posts=0,  
                 board9_new_posts=0, board9_deleted_posts=0,  
                 board10_new_posts=0, board10_deleted_posts=0): 
        self.date = date  
        self.total_new_posts = total_new_posts  
        self.total_deleted_posts = total_deleted_posts  
        self.board1_new_posts = board1_new_posts  
        self.board1_deleted_posts = board1_deleted_posts  
        self.board2_new_posts = board2_new_posts  
        self.board2_deleted_posts = board2_deleted_posts  
        self.board3_new_posts = board3_new_posts  
        self.board3_deleted_posts = board3_deleted_posts  
        self.board4_new_posts = board4_new_posts  
        self.board4_deleted_posts = board4_deleted_posts  
        self.board5_new_posts = board5_new_posts  
        self.board5_deleted_posts = board5_deleted_posts  
        self.board6_new_posts = board6_new_posts  
        self.board6_deleted_posts = board6_deleted_posts  
        self.board7_new_posts = board7_new_posts  
        self.board7_deleted_posts = board7_deleted_posts  
        self.board8_new_posts = board8_new_posts  
        self.board8_deleted_posts = board8_deleted_posts  
        self.board9_new_posts = board9_new_posts  
        self.board9_deleted_posts = board9_deleted_posts  
        self.board10_new_posts = board10_new_posts  
        self.board10_deleted_posts = board10_deleted_posts  

def update_or_add_post(stat_info:PostStats): 
    """更新或增加记录"""
    session = Session()  # 使用scoped_session获取当前线程的Session 
    is_success=False
    try:  
        # 尝试获取已存在的记录  
        existing_post = session.query(PostStats).filter_by(date=stat_info.date).first()  
        if existing_post:  
            # 如果存在，则更新部分属性  
            for key, value in stat_info.__dict__.items():  
                # 排除SQLAlchemy的内部属性和未设置的属性（即值为默认值的属性）  
                if key not in ['_sa_instance_state'] and value is not None:  
                    current_value = getattr(existing_post, key, None)  
                    # 比较两个值，取较大值并设置  
                    if isinstance(current_value, int) and isinstance(value, int):  
                        setattr(existing_post, key, max(current_value, value))   
                session_result=session.flush()  # 提交更改到数据库，但不关闭session  
                print_if(f"post_stats_db_manager update post:{session_result}")
        else:  
            # 如果不存在，则添加新记录  
            session_result=session.add(stat_info) 
            print_if(f"post_stats_db_manager add post:{session_result}")
        is_success=True
        session.commit()  # 最终提交整个事务  
    except Exception as e:  
        print_if(f"post_stats_db_manager.update_or_add_post: {e}",2)
        session.rollback()  # 如果发生异常，回滚事务  
        # raise e  # 重新抛出异常  
    finally:  
        Session.remove()  # 从线程局部存储中移除session，但不关闭它 
    return is_success


def query_all_stats()->list[PostStats]:  
    
    """查询所有记录"""
    session = Session()  # 使用scoped_session获取当前线程的Session  

    stats:PostStats = None  
    retry_cnt = 0  
    try:  
        while retry_cnt < query_db_retry_cnt_limit:  
            try:  
                stats = session.query(PostStats).all()
                break  # 如果查询成功，则跳出循环  
            except exc.OperationalError as e:  
                # 捕获OperationalError异常，并重试  
                print_if(f"query_all_posts时发生错误：{e}，正在重试...（剩余尝试次数：{query_db_retry_cnt_limit - retry_cnt - 1}）", 1)  
                retry_cnt += 1  
                if retry_cnt < query_db_retry_cnt_limit:  
                    time.sleep(1)  # 根据需要调整retry_delay的值  
                else:  
                    # 所有重试都失败了，可以抛出异常或者返回None  
                    print_if(f"query_all_posts时所有重试都已失败，无法查询帖子。",2)  
                    # 这里可以选择抛出异常或返回None，这里我们保持返回None  
            session.rollback()
  
    finally:  
        Session.remove()  # 从线程局部存储中移除session，但不关闭它  
  
    return stats  # 返回查询结果或None 

