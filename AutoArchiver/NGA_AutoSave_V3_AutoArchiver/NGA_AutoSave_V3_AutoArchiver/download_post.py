'''
下载一个帖子里的页面，会从最后一次记录的页面开始下载
'''

from datetime import date, datetime
from bs4 import BeautifulSoup
from db_managers.monitoring_posts_db_manager import MonitoringPost  
from db_managers import monitoring_posts_db_manager 
from utils import setting_manager
import re,os
from utils.print_if import print_if
from utils.m_requests import MRequests
from requests import Response
from utils.nga_html_to_md import PostExtractor


ngaBaseUrl=setting_manager.get("ngaBaseUrl")
tidBaseUrl=setting_manager.get("tidBaseUrl")

class DownloadPostOperator:
    def __init__(self,post_outline:monitoring_posts_db_manager.MonitoringPost):
        self.post_outline=post_outline

    def sanitize_filename(self,filename):  
        """标准化路径"""
        # 创建一个转换表，将非法字符映射为空格  
        trans_table = str.maketrans({k: '' for k in '&#<>:"|?*'})  
        # 使用转换表清理文件名  
        filename_sanitized=filename.translate(trans_table)
        return filename_sanitized

    def parse_post_time(self,html):  
        '''最后帖子时间处理'''
        soup = BeautifulSoup(html, 'html.parser')  
        # 假设最后一条回复的div总是最后一个拥有postInfo类的div  
        last_post_info_div = soup.find_all('div', class_='postInfo')[-1]  
        post_time_span = last_post_info_div.find('span', title='reply time')
        
        if post_time_span:  
            post_time_str = post_time_span.text.strip()+":00"   
            post_time = datetime.strptime(post_time_str, '%Y-%m-%d %H:%M:%S')  
            return post_time  
        else:  
            return None  

    
    def page_process(self,html_block:str)->str:
        '''
        保存页面处理

        1.删除<div id="mainmenu">
        2.类似<a href="/read.php?tid=37965650&page=4" class=" uitxt1" title="" onclick="null">&nbsp;4&nbsp;</a>这样的以/read.php?作为链接开头的的页面跳转链接修改为本地文件连接，如<a href="tid=37965650&page=4"
        3.将非以/read.php?开头的链接导向nga（前缀https://bbs.nga.cn），如将<a href="/thread.php?fid=860" class="nav_link" data-fb="167772168">音乐类游戏讨论</a>改为<a href="https://bbs.nga.cn/thread.php?fid=860" class="nav_link" data-fb="167772168">音乐类游戏讨论</a>
        4.将
        "
        <script type="text/javascript">
        //loadscriptstart
        var __CURRENT_UID = parseInt('65496420',10),
        __NOW = 1711523119,
        __CURRENT_UNAME = '用户名',
        __CACHE_PATH = './data/bbscache',
        "
        中的__CURRENT_UNAME置为空字符串
        '''

        # 创建BeautifulSoup对象  
        soup = BeautifulSoup(html_block, 'html.parser')  
  
        # 1. 删除<div id="mainmenu">  
        mainmenu_div = soup.find(id='mainmenu')  
        if mainmenu_div:  
            mainmenu_div.decompose()  
  
        # 2. 修改链接，废弃不做了
        '''  
        hrefs = soup.find_all('a', href=True)  
        for a_tag in hrefs:  
            href = a_tag['href']  
            if '/read.php' in href:  
                # 如果链接包含/read.php，则移除/read.php?及其前面的部分  
                new_href = href.split('/read.php?')[1] if '?' in href else href.split('/read.php')[1]  
                a_tag['href'] = new_href  
            elif 'http' not in href:  
                # 否则，在链接前面加上'https://bbs.nga.cn/'  
                #a_tag['href'] = 'https://bbs.nga.cn/' + href  
                a_tag['href'] = f'{ngaBaseUrl}/{href}' 
        '''
  
        # 4. 将__CURRENT_UNAME置为空字符串  
        for script in soup.find_all('script'):  
            # 寻找包含__CURRENT_UNAME的行，并将其设置为空字符串  
            script_text = str(script)  
            if '__CURRENT_UNAME' in script_text:  
                new_script_text = script_text.replace('__CURRENT_UNAME = \'用户名\'', '__CURRENT_UNAME = \'\'')  
                script.string.replace_with(BeautifulSoup(new_script_text, 'html.parser').string)  
  
        return soup.prettify() 

    #def get_poster_location(tid:int,poster_url:str,posts_in_db:list[MonitoringPost])->str:
    def get_poster_location(self)->str:
        """获取帖子发帖人的IP属地"""
        post=self.post_outline
        if (post.posterLocation is not None) and (self.post_outline.posterLocation!=""):
            print_if(f"帖子tid={self.post_outline.tid}的发帖人IP已存在于数据库：{self.post_outline.posterLocation}")
            # 如果找到匹配的tid，返回其posterLocation  
            return post.posterLocation 
        elif self.post_outline.posterUrl is None or self.post_outline.posterUrl=="":
            print_if(f"帖子tid={self.post_outline.tid}的无法获取发帖人IP，因为无posterUrl",1)
            return
        full_url = f"{ngaBaseUrl}{self.post_outline.posterUrl}"
        response = MRequests(full_url).easy_get()
        # 使用正则表达式从JavaScript变量中提取ipLoc值  
        pattern = r'"ipLoc":"([^"]+)"'  
        match = re.search(pattern, response.text, re.DOTALL)  
        if match:  
            ip_location = match.group(1)  
            print_if(f"帖子tid={self.post_outline.tid}的发帖人IP已在线获取：{ip_location}")
            return ip_location  
        
        # 如果没有找到IP属地的信息，返回空字符串  
        print_if(f"帖子tid={self.post_outline.tid}的无法获取发帖人IP，posterUrl={self.post_outline.posterUrl}",1)
        return ""  

    def invalid_detector(self,response:Response,url:str):
        """帖子可用性判断"""
        if response.status_code == 200:  
            # NGA帖子的无法访问错误
            match = re.search(r"\(ERROR:<!--msgcodestart-->\d+<!--msgcodeend-->\)", response.text)
            if(match):
                print_if(f"帖子{url}访问失败: {match.group()}",2)
                return False
        else:
            return False
        return True

    def download(self):  
        '''下载网页序列'''  
        post_outline=self.post_outline
        tid_url = f"{tidBaseUrl}{post_outline.tid}" 
        base_url = f"{ngaBaseUrl}/{tid_url}"  
        print_if(f"********尝试下载url {base_url}********\n")  
        has_next_page = True  
        curr_page = int(post_outline.lastPage) if post_outline.lastPage!=None else 1
        final_reply_time:datetime = datetime.now()

        # 文件夹处理
        saveFileBaseFolder:str=setting_manager.get("saveFileBaseFolderAtArchiver")# 基础存档文件夹
        savedFilePath=post_outline.savedFilePath# post_outline中存的存档帖子文件夹
        # 如果post_outline中存的存档帖子文件夹为空，那么生成这个文件夹名
        tid_part=tid_url.split('?')[1]
        if savedFilePath=="" or savedFilePath==None:
            savedFilePath=f"{tid_part}_{post_outline.tidTitle}"
            post_outline.savedFilePath=savedFilePath
        # 完整文件夹名，基础文件夹/帖子文件夹
        folder_name=f"{saveFileBaseFolder}/{savedFilePath}"
        folder_name=self.sanitize_filename(folder_name)
        # 生成文件夹
        if not os.path.exists(folder_name):  
            os.makedirs(folder_name)  

        # 下载网页并保存
        while has_next_page:  

            # 下载网页
            page_url = f"{base_url}&page={curr_page}" if curr_page > 1 else base_url  
            page_html = MRequests(page_url).easy_get()

            # 帖子可用性判断
            if not self.invalid_detector(page_html,tid_url):
                post_outline.validState=2
                break

            # Html处理
            #page_html_text=page_processor.PageProcessor(page_html.text).process()
            page_html_text=self.page_process(page_html.text)
          
            # 构建文件名  
            filename = f"{tid_part}.html" if curr_page == 1 else f"{tid_part}page={curr_page}.html"  
            filename = f"{folder_name}/{filename}"
            

            # 保存文件
            try:  
                
                with open(filename, 'w', encoding='utf-8') as file:  
                    file.write(page_html_text)  
                    print_if(f"网页已成功保存为 {filename}，使用utf-8编码\n",3)  
            except UnicodeEncodeError:  
                print_if(f"网页 {filename}使用utf-8编码保存失败，正在尝试gbk编码保存为\n",1)  
                with open(filename, 'w', encoding='gbk') as file:  
                    file.write(page_html_text)  
                    print_if(f"网页已成功保存为 {filename}，使用gbk编码\n",3)  
            except OSError as e:
                print_if(f"保存网页{filename}时出现错误: {e}",2)

            # 保存为md
            final_floor=PostExtractor(page_html_text).extract_and_save_md(
                post_outline.tidTitle,post_outline.tid,f"{folder_name}/{tid_part}.md",post_outline.repliesCnt)

            # 更新帖子最新回帖数量
            post_outline.repliesCnt=final_floor
          
            # 检查是否存在下一页  
            next_page_pattern = r"<a class=\"pager_spacer\" href=\"(.*?)\" title=\"下一页\">"  
            next_page_match = re.search(next_page_pattern, page_html_text)  
            if not next_page_match:  
                has_next_page = False  
                # 最后回复时间
                final_reply_time:datetime = self.parse_post_time(page_html_text)  
            else:  
                curr_page = curr_page+1 
                print_if(f"{base_url}更新最新页面 {curr_page}\n")  

        # 修改post记录
        post_outline.lastPage=curr_page
        post_outline.finalReplayTime=final_reply_time

        # 如果最后回复时间超时，则进坟
        post_expire:int=setting_manager.get("postExpire")
        save_file_expire_dict:dict=setting_manager.get("saveFileExpire")
        save_file_expire:int=save_file_expire_dict[post_outline.fidOrStid] if post_outline.fidOrStid in save_file_expire_dict else save_file_expire_dict["default"]
        current_time = datetime.now()  
  
        # 计算时间差，以秒为单位  
        time_difference = (current_time - final_reply_time).total_seconds()  
        if time_difference > post_expire and post_outline.validState == 1: 
            # 通常帖子的超时
            post_outline.validState = 3  
            print_if(f"{savedFilePath}已经超时，进坟",1)
        elif time_difference > save_file_expire and post_outline.validState == 4: 
            # 通常帖子的超时
            post_outline.validState = 5  
            print_if(f"{savedFilePath}已经确认超时，即将删除",1)
        else:  
            # 如果没有超过，你可以根据需要设置其他值，或者什么都不做  
            pass  

        # 发帖人IP属地
        post_outline.posterLocation=self.get_poster_location()


        monitoring_posts_db_manager.update_or_add_post(post_outline)

        return post_outline


# 测试用
'''
post:MonitoringPost=MonitoringPost()
post.tidUrl="read.php?tid=39762686"
post.lastPage=1
post.retryCnt=0
download_post_operator=DownloadPostOperator(post) 
operated=download_post_operator.download()
'''


        



    
    
 