from datetime import datetime, timedelta
import os
from random import Random
from urllib.request import Request
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse,StreamingHttpResponse
from mainApp.models import MonitoringPosts,PostStats
from misc.utils import setting_manager
from django.db.models import Q
from pyecharts.charts import Line  
from pyecharts import options as opts  

# 监控中的版面
monitoringBoards:dict[str,str]=setting_manager.get("monitoringBoards")
monitoring_board_values=["总体"]
monitoring_board_values=monitoring_board_values+list(monitoringBoards.values())
monitoring_board_values = monitoring_board_values + ['未知版面'] * (11 - len(monitoring_board_values)) 
# print(f'monitoring_board_values:{monitoring_board_values}')
per_page=setting_manager.get("show_posts_per_page",100)
saveFileBaseFolder:str=setting_manager.get("saveFileBaseFolderAtServer")

def dbGetAll(request:HttpRequest):
    '''获得所有帖子，并可以筛选'''
    search_query = request.GET.get('dbAllSearch', '')  
    only_deleted = request.GET.get('only_deleted', '') 
    print(f"search_query:{search_query}  , only_deleted:{only_deleted}")
    if search_query:  
        # 使用icontains来执行不区分大小写的搜索  
        monitoring_posts = MonitoringPosts.objects.filter(  
            Q(tid__icontains=search_query) |  
            Q(tidTitle__icontains=search_query) |  
            Q(poster__icontains=search_query)  
        )  
        
    else:  
        # 如果没有搜索查询，则获取所有帖子（或根据你的需求进行筛选）  
        monitoring_posts = MonitoringPosts.objects.all()  
    if only_deleted=="on" :  
        print("仅筛选被删除的帖子")
        monitoring_posts = monitoring_posts.filter(validState=2)  
        
    monitoring_posts=monitoring_posts.order_by("-tid")


    #monitoring_posts=MonitoringPosts.objects.all().order_by("-tid")
    valid_state_choices = {  
        1: "正常",  
        2: "被锁",  
        3: "超时但仍暂存",  
        4: "超时删除前最后访问",  
        5: "确认超时",
        6: "确认超时并删除存档",
        7: "连续数次无法访问"
    }  
    i=0
    for post in monitoring_posts:  
        post.num=i
        i=i+1
        if(post.retryCnt>0):
            post.validState=7
        post.validStateDisplay = valid_state_choices.get(post.validState, "未知状态")
        post.board = monitoringBoards.get(post.fidOrStid, "未知版面") 
        
    # 分页处理
    paginator = Paginator(monitoring_posts, per_page)  
    page_number = request.GET.get('page',1)  
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    page_number_int=int(page_number)
    # 生成页面数字范围
    page_range=range(page_number_int-5 if page_number_int-5>0 else 1,page_number_int+5 if page_number_int+5<=paginator.num_pages+1 else paginator.num_pages+1)
    print(f"page_range: {page_range}")
    # 上下文变量  
    context = {  
        'monitoring_posts': page_obj,  
        # 添加额外的上下文变量以用于分页链接  
        'paginator': paginator,  
        'page_obj': page_obj,  
        'page_range':page_range,
        'search_query': search_query,  # 传递给模板以便显示搜索词  
        'only_deleted': only_deleted  # 传递给模板以便显示筛选条件 
    }  
    print (only_deleted)
    return render(request, 'allPosts.html', context)

def postStat(request:HttpRequest):
    '''帖子统计'''

    date_start = request.GET.get('dateStart')
    date_end = request.GET.get('dateEnd')  
    if date_start and date_end:
        try:  
            start_date = datetime.strptime(date_start, '%Y-%m-%d')  
            end_date = datetime.strptime(date_end, '%Y-%m-%d')  
        except ValueError:  
            # 如果日期格式不正确，返回错误  
            return JsonResponse({'error': 'Invalid date format'}, status=400)  
    else:
        start_date=datetime.now().date()
        end_date=start_date- timedelta(days=7)
    # print("==============postStat=============")
    # print(f"start_date:{start_date}, end_date:{end_date}")

    # 查询数据库  
    stats = PostStats.objects.filter(date__range=(start_date, end_date)).order_by('date')  
    dates = [stat.date for stat in stats]  
        
    new_posts:list[list[int]]=[]
    deleted_posts:list[list[int]]=[]
    new_posts.append([stat.total_new_posts for stat in stats])
    deleted_posts.append([stat.total_deleted_posts for stat in stats])  
    new_posts.append([stat.board1_new_posts for stat in stats])  
    deleted_posts.append([stat.board1_deleted_posts for stat in stats])  
    new_posts.append([stat.board2_new_posts for stat in stats])  
    deleted_posts.append([stat.board2_deleted_posts for stat in stats])  
    new_posts.append([stat.board3_new_posts for stat in stats])  
    deleted_posts.append([stat.board3_deleted_posts for stat in stats])  
    new_posts.append([stat.board4_new_posts for stat in stats])  
    deleted_posts.append([stat.board4_deleted_posts for stat in stats])  
    new_posts.append([stat.board5_new_posts for stat in stats])  
    deleted_posts.append([stat.board5_deleted_posts for stat in stats])  
    new_posts.append([stat.board6_new_posts for stat in stats])  
    deleted_posts.append([stat.board6_deleted_posts for stat in stats])  
    new_posts.append([stat.board7_new_posts for stat in stats])  
    deleted_posts.append([stat.board7_deleted_posts for stat in stats])  
    new_posts.append([stat.board8_new_posts for stat in stats])  
    deleted_posts.append([stat.board8_deleted_posts for stat in stats])  
    new_posts.append([stat.board9_new_posts for stat in stats])  
    deleted_posts.append([stat.board9_deleted_posts for stat in stats])  
    new_posts.append([stat.board10_new_posts for stat in stats])  
    deleted_posts.append([stat.board10_deleted_posts for stat in stats])  
    
    # 初始化折线图  
    line = (  
        Line(init_opts=opts.InitOpts(width="100%", height="100%"))  
        .add_xaxis(dates)  
        .set_global_opts(  
            title_opts=opts.TitleOpts(title="帖子统计", pos_left="center", pos_top="0%"),  
            legend_opts=opts.LegendOpts(is_show=True, pos_left="center", pos_top="5%"),  # 显示图例  
            toolbox_opts=opts.ToolboxOpts(is_show=True),  # 显示工具箱，包括保存图表、数据视图切换等  
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),  # 提示框配置项  
        )  
    ) 
    
    for i in range(0,11,1):
        if sum(new_posts[i])+sum(deleted_posts[i])==0:
            continue    
        line.add_yaxis(f"{monitoring_board_values[i]} 新帖子", new_posts[i], label_opts=opts.LabelOpts(is_show=False))
        line.add_yaxis(f"{monitoring_board_values[i]} 删除帖子", deleted_posts[i], label_opts=opts.LabelOpts(is_show=False))
        

    # 将图表渲染为HTML字符串  
    html_content = line.render_embed()  
  
    # print(f"postStat  html_content:{html_content}")
    context={
        'chart_html': html_content,
    }
    # 渲染模板并返回响应  
    return render(request, 'postStats.html', context)

def getPostRecord(request:HttpRequest):
    '''获取帖子存档'''    
    tid=request.GET.get("tid")
    file_links_for_tid = get_file_links_for_tid(tid)
    if isinstance(file_links_for_tid, str):  
        return HttpResponse(f"tid={tid} 请求失败，{file_links_for_tid}")
    context={
    }
    context.update(file_links_for_tid)
    print(f"context:{context}")
    return render(request, 'getPostRecord.html', context)


def get_file_links_for_tid(tid): 
    '''获取留档文件'''
    # 获取文件夹
    if not tid:
        return "未输入tid"
    sub_folder= MonitoringPosts.objects.all().filter(tid=int(tid))[0].savedFilePath
    tid_folder=f"{saveFileBaseFolder}/{sub_folder}"
    tid_path = os.path.join(tid_folder)  
    '''
    print(f"当前工作目录是: {os.getcwd() }")
    print(f"tid_path: {tid_path}")
    print(f"os.path.abspath(tid_path) :{os.path.abspath(tid_path) }")
    print(f"os.listdir(tid_path):{os.listdir(tid_path)}")
    '''

    # 获取文件
    if os.path.exists(tid_path):  
        files = [f for f in os.listdir(tid_path) if os.path.isfile(os.path.join(tid_path, f))]  
        file_links:list[dict[str,str]] = []  
        for file in files:  
            # 假设文件可以直接通过URL访问，例如静态文件或通过特定视图提供  
            # 这里我们简单构建一个静态文件的URL作为示例  
            file_url = f'{sub_folder}/{file}'  # 需要确保URL正确，并且文件实际可访问  
            file_links.append({'name': file, 'url': file_url})  
        # print(f"file_links:{file_links}")
        return {
            "file_links":file_links,
            "folder_name":sub_folder
            } 
    else:  
        return "无此tid对应帖子"  

def test(request):
    return HttpResponse(f"Hello,World!{request}")
