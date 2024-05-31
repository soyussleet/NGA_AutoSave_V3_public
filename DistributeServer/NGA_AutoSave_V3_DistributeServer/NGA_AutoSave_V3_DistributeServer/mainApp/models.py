from django.db import models

class MonitoringPosts(models.Model):
    tid = models.IntegerField(primary_key=True)  
    tidTitle = models.CharField(max_length=50)  
    savedFilePath = models.CharField(max_length=255)
    poster = models.CharField(max_length=255)
    posterUrl=models.CharField(max_length=255) 
    posterLocation=models.CharField(max_length=255) 
    validState = models.IntegerField()  # 1：正常；2：被锁；3：超时进坟；4：主动过滤
    lastPage = models.IntegerField()  
    repliesCnt = models.IntegerField()
    firstPostTime = models.DateTimeField()  
    finalReplayTime = models.DateTimeField()   
    fidOrStid = models.CharField(max_length=255)  
    retryCnt = models.IntegerField()   
    anonymousPoster = models.BooleanField()
    
    def toStr(self) -> str:
        return f"""
tid         : {self.tid}\n
title       : {self.tidTitle}\n
poster      : {self.poster}\n
repliesCnt  : {self.repliesCnt}\n
validState  : {self.validState}\n
=====================\n
        """
    def __str__(self) -> str:
        return self.toStr

    class Meta:  
        db_table = 'monitoring_posts'
