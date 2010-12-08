"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from pubsub import pubsub
from blogango.models import Blog, BlogRoll

class PubSubTest(TestCase):
    def test_registration(self):
        """
        Test that models are registered with pubsub
        """
        pubsub.register([Blog, BlogRoll])

