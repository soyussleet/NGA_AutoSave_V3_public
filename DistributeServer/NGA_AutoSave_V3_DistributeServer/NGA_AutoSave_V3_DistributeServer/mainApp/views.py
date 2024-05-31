from urllib.request import Request
from django.shortcuts import render # type: ignore
from django.core.paginator import Paginator # type: ignore
from django.http import HttpRequest, HttpResponse# type: ignore
from mainApp.models import MonitoringPosts
from misc.utils import setting_manager
from django.db.models import Q  # type: ignore

monitoringBoards=setting_manager.get("monitoringBoards")
per_page=setting_manager.get("show_posts_per_page",100)


def dbGetAll(request:HttpRequest):
    response=''
    search_query = request.GET.get('dbAllSearch', '')  
    only_deleted = request.GET.get('only_deleted', '') 
    print(f"search_query:{search_query}  , only_deleted:{only_deleted}")
    if search_query:  
        # 使用icontains来执行不区分大小写的搜索  
        # 假设TID、标题、发帖人字段分别是tid、title、poster  
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
        post.sharp=i
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



def test(request):
    return HttpResponse(f"Hello,World!{request}")
