import os
from unittest import mock
import xml.etree.ElementTree as et
import pytest
import pandas as pd
from src.core.labeller import Labeller


# Mock data for XML parsing
valid_item_xml = """<Items>
    <Item id="1">
        <Description>Tomato</Description>
        <CaseQty>10</CaseQty>
        <CaseUOM>kg</CaseUOM>
        <PakQty>1</PakQty>
        <PakUOM>kg</PakUOM>
        <InventoryGroup>Vegetables</InventoryGroup>
    </Item>
</Items>"""

empty_xml = """<Items></Items>"""

invalid_xml = """<Items><Item id="1"><Description>Tomato</InvalidTag></Items>"""

@pytest.fixture
def mock_valid_item_xml(tmp_path):
    """Fixture to create a temporary valid XML file."""
    d = tmp_path / "data"
    d.mkdir()
    file = d / "Items.xml"
    file.write_text(valid_item_xml)
    return str(d)

@pytest.fixture
def mock_empty_xml(tmp_path):
    """Fixture to create a temporary empty XML file."""
    d = tmp_path / "data"
    d.mkdir()
    file = d / "Items.xml"
    file.write_text(empty_xml)
    return str(d)

@pytest.fixture
def mock_invalid_xml(tmp_path):
    """Fixture to create a temporary invalid XML file."""
    d = tmp_path / "data"
    d.mkdir()
    file = d / "Items.xml"
    file.write_text(invalid_xml)
    return str(d)


# Edge Case Tests
def test_labeller_with_valid_data(mock_valid_item_xml):
    """Test Labeller with valid XML input."""
    labeller = Labeller([mock_valid_item_xml], restaurant="Test Restaurant")
    assert not labeller.items.empty, "Items DataFrame should not be empty."
    assert labeller.items.shape[0] == 1, "There should be 1 item in the DataFrame."

def test_labeller_with_empty_data(mock_empty_xml):
    """Test Labeller with empty XML input."""
    labeller = Labeller([mock_empty_xml], restaurant="Test Restaurant")
    assert labeller.items.empty, "Items DataFrame should be empty."

def test_labeller_with_invalid_xml(mock_invalid_xml):
    """Test Labeller with invalid XML input."""
    with pytest.raises(et.ParseError):
        Labeller([mock_invalid_xml], restaurant="Test Restaurant")

def test_labeller_file_not_found():
    """Test Labeller when XML file is not found."""
    with pytest.raises(FileNotFoundError):
        Labeller(['/invalid/path'], restaurant="Test Restaurant")


# Mutation Tests (tests with slight changes in input)
def test_labeller_with_missing_attributes_in_xml(mock_valid_item_xml, tmp_path):
    """Test Labeller with XML that has missing attributes."""
    missing_attr_xml = """<Items><Item id="1"></Item></Items>"""
    d = tmp_path / "data"
    d.mkdir(exist_ok=True)
    file = d / "Items.xml"
    file.write_text(missing_attr_xml)
    
    labeller = Labeller([str(d)], restaurant="Test Restaurant")
    print(labeller.items)
    assert labeller.items.empty, "DataFrame should be empty when attributes are missing."


def test_labeller_with_extra_attributes_in_xml(mock_valid_item_xml, tmp_path):
    """Test Labeller with extra attributes in XML."""
    extra_attr_xml = """<Items>
    <Item id="1" extra="yes">
        <Description>Tomato</Description>
        <CaseQty>10</CaseQty>
        <CaseUOM>kg</CaseUOM>
        <PakQty>1</PakQty>
        <PakUOM>kg</PakUOM>
        <InventoryGroup>Vegetables</InventoryGroup>
    </Item>
</Items>"""
    d = tmp_path / "data"
    d.mkdir(exist_ok=True)
    file = d / "Items.xml"
    file.write_text(extra_attr_xml)
    
    labeller = Labeller([str(d)], restaurant="Test Restaurant")
    assert labeller.items.shape[0] == 1, "Items DataFrame should have 1 row even with extra attributes."


def test_labeller_with_non_numeric_values_in_numeric_fields(mock_valid_item_xml, tmp_path):
    """Test Labeller with non-numeric values in numeric fields."""
    non_numeric_xml = """<Items>
    <Item id="1">
        <Description>Tomato</Description>
        <CaseQty>non_numeric</CaseQty>
        <CaseUOM>kg</CaseUOM>
        <PakQty>1</PakQty>
        <PakUOM>kg</PakUOM>
        <InventoryGroup>Vegetables</InventoryGroup>
    </Item>
</Items>"""
    d = tmp_path / "data"
    d.mkdir(exist_ok=True)
    file = d / "Items.xml"
    file.write_text(non_numeric_xml)
    
    labeller = Labeller([str(d)], restaurant="Test Restaurant")
    assert labeller.items.iloc[0]['CaseQty'] == 'non_numeric', "CaseQty should hold the non-numeric value as string."


# Test for __str__ and __repr__
def test_labeller_repr(mock_valid_item_xml):
    """Test __repr__ output of Labeller."""
    labeller = Labeller([mock_valid_item_xml], restaurant="Test Restaurant")
    repr_output = repr(labeller)
    assert "Labeller FOR Test Restaurant" in repr_output
    assert "Items: 1" in repr_output

def test_labeller_str(mock_valid_item_xml):
    """Test __str__ output of Labeller."""
    labeller = Labeller([mock_valid_item_xml], restaurant="Test Restaurant")
    str_output = str(labeller)
    assert "Labeller FOR Test Restaurant" in str_output
    assert "Items: 1" in str_output
