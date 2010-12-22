from django.db.models.base import ModelBase
from django.db.models.signals import post_save

from pubsub.utils import handle_post_save

class PubSub(object):
    """
    Manages models to be published

    registry is a list of registered models
    """
    def __init__(self, registry=None):
        self.registry = registry or []
        self.registry = set(self.registry)

    def register(self, model_or_iterable):
        """
        Registers single model or an iterable containing models
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            self.registry.add(model)
            post_save.connect(handle_post_save, sender=model)

pubsub = PubSub()
