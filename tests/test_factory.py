#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


from dicomgenerator.factory import CTDatasetFactory
from factory import random


@pytest.fixture
def fix_random_seed():
    """Make sure tests using Faker will have reproducible results"""
    random.reseed_random('fixed random seed')


def test_factory():
    """Check whether dataset factory actually generates datasets
    """
    generated = CTDatasetFactory()
    assert generated.SeriesDate == generated.AcquisitionDate
    assert CTDatasetFactory(AccessionNumber='1234').AccessionNumber == '1234'


def test_factory_random(fix_random_seed):
    """Test reproducibility of randomized tests

    Kind of a meta test as it tests pytest and factory instead of my own code.
    Still, I want to make sure this works"""
    dataset = CTDatasetFactory()
    assert str(dataset.PatientName) == "van Ooyen^Fiene"
