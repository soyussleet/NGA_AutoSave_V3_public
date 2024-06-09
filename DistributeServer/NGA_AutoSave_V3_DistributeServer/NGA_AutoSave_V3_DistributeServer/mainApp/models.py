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


class PostStats(models.Model):  
    id = models.AutoField(primary_key=True)  # Django默认的主键  
    date = models.DateField(null=False, db_index=True)  # 添加db_index提高查询效率  
    total_new_posts = models.IntegerField(null=False, default=0)  
    total_deleted_posts = models.IntegerField(null=False, default=0)  
    board1_new_posts = models.IntegerField(null=True, blank=True, default=0)  
    board1_deleted_posts = models.IntegerField(null=True, blank=True, default=0)  
    board2_new_posts = models.IntegerField(null=True, blank=True, default=0)  
    board2_deleted_posts = models.IntegerField(null=True, blank=True, default=0)  
    board3_new_posts = models.IntegerField(null=True, blank=True, default=0)  
    board3_deleted_posts = models.IntegerField(null=True, blank=True, default=0)  
    board4_new_posts = models.IntegerField(null=True, blank=True, default=0) 
    board4_deleted_posts = models.IntegerField(null=True, blank=True, default=0) 
    board5_new_posts = models.IntegerField(null=True, blank=True, default=0) 
    board5_deleted_posts = models.IntegerField(null=True, blank=True, default=0)  
    board6_new_posts = models.IntegerField(null=True, blank=True, default=0) 
    board6_deleted_posts = models.IntegerField(null=True, blank=True, default=0) 
    board7_new_posts = models.IntegerField(null=True, blank=True, default=0) 
    board7_deleted_posts = models.IntegerField(null=True, blank=True, default=0) 
    board8_new_posts = models.IntegerField(null=True, blank=True, default=0) 
    board8_deleted_posts = models.IntegerField(null=True, blank=True, default=0)  
    board9_new_posts = models.IntegerField(null=True, blank=True, default=0) 
    board9_deleted_posts = models.IntegerField(null=True, blank=True, default=0) 
    board10_new_posts = models.IntegerField(null=True, blank=True, default=0) 
    board10_deleted_posts = models.IntegerField(null=True, blank=True, default=0) 
  
    # 如果你需要确保date字段的唯一性，可以添加unique_together  
    class Meta:  
        db_table = 'post_stats'
        unique_together = [['date']]  # 这实际上不是一个复合主键，只是确保date字段的唯一性  
  
    # 其他可能的模型方法，如save(), delete()的覆盖等  
  
    def __str__(self):  
        return f"帖子统计存档：{self.date}，新贴数量：{self.total_new_posts}，被删帖数量：{self.total_deleted_posts}。"