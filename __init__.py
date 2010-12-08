from django.db.models.base import ModelBase

class PubSub(object):
    """
    Manages models to be published
    """
    def __init__(self, registry=None):
        self.registry =  registry or []
        
    def register(self, model_or_iterable):
        """
        Registers single model or an iterable containing models
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            self.registry.append(model)

pubsub = PubSub()
