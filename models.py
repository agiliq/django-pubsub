from django.db import models
from django.db.models.signals import post_save

from pubsub import pubsub
from pubsub.utils import publish_handler

for model in pubsub.registry:
    post_save.connect(publish_handler, sender=model)
