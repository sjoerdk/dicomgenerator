#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from dicomgenerator.factory import CTDatasetFactory, DataElementFactory
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


def test_data_element_factory(fix_random_seed):

    element = DataElementFactory(tag='PatientName')
    assert element.VR == 'PN'
    assert element.value == "van Ooyen^Fiene"


def test_data_element_factory_argument(fix_random_seed):

    element = DataElementFactory(tag=0x00100010)
    assert element.VR == 'PN'
    assert element.value == "van Ooyen^Fiene"


def test_data_element_factory_rest(fix_random_seed):

    element2 = DataElementFactory(tag='AcquisitionTime')
    assert element2.VR == 'TM'
    assert element2.value == '184146.928'

    element3 = DataElementFactory(tag='SeriesInstanceUID')
    assert element3.VR == 'UI'
    assert element3.value == (
        '1.2.826.0.1.3680043.10.404.3499455237445106102360603272897163423')

    element4 = DataElementFactory(tag='PatientBirthDate')
    assert element4.VR == 'DA'
    assert element4.value == '20120511'



