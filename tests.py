"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User

from pubsub import pubsub
from blogango.models import BlogEntry, BlogRoll

class PubSubTest(TestCase):
    def test_registration(self):
        """
        Test that models are registered with pubsub
        """
        models = [BlogEntry, BlogRoll]
        pubsub.register(models)
        self.assertTrue(set(models).issubset(pubsub.registry))

    def test_publish(self):
        """
        Test message is published when registered models
        are created/updated
        """
        spiderman = User.objects.create(username="spiderman", password="mary_jane")
        BlogEntry.objects.create(title="Spam Blog", text="This is BlogSpam", created_by=spiderman)
