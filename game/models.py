from django.db import models

class AuthCode(models.Model):
    code = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    last_login = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.code, self.name)

    class Meta:
        verbose_name = 'AuthCode'
        verbose_name_plural = 'AuthCodes'

class AuthCodeNum(models.Model):
    code = models.IntegerField(default=0)
    name = models.CharField(max_length=255, default='')
    last_login = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.code, self.name)

    class Meta:
        verbose_name = 'AuthCodeNum'
        verbose_name_plural = 'AuthCodeNums'
