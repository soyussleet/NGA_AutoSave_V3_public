"""
html转md
"""

from bs4 import BeautifulSoup  
import os,re
from requests import Response  

from utils import setting_manager
from utils.m_requests import MRequests
from utils.print_if import print_if


ngaBaseUrl=setting_manager.get("ngaBaseUrl")
imgBaseUrl=setting_manager.get("imgBaseUrl")
  
class PostExtractor:  

    

    def __init__(self, html_content:str|bytes|Response):
        if isinstance(html_content,Response):
            html_content=html_content.text 
        self.soup = BeautifulSoup(html_content, 'html.parser') 
        self.final_floor:int=0
  
    def extract_posts(self, last_latest_floor=0)->list[dict]:  
        replays: list[dict] = []  
        for tr in self.soup.find_all('tr', class_=lambda c: c and 'postrow' in c):  
            floor_id = tr.get('id').split('row')[1]  
            floor_num = int(floor_id) 
            self.final_floor=floor_num
            # 跳过所有已经保存过的回复，以确保不会重复保存到md中
            # 新帖子时的last_latest_floor应当为-1，所以也不会跳过
            if floor_num <= last_latest_floor : 
                continue  
  
            author_link = tr.find('a', class_='author b')['href']  
            author_link=f"{ngaBaseUrl}/{author_link}"
            post_time = tr.find('span', id=lambda id: id and 'postdate' in id).get_text(strip=True)  
            post_content=""
            try:
                post_content = tr.find('span', class_='postcontent ubbcode').get_text(strip=True, separator='\n')  
            except Exception as e:
                try:
                    post_content = tr.find('p', class_='postcontent ubbcode').get_text(strip=True, separator='\n') 
                except Exception as e:
                    print_if(f"无法获取楼层内容：{e}")

            # 处理正文的图片链接
            img_regex = r'\[img\]./(.*?)\[/img\]'  
            matches = re.finditer(img_regex, post_content)  
            for match in matches:  
                # 移除'./'并拼接完整的URL  
                part_img_url=match.group(1)
                full_img_url = f"{imgBaseUrl}/{part_img_url}"  
                # 替换原始链接为 Markdown 图片语法  
                replacement = f'![标题]({full_img_url})'  
                post_content = post_content.replace(match.group(0), replacement)  


            replays.append({  
                'floor_num': floor_num,  
                'author_link': author_link,  
                'post_time': post_time,  
                'post_content': post_content  
            })  
  
        return replays  
  
    def save_to_md(self, replays, post_title:str,post_tid:int, md_path:str,last_latest_floor=0):  
        if not os.path.exists(md_path) and last_latest_floor == -1:  
            with open(md_path, 'w', encoding='utf-8') as f:  
                f.write(f'# {post_title}\n')  
                f.write(f'# {ngaBaseUrl}/read.php?tid={post_tid}\n\n')  

  
        with open(md_path, 'a', encoding='utf-8') as f:  
            for replay in replays:  
                f.write(f'## \# {replay["floor_num"]}\n')  
                f.write(f'### 发帖人链接\n')  
                f.write(f'{replay["author_link"]}\n\n')  
                f.write(f'### 发帖时间\n')  
                f.write(f'{replay["post_time"]}\n\n')  
                f.write(f'### 帖子内容\n')  
                f.write(f'```\n{replay["post_content"]}\n```\n\n')  

    def extract_and_save_md(self,post_title:str,post_tid:int, md_path:str,last_latest_floor=-1):
        """将帖子内容保存为md文件"""
        replays = self.extract_posts(last_latest_floor)
        self.save_to_md(replays,post_title,post_tid, md_path,last_latest_floor)
        return self.final_floor
  
'''
html_content=MRequests("https://bbs.nga.cn/read.php?tid=40068540").easy_get()
# 实例化类并调用方法  
extractor = PostExtractor(html_content)  
posts = extractor.extract_posts(last_latest_floor=0)  # 假设我们只想获取楼层7及以上的帖子  
title = "示例帖子标题"  # 这里需要传入帖子的标题  
md_path = "output.md"  # 指定md文件路径  
extractor.save_to_md(posts, title, md_path,last_latest_floor=0) 
'''