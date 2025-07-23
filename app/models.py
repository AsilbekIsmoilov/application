from django.db import models



class Operator(models.Model):
    fio = models.CharField(max_length=255, blank=True, null=True)
    operator_id = models.CharField(max_length=10, blank=True, null=True)
    rank = models.IntegerField(default=0)
    daily_status = models.CharField(max_length=100, blank=True, null=True)
    monthly_status = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.fio or f"Operator {self.id}"



class Theme(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title




class RequestLog(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.SET_NULL, null=True)
    theme = models.ForeignKey(Theme,on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=13)
    num_app = models.CharField(max_length=50)
    service_id = models.CharField(max_length=10)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 

    def __str__(self):
        return f"Оператор: {self.operator} --- Номер абонента: {self.phone_num} --- Дата: {self.created_at.strftime('%d.%m.%Y')}"




class Urls(models.Model):
    icons = models.ImageField(upload_to="icons/",blank=True)
    title = models.CharField(max_length=150,blank=True, null=True)
    url = models.URLField(max_length=250,blank=True,null=True)

    def __str__(self):
        return self.title
