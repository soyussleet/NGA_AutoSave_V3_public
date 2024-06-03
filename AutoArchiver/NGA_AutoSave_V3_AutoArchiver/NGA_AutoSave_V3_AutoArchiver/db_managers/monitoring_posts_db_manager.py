'''
帖子数据库
'''

from utils import setting_manager as setting
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Boolean, DateTime, ForeignKey,exc  
from sqlalchemy.orm import scoped_session, sessionmaker, relationship  
from sqlalchemy.ext.declarative import declarative_base  
from utils.print_if import print_if
import time
from datetime import date, datetime, timedelta
  
# 数据库连接信息  
DB_USER = setting.get('DB_USER')  
DB_PASSWORD = setting.get('DB_PASSWORD')  
DB_HOST = setting.get('DB_HOST')
DB_PORT = setting.get('DB_PORT')  
DB_NAME = setting.get('DB_NAME')  
TABLE_NAME = setting.get('TABLE_NAME_monitoring_posts')
  
# 创建数据库引擎  
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")  
  
# 创建基类  
Base = declarative_base()  
# 创建所有未创建的表  
Base.metadata.create_all(engine)  
  
# 使用scoped_session来为每个线程创建独立的Session  
session_factory = sessionmaker(bind=engine)  
Session = scoped_session(session_factory) 
session= session_factory()


  
query_db_retry_cnt_limit:int=setting.get("queryDbRetryCntLimit")
post_db_valid_state_retry_cnt_limit:int=setting.get("postDbValidStateRetryCntLimit")

# 定义monitoring_posts表的ORM模型  
class MonitoringPost(Base):  
    __tablename__ = TABLE_NAME  
      
    tid = Column(Integer, primary_key=True)  
    tidTitle = Column(String, nullable=False)  
    savedFilePath = Column(String, nullable=False)  
    poster = Column(String, nullable=False)  
    posterUrl=Column(String, nullable=False) 
    posterLocation=Column(String, nullable=False) 
    validState = Column(Integer, nullable=False)  # 1：正常；2：被锁；3：超时进坟；4：主动过滤
    lastPage = Column(Integer, nullable=False)  
    repliesCnt = Column(Integer, nullable=False)
    firstPostTime = Column(DateTime, nullable=False)  
    finalReplayTime = Column(DateTime, nullable=False)   
    fidOrStid = Column(String, nullable=False)  
    retryCnt = Column(Integer, nullable=False)   
    anonymousPoster = Column(Boolean, nullable=False)  

    def toString(self):
        return (  
            f"\n"
            f"tid             : {self.tid}\n"  
            f"tidTitle        : {self.tidTitle}\n"  
            f"savedFilePath   : {self.savedFilePath}\n"  
            f"poster          : {self.poster}\n"  
            f"posterUrl       : {self.posterUrl}\n" 
            f"posterLocation  : {self.posterLocation}\n" 
            f"validState      : {self.validState}\n"  
            f"lastPage        : {self.lastPage}\n"  
            f"repliesCnt      : {self.repliesCnt}\n"  
            f"firstPostTime   : {self.firstPostTime.strftime('%Y-%m-%d %H:%M:%S')}\n"  
            f"finalReplayTime : {self.finalReplayTime.strftime('%Y-%m-%d %H:%M:%S')}\n" 
            f"fidOrStid       : {self.fidOrStid}\n"  
            f"retryCnt        : {self.retryCnt}\n"   
            f"anonymousPoster : {self.anonymousPoster}\n"  
        )
      
    # 根据需要添加其他关系或方法  
  
tidFilterValidState=setting.get("tidFilterValidState")
  
 

def query_all_posts()->list[MonitoringPost]:  
    
    """查询所有记录"""
    session = Session()  # 使用scoped_session获取当前线程的Session  

    posts:MonitoringPost = None  
    retry_cnt = 0  
    try:  
        while retry_cnt < query_db_retry_cnt_limit:  
            try:  
                posts = session.query(MonitoringPost).all()
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
  
    return posts  # 返回查询结果或None 

# 查询函数  
def query_by_tid(tid: int)->MonitoringPost:  
    """使用tid查询"""  
    session = Session()  # 使用scoped_session获取当前线程的Session  
    post = None  
    retry_cnt = 0  
    post:MonitoringPost=None
    try:  
        while retry_cnt < query_db_retry_cnt_limit:  
            try:  
                post = session.query(MonitoringPost).filter_by(tid=tid).first()  
                if post is not None:  
                    print_if(f"tid={tid}的数据库记录查询成功: {post.toString()}")
                    break  # 如果查询成功，则跳出循环  
                else:  
                    print_if(f"tid={tid}的数据库未查询到")
                    # 如果没有找到对应的记录，但连接正常，返回None或者做其他处理  
                    break  
            except exc.OperationalError as e:  
                # 捕获OperationalError异常，并重试  
                print_if(f"查询tid={tid}时发生错误：{e}，正在重试...（剩余尝试次数：{query_db_retry_cnt_limit - retry_cnt - 1}）", 1)  
                retry_cnt += 1  
                if retry_cnt < query_db_retry_cnt_limit:  
                    # 在这里可以添加一些延迟逻辑，比如time.sleep，以避免过快地重试  
                    time.sleep(1)  # 根据需要调整retry_delay的值  
                else:  
                    # 所有重试都失败了，可以抛出异常或者返回None  
                    print_if(f"查询tid={tid}时所有重试都已失败，无法查询帖子。",2)  
                    # 这里可以选择抛出异常或返回None，这里我们保持返回None  
            session.rollback()
  
    finally:  
        Session.remove()  # 从线程局部存储中移除session，但不关闭它  
  
    return post  # 返回查询结果或None 
  
def query_by_title(substring:str):  
    session = Session()  # 使用scoped_session获取当前线程的Session  
    try:  
        posts = session.query(MonitoringPost).filter(  
            MonitoringPost.tidTitle.like(f'%{substring}%')  
        ).all()  
        return posts  
    finally:    
        Session.remove()  # 从线程局部存储中移除session，但不关闭它 
  
def query_by_poster(substring:str):  
    session = Session()  # 使用scoped_session获取当前线程的Session  
    try:  
        posts = session.query(MonitoringPost).filter(MonitoringPost.poster.like(f'%{substring}%')).all()  
        return posts  
    finally:    
        Session.remove()  # 从线程局部存储中移除session，但不关闭它 
  
def query_by_valid_state(valid_state:int):  
    session = Session()  # 使用scoped_session获取当前线程的Session  
    try:  
        posts = session.query(MonitoringPost).filter_by(validState=valid_state).all()  
        return posts  
    finally:    
        Session.remove()  # 从线程局部存储中移除session，但不关闭它 
  
def query_by_anonymous_poster(anonymous:bool):  
    session = Session()  # 使用scoped_session获取当前线程的Session  
    try:  
        posts = session.query(MonitoringPost).filter_by(anonymousPoster=anonymous).all()  
        return posts  
    finally:    
        Session.remove()  # 从线程局部存储中移除session，但不关闭它 
      
def update_or_add_post(post:MonitoringPost): 
    """更新或增加记录"""
    session = Session()  # 使用scoped_session获取当前线程的Session 
    post=valid_state_judge(post)
    try:  
        # 尝试获取已存在的记录  
        existing_post = session.query(MonitoringPost).filter_by(tid=post.tid).first()  
        if existing_post:  
            # 如果存在，则更新部分属性  
            for key, value in post.__dict__.items():  
                # 排除SQLAlchemy的内部属性和未设置的属性（即值为默认值的属性）  
                if key not in ['_sa_instance_state'] and value is not None:  
                    setattr(existing_post, key, value)  
                session_result=session.flush()  # 提交更改到数据库，但不关闭session  
                print_if(f"monitoring_posts_db_manager update post:{session_result}")
        else:  
            # 如果不存在，则添加新记录  
            session_result=session.add(post) 
            print_if(f"monitoring_posts_db_manager add post:{session_result}")
        session.commit()  # 最终提交整个事务  
    except Exception as e:  
        print_if(f"monitoring_posts_db_manager.update_or_add_post: {e}",2)
        session.rollback()  # 如果发生异常，回滚事务  
        # raise e  # 重新抛出异常  
    finally:  
        Session.remove()  # 从线程局部存储中移除session，但不关闭它 

# 删除函数  
def delete_post(tid:int):  
    session = Session()  # 使用scoped_session获取当前线程的Session  
    try:  
        post = session.query(MonitoringPost).filter_by(tid=tid).first()  
        if post:  
            session.delete(post)  
            session.commit() 
    finally:  
        Session.remove()  # 从线程局部存储中移除session，但不关闭它 
        
def valid_state_judge(post:MonitoringPost)->MonitoringPost:
    """当帖子访问失败时，先retryCnt+1，当大于5时设置validState=2。当validState==1时retryCnt=0"""
    if(post.validState==1):
        post.retryCnt=0
    elif(post.validState==2):
        if(int(post.retryCnt)<post_db_valid_state_retry_cnt_limit):
            post.validState=1
            post.retryCnt+=1
        else:
            post.validState=2
            post.retryCnt=0
    else:
        pass
    return post

def get_posts_by_first_post_time(target_date:date=datetime.now().date()-timedelta(days=1), session=Session())->list[MonitoringPost]:  
    '''查询所有firstPostTime在指定日期内的记录，默认为昨天'''
    # 获取目标日期的开始和结束时间  
    start_of_day = datetime.combine(target_date, datetime.min.time())  
    end_of_day = datetime.combine(target_date, datetime.max.time())  
      
    # 查询所有firstPostTime在指定日期内的记录  
    posts = session.query(MonitoringPost).filter(  
        MonitoringPost.firstPostTime >= start_of_day,  
        MonitoringPost.firstPostTime <= end_of_day  
    ).all()  
      
    return posts  
  
def get_posts_by_valid_state_and_final_replay_time(target_date:date=datetime.now().date()-timedelta(days=1), valid_state=2, session=Session())->list[MonitoringPost]:  
    '''查询所有validState等于指定值且finalReplayTime在指定日期内的记录，默认为昨天且validState=2'''
    # 获取目标日期的开始和结束时间  
    start_of_day = datetime.combine(target_date, datetime.min.time())  
    end_of_day = datetime.combine(target_date, datetime.max.time())  
      
    # 查询所有validState等于指定值且finalReplayTime在指定日期内的记录  
    posts = session.query(MonitoringPost).filter(  
        MonitoringPost.validState == valid_state,  
        MonitoringPost.finalReplayTime >= start_of_day,  
        MonitoringPost.finalReplayTime <= end_of_day  
    ).all()  
      
    return posts  