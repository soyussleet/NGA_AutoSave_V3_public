'''
m_requests.py
主要是对request的改写，现在可以对一个网页进行多次重试访问
'''


import requests  
from requests import Response
from utils import cookie_format
from utils.print_if import print_if
  
class MRequests:
    """
    使用requests库发送GET请求。
    为了确保线程安全，请每次使用时均进行实例化
    使用样例1：
    response=m_requests.MRequests(url).easy_get()
    使用样例2：
    mRequest=m_requests.MRequests(url)
    response=mRequest.get(retryMax=10)
    """
    def __init__(self,url):
        self.url=url


    def get(self, params=None, retryMax=4, **kwargs)->Response:  
        """  
        使用requests库发送GET请求。若访问失败，最多尝试进行retryMax次重试，默认为4  
  
        参数:  
        url (str): 请求的URL地址  
        params (dict, optional): 请求的参数，默认为None  
        retryCnt (int, optional): 重试次数，默认为0  
  
        返回:  
        requests.Response: 返回requests库的响应对象，无论请求是否成功  
  
        注意:  
        如果请求失败，且重试次数小于retryMax，会递归调用该函数并增加重试次数。  
        当重试次数达到retryMax时，将打印"访问失败，已达到最大重试次数"，并返回None。  
        """
        retryCnt = kwargs.pop('retryCnt', 0)  # 从kwargs中弹出retryCnt，默认为0  
        response=Response()
        try:  
            response:Response = requests.get(self.url, params=params, **kwargs)  
            response.raise_for_status()  # 如果状态不是200, 引发HTTPError异常  
            return response  
        except requests.exceptions.RequestException:  
            if retryCnt < retryMax:  
                retryCnt += 1  
                print_if(f"{self.url}访问失败，进行第{retryCnt}次重试",1)  
                return self.get(params=params, **kwargs, retryMax=retryMax, retryCnt=retryCnt)  # 递归调用，增加retryCnt  
            else:  
                print_if(f"{self.url}访问失败，已达到最大重试次数",2)  
                return response

    def easy_get(self)->Response:
        """  
        使用requests库发送GET请求，添加了默认配置
        """
        return self.get(params=None, retryMax=4, cookies=cookie_format.get_cookies())