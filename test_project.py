import project
import pytest
    
def  test_get_nws_forecast():
    with pytest.raises(SystemExit):
        assert project.get_nws_forecast("https://api.weather.gov/points/33.6633,-95.5477/forecast")
        
def test_valid_zip():
    assert project.valid_zip('75460')==True
    assert project.valid_zip('00000')==False
    
def test_get_long_lat():
    with pytest.raises(SystemExit):
          assert project.get_long_lat(75463)
    assert project.get_long_lat(75460)==(33.6633, -95.5477, 'Paris, Lamar County, Texas, 75460, United States')
    
def test_get_nws_forecast_url():
    assert project.get_nws_forecast_url(33.6633, -95.5477)!="https://api.weather.gov/points/33.6633,-95.5477/forecast"
    assert project.get_nws_forecast_url(33.6633, -95.5477)=="https://api.weather.gov/gridpoints/FWD/136,143/forecast"
