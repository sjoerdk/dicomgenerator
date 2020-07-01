#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from pydicom.dataelem import DataElement
from pydicom.tag import BaseTag, Tag

from dicomgenerator.factory import CTDatasetFactory, DataElementFactory
from factory import random


@pytest.fixture
def fix_random_seed():
    """Make sure tests using Faker will have reproducible results"""
    random.reseed_random("fixed random seed")


def test_factory():
    """Check whether dataset factory actually generates datasets
    """
    generated = CTDatasetFactory()
    assert generated.SeriesDate == generated.AcquisitionDate
    assert CTDatasetFactory(AccessionNumber="1234").AccessionNumber == "1234"


def test_factory_random(fix_random_seed):
    """Test reproducibility of randomized tests

    Kind of a meta test as it tests pytest and factory instead of my own code.
    Still, I want to make sure this works"""
    dataset = CTDatasetFactory()
    assert str(dataset.PatientName) == "van Ooyen^Fiene"


@pytest.mark.parametrize(
    "tagpwc,expected_vr, expected_value",
    [
        ("PatientName", "PN", "van Ooyen^Fiene"),
        (0x00100010, "PN", "van Ooyen^Fiene"),
        ("AcquisitionTime", "TM", "184146.928"),
        (
            "SeriesInstanceUID",
            "UI",
            "1.2.826.0.1.3680043.10.404.1018842105998743551928118404590099790",
        ),
        ("PatientBirthDate", "DA", "20121108"),
        ("Rows", "US", 41990),
    ],
)
def test_data_element_factory_argument(
    fix_random_seed, tag, expected_vr, expected_value
):
    """Try to create a DataElementFactory of several types
    """

    element = DataElementFactory(tag=tag)
    assert element.tag == Tag(tag)
    assert element.VR == expected_vr
    assert element.value == expected_value


def test_data_element_factory_init():
    """factory does slightly iffy casting of string to Tag(). Verify that this works
    """
    assert type(DataElementFactory().tag) == BaseTag
    assert type(DataElement(tag="Modality", VR="SH", value="kees").tag) == BaseTag
    assert type(DataElementFactory(tag="Modality").tag) == BaseTag
    assert type(DataElementFactory(tag=(0x0010, 0x0020)).tag) == BaseTag


def test_data_element_factory_exceptions(fix_random_seed):

    with pytest.raises(ValueError):
        DataElementFactory(tag="unknown_tag")
