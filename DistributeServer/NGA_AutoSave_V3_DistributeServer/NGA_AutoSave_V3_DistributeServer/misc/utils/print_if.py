"""
带分类别（等级）显示的print
"""
from utils import setting_manager
group_show=setting_manager.get("logGroupShow")
group_name=setting_manager.get("logGroupName")
group_name_show=setting_manager.get("logGroupNameShow")


def print_if(message,group=0):
    """
    带分类别（等级）显示的print，默认分类为0
    可以在setting.json的logGroup中修改显示分类
    分类: 0:通用, 1:警告, 2:错误, 3:成功, 4:零碎（通常不显示）; 5:阶段标题; 6:临时
    """ 
    add_text=group_name[group] if group_name_show and group>=0 and group<len(group_name) else ""
    if(group in group_show):
        print(f"{add_text}{message}\n")

