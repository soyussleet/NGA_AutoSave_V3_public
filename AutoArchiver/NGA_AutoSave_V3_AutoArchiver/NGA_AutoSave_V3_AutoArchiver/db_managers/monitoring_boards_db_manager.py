'''
监控版面数据库
'''

from utils import setting_manager as setting
from sqlalchemy import create_engine, MetaData, Table, select  
from sqlalchemy.orm import sessionmaker  
  
# 数据库连接信息  
DB_USER = setting.get('DB_USER')  
DB_PASSWORD = setting.get('DB_PASSWORD')  
DB_HOST = setting.get('DB_HOST')
DB_PORT = setting.get('DB_PORT')  
DB_NAME = setting.get('DB_NAME')  
TABLE_NAME = setting.get('TABLE_NAME_monitoring_boards')

# 公共变量，用于存储从数据库读取的数据  
boards_data = [] 
  
# 创建数据库引擎  
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")  
  
# 创建会话类  
Session = sessionmaker(bind=engine)  
  
# 获取元数据和表  
metadata = MetaData()  
monitoring_boards_table = Table(TABLE_NAME, metadata, autoload_with=engine)  
  
# 读取所有 fidOrStid 和 fidTitle，并返回字典列表  
def read_all_boards_data():  
    '''读取所有 fidOrStid 和 fidTitle，并返回字典列表'''
    global boards_data  
    with Session() as session:  
        result = session.execute(select(monitoring_boards_table.c.fidOrStid, monitoring_boards_table.c.fidTitle))  
        boards_data = [{"fid_or_stid": row[0], "fid_title": row[1]} for row in result]  
        return boards_data  
  
# 插入数据  
def insert_data(fid_or_stid, fid_title): 
    '''插入 fid_or_stid'''
    with Session() as session:  
        insert_stmt = monitoring_boards_table.insert().values(fidOrStid=fid_or_stid, fidTitle=fid_title)  
        session.execute(insert_stmt)  
        session.commit()  
    boards_data.append({"fid_or_stid": fid_or_stid, "fid_title": fid_title})  
  
# 更新数据  
def update_data(fid_or_stid, new_fid_title):   
    '''更新fid_or_stid''' 
    with Session() as session:  
        update_stmt = monitoring_boards_table.update().where(monitoring_boards_table.c.fidOrStid == fid_or_stid).values(fidTitle=new_fid_title)  
        session.execute(update_stmt)  
        session.commit()  
    for item in boards_data:  
        if item['fid_or_stid'] == fid_or_stid:  
            item['fid_title'] = new_fid_title  
            break  
  
# 删除数据  
def delete_data(fid_or_stid):  
    '''删除fid_or_stid'''
    with Session() as session:  
        delete_stmt = monitoring_boards_table.delete().where(monitoring_boards_table.c.fidOrStid == fid_or_stid)  
        session.execute(delete_stmt)  
        session.commit()  
    boards_data = [item for item in boards_data if item['fid_or_stid'] != fid_or_stid]  
    
# 从boards_data读取数据，返回所有fid_or_stid组成的数组  
def get_all_fid_or_stid():  
    '''返回所有fid_or_stid组成的数组'''
    return [item['fid_or_stid'] for item in boards_data]  

# 读取给定fid对应的标题，如果boards_data中没有，则先更新boards_data  
def read_title_of_fid(fid):  
    '''读取给定fid对应的标题'''
    # 尝试从boards_data中直接读取  
    for item in boards_data:  
        if item['fid_or_stid'] == fid:  
            return item['fid_title']  
  
    # 如果没有找到，则更新boards_data  
    read_all_boards_data()  
  
    # 再次尝试查找  
    for item in boards_data:  
        if item['fid_or_stid'] == fid:  
            return item['fid_title']  
  
    # 如果仍然找不到，则返回None  
    return None

# 初始加载
read_all_boards_data()
