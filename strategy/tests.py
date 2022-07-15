from audioop import reverse
from datetime import datetime
from django.test import TestCase
from .models import TradeData
from django.urls import reverse

# Create your tests here.


class ModelTest(TestCase):
    def test_models(self):
        data = TradeData.objects.create(
            datetime=datetime.now(),
            close=22.2,
            high=22.2,
            low=22.2,
            open=22.2,
            volume=2222,
            instrument="ABC",
        )
        # print(data.datetime)
        self.assertEqual(type(data.datetime), datetime)
        self.assertEqual(type(data.close), float)
        self.assertEqual(type(data.high), float)
        self.assertEqual(type(data.low), float)
        self.assertEqual(type(data.open), float)
        self.assertEqual(type(data.volume), int)
        self.assertEqual(type(data.instrument), str)
