import os
import tempfile
from xml.etree.ElementTree import Element, SubElement, ElementTree
import pytest
import pandas as pd
from core.lib.labeller import Labeller  # Adjusted import path to match the project structure

@pytest.fixture
def create_xml_files():
    """Fixture to create temporary XML files for testing."""
    temp_dir = tempfile.TemporaryDirectory()

    # Create Items.xml
    items_xml = Element('Items')
    item = SubElement(items_xml, 'Item', id='123')
    SubElement(item, 'Description').text = 'Item 123'
    SubElement(item, 'CaseQty').text = '10'
    SubElement(item, 'CaseUOM').text = 'kg'
    SubElement(item, 'PakQty').text = '5'
    SubElement(item, 'PakUOM').text = 'g'
    SubElement(item, 'InventoryGroup').text = 'Group A'
    tree = ElementTree(items_xml)
    tree.write(os.path.join(temp_dir.name, 'Items.xml'))

    # Create Ingredients.xml
    ingredients_xml = Element('Ingredients')
    ingredient = SubElement(ingredients_xml, 'Ingredient', ingredient='456', conversion='2', invFactor='1', qty='50', recipe='789', uom='ml')
    tree = ElementTree(ingredients_xml)
    tree.write(os.path.join(temp_dir.name, 'Ingredients.xml'))

    # Create Preps.xml
    preps_xml = Element('Preps')
    prep = SubElement(preps_xml, 'Prep', id='987')
    SubElement(prep, 'Description').text = 'Prep 987'
    SubElement(prep, 'PakQty').text = '20'
    SubElement(prep, 'PakUOM').text = 'ml'
    SubElement(prep, 'InventoryGroup').text = 'Group B'
    tree = ElementTree(preps_xml)
    tree.write(os.path.join(temp_dir.name, 'Preps.xml'))

    # Create Products.xml
    products_xml = Element('Products')
    product = SubElement(products_xml, 'Prod', id='654')
    SubElement(product, 'Description').text = 'Product 654'
    SubElement(product, 'SalesGroup').text = 'Sales A'
    tree = ElementTree(products_xml)
    tree.write(os.path.join(temp_dir.name, 'Products.xml'))

    # Create Conversions.xml
    conversions_xml = Element('Conversions')
    conversion = SubElement(conversions_xml, 'Conversion', id='321', multiplier='1.5')
    convert_from = SubElement(conversion, 'ConvertFrom', qty='100', uom='g')
    convert_to = SubElement(conversion, 'ConvertTo', qty='150', uom='ml')
    tree = ElementTree(conversions_xml)
    tree.write(os.path.join(temp_dir.name, 'Conversions.xml'))

    yield temp_dir.name

    # Teardown: Cleanup temporary files
    temp_dir.cleanup()


def test_read_items(create_xml_files):
    """Test reading Items.xml and creating dataframe."""
    labeller = Labeller([create_xml_files], "Test Restaurant")
    labeller.read_items()
    
    expected_items = pd.DataFrame({
        'ItemId': ['123'],
        'Description': ['Item 123'],
        'CaseQty': ['10'],
        'CaseUOM': ['kg'],
        'PakQty': ['5'],
        'PakUOM': ['g'],
        'InventoryGroup': ['Group A']
    })

    pd.testing.assert_frame_equal(labeller.items, expected_items)


def test_read_ingredients(create_xml_files):
    """Test reading Ingredients.xml and creating dataframe."""
    labeller = Labeller([create_xml_files], "Test Restaurant")
    labeller.read_ingredients()

    expected_ingredients = pd.DataFrame({
        'IngredientId': ['456'],
        'Qty': ['50'],
        'Uom': ['ml'],
        'Conversion': ['2'],
        'InvFactor': ['1'],
        'Recipe': ['789']
    })

    pd.testing.assert_frame_equal(labeller.ingredients, expected_ingredients)


def test_read_preps(create_xml_files):
    """Test reading Preps.xml and creating dataframe."""
    labeller = Labeller([create_xml_files], "Test Restaurant")
    labeller.read_preps()

    expected_preps = pd.DataFrame({
        'PrepId': ['987'],
        'Description': ['Prep 987'],
        'PakQty': ['20'],
        'PakUOM': ['ml'],
        'InventoryGroup': ['Group B']
    })

    pd.testing.assert_frame_equal(labeller.preps, expected_preps)


def test_read_products(create_xml_files):
    """Test reading Products.xml and creating dataframe."""
    labeller = Labeller([create_xml_files], "Test Restaurant")
    labeller.read_products()

    expected_products = pd.DataFrame({
        'ProdId': ['654'],
        'Description': ['Product 654'],
        'SalesGroup': ['Sales A']
    })

    pd.testing.assert_frame_equal(labeller.products, expected_products)


def test_read_conversions(create_xml_files):
    """Test reading Conversions.xml and creating dataframe."""
    labeller = Labeller([create_xml_files], "Test Restaurant")
    labeller.read_conversions()

    expected_conversions = pd.DataFrame({
        'ConversionId': ['321'],
        'Multiplier': ['1.5'],
        'ConvertFromQty': ['100'],
        'ConvertFromUom': ['g'],
        'ConvertToQty': ['150'],
        'ConvertToUom': ['ml']
    })

    pd.testing.assert_frame_equal(labeller.conversions, expected_conversions)


def test_read_recipes(create_xml_files):
    """Test reading all recipe files and creating respective dataframes."""
    labeller = Labeller([create_xml_files], "Test Restaurant")
    labeller.read_recipes()

    # Test Items DataFrame
    expected_items = pd.DataFrame({
        'ItemId': ['123'],
        'Description': ['Item 123'],
        'CaseQty': ['10'],
        'CaseUOM': ['kg'],
        'PakQty': ['5'],
        'PakUOM': ['g'],
        'InventoryGroup': ['Group A']
    })
    pd.testing.assert_frame_equal(labeller.items, expected_items)

    # Test Ingredients DataFrame
    expected_ingredients = pd.DataFrame({
        'IngredientId': ['456'],
        'Qty': ['50'],
        'Uom': ['ml'],
        'Conversion': ['2'],
        'InvFactor': ['1'],
        'Recipe': ['789']
    })
    pd.testing.assert_frame_equal(labeller.ingredients, expected_ingredients)

    # Test Preps DataFrame
    expected_preps = pd.DataFrame({
        'PrepId': ['987'],
        'Description': ['Prep 987'],
        'PakQty': ['20'],
        'PakUOM': ['ml'],
        'InventoryGroup': ['Group B']
    })
    pd.testing.assert_frame_equal(labeller.preps, expected_preps)

    # Test Products DataFrame
    expected_products = pd.DataFrame({
        'ProdId': ['654'],
        'Description': ['Product 654'],
        'SalesGroup': ['Sales A']
    })
    pd.testing.assert_frame_equal(labeller.products, expected_products)

    # Test Conversions DataFrame
    expected_conversions = pd.DataFrame({
        'ConversionId': ['321'],
        'Multiplier': ['1.5'],
        'ConvertFromQty': ['100'],
        'ConvertFromUom': ['g'],
        'ConvertToQty': ['150'],
        'ConvertToUom': ['ml']
    })
    pd.testing.assert_frame_equal(labeller.conversions, expected_conversions)
