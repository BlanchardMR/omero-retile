from src.utils import tileMultiple, roiTiler, getProjectPixels
from unittest.mock import Mock, PropertyMock

#test with mock data if tile multiple returns proper rows, cols for image size
def test_tileMultiple():
    mock_image = Mock()
    mock_image.getSizeX = PropertyMock(return_value=9000)
    mock_image.getSizeY = PropertyMock(return_value=9000)
    assert tileMultiple(mock_image, 2048) == (4,4)
    mock_image.getSizeX = PropertyMock(return_value=0)
    mock_image.getSizeY = PropertyMock(return_value=0)
    assert tileMultiple(mock_image, 2048) == (0,0)
    mock_image.getSizeX = PropertyMock(return_value=100000)
    mock_image.getSizeY = PropertyMock(return_value=500)
    assert tileMultiple(mock_image, 2048) == (48,0)
    mock_image.getSizeX = PropertyMock(return_value=500)
    mock_image.getSizeY = PropertyMock(return_value=100000)

#test roiTiler to verify roi # returned matches rows x columns
def test_get_tile_size():
    list_rois = roiTiler(2048, 10, 10)
    assert len(list_rois) == 100

def test_getProjectPixels():
    mock_conn = Mock()
    id_list = [1,2,3,4,5,6,7,8,9,10]
    mock_image = Mock()
    primary_pixels = Mock()
    mock_conn.getObject = PropertyMock(return_value=mock_image)
    mock_image.getPrimaryPixels = primary_pixels
    assert len(getProjectPixels(mock_conn, id_list)) == 10
