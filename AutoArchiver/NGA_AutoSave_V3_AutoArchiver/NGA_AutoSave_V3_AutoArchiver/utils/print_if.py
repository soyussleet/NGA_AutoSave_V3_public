"""
带分类别（等级）显示的print
"""
from datetime import datetime
from utils import setting_manager
group_show=setting_manager.get("logGroupShow")
group_name=setting_manager.get("logGroupName")
group_name_show=setting_manager.get("logGroupNameShow")
add_time=setting_manager.get("printIfAddTime")

latest_print_time=datetime.now()

def print_if(message,group=0,need_stage_time=True):
    """
    带分类别（等级）显示的print，默认分类为0
    可以在setting.json的logGroup中修改显示分类
    分类: 0:通用, 1:警告, 2:错误, 3:成功, 4:零碎（通常不显示）; 5:阶段标题; 6:临时
    need_stage_time:bool，代表是否需要记录时间，以判断下载循环卡死
    
    """ 
    global latest_print_time
    if need_stage_time:
        latest_print_time=datetime.now()
    formatted_now=datetime.now().strftime("%Y/%m/%d %H:%M:%S:%f")[:-3] if(add_time) else ""

    add_text=group_name[group] if group_name_show and group>=0 and group<len(group_name) else ""
    if(group in group_show):
        print(f"{add_text} {formatted_now} : {message}\n")
        
def print_passed_time(new_time:datetime|None=None):
    '''距离上一次打印输出时间'''
    if new_time== None:
        new_time=datetime.now()
    global latest_print_time
    print_if(f"new_time: {new_time} , latest_print_time:{latest_print_time}",6,False)
    return (new_time-latest_print_time).total_seconds()

