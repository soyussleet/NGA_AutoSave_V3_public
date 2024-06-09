from django.shortcuts import render
from django.http import HttpResponse, Http404  
from misc.utils import setting_manager
import os
import markdown
# Create your views here.

base_path =setting_manager.get("saveFileBaseFolderAtServer")

def saved_files_serve(request):  
    '''获得留档文件，支持md渲染'''
    link=request.GET.get("link")
    full_path=os.path.join(base_path,link)

    if not os.path.exists(full_path):  
        raise Http404("File not found")  
    
    # 根据文件扩展名判断是否需要转换为 HTML  
    _, ext = os.path.splitext(full_path) 
    if ext.lower() == '.md':  
        with open(full_path, 'r', encoding='utf-8') as fh:  
            markdown_content = fh.read()  
            html_content = markdown.markdown(markdown_content, safe_mode='escape')  
            print(f"html_content:{html_content}")
            response = HttpResponse(html_content, content_type='text/html; charset=utf-8') 
            return response 
    else:  
        with open(full_path, 'rb') as fh:  
            response = HttpResponse(fh.read())  
            response['Content-Disposition'] = 'inline; filename="%s"' % os.path.basename(full_path)  
            return response


def test(request):
    return HttpResponse(f"Hello,World!{request}")