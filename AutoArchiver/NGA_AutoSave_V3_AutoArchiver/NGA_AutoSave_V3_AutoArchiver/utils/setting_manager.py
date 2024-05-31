'''
设置管理器
'''

from email.policy import default
from utils import m_paths
import json  
import os
  
setting_path=m_paths.setting_json_path
setting_template_path=m_paths.setting_template_json_path


# 缓存设置项的字典  
settings_cache = {}  
  
def load_settings(setting_path=setting_path):  
    """从JSON文件加载设置到缓存字典"""  
    global settings_cache
    
    # 如果没有settings，则从template复制过来
    if not os.path.exists(setting_path):  
        with open(setting_template_path, 'rb') as source_file:  
            with open(setting_path, 'wb') as dest_file:  
                dest_file.write(source_file.read())  
        print(f"文件已从 {setting_template_path} 复制到 {setting_path}") 

    # 读取setting文件
    with open(setting_path, 'r',encoding='utf-8') as f:  
        settings_cache = json.load(f)  
    return settings_cache  
  
def save_settings(setting_path=setting_path):  
    """将缓存字典中的设置保存到JSON文件"""  
    global settings_cache  
    with open(setting_path, 'w',encoding='utf-8') as f:  
        json.dump(settings_cache, f)  
  
def get(key:str,default=None):  
    """从缓存字典中获取设置值"""  
    global settings_cache  
    return settings_cache.get(key,default)  
  
def update(key, value):  
    """更新缓存字典中的设置值，并保存到JSON文件"""  
    global settings_cache  
    settings_cache[key] = value  
    save_settings()  
  
# 初始化设置缓存  
load_settings()
