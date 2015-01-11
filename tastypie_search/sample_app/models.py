""" Sample Models demonstrate searchable resources.
"""
from django.db import models

class USState(models.Model):
    """ US state codes are the primary key, e.g. 'ME', Maine.
    The PK appears as a human readable code in the foreign key.
    """
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'US State'
        verbose_name_plural = 'US States'
        ordering = [ 'name' ]

    def __unicode__(self):
        return self.name

class Capitol(models.Model):
    """ A US State Capitol City
    Its CapitolModelResource has a searchable
    `history` and related `state` name.
    """
    name = models.CharField(max_length=100)
    state = models.ForeignKey(USState)
    history = models.TextField(default='')

    def __unicode__(self):
        return u'%s, %s' % (self.name, self.state.code)

