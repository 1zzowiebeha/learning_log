from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class CommonInfo(models.Model):
    """Date fields that can be included via subclassing
    CommonInfo."""
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Topic(CommonInfo):
    """A topic the user is learning about."""
    content = models.TextField(verbose_name="Topic name")
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return a string that represents the topic."""
        return self.content


class TopicHourData(models.Model):
    topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE)
    hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="hours spent with topic",
        default=0,
        max_length=100_000,
    )

    created_on = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"hours for {self.topic.content}"
    
    class Meta:
        ordering = ["topic", "hours"]
        
        
class Entry(CommonInfo):
    """An entry for a topic."""
    content = models.TextField(verbose_name="Entry text")
    topic = models.ForeignKey(to=Topic,
                              on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'entries'
        ordering = ["content"]

    def __str__(self) -> str:
        """Return the entry's contents, truncated via an ellipsis
        if over 50 characters. Used in the admin panel."""
        ellipsis = '...' if len(self.content) > 50 else ''
        return f"{self.content[:50]}{ellipsis}"