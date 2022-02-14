from django.db import models
from model_utils.models import TimeStampedModel

from pylon.users.models import User

from .middleware import get_current_user

class StampedModel(TimeStampedModel):
    created_by = models.ForeignKey(User,
        related_name='%(class)s_created_by',
        blank=True,
        null=True,
        on_delete=models.CASCADE)

    modified_by = models.ForeignKey(User,
        related_name='%(class)s_modified_by',
        blank=True,
        null=True,
        on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        
        user = get_current_user()
        
        if user:
            self.modified_by = user
            if not self.id:
                self.created_by = user
        super(StampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True    