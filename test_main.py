from main import main
from lib import spark
from pyspark.sql import Row
import pytest
import os

@pytest.fixture(scope="module")
def sample_data():
    # Create sample data similar to the expected CSV structure
    data = [
        Row(Date="2010-01-04", Close=30.5725, Name="AAPL"),
        Row(Date="2010-01-05", Close=30.625, Name="AAPL"),
        Row(Date="2011-01-03", Close=40.0, Name="AAPL"),
        Row(Date="2011-01-04", Close=41.0, Name="AAPL"),
        Row(Date="2012-01-03", Close=50.0, Name="AAPL"),
        Row(Date="2012-01-04", Close=51.0, Name="AAPL"),
        Row(Date="2012-01-05", Close=52.0, Name="AAPL"),
    ]
    return spark.createDataFrame(data)

def test_main(monkeypatch, sample_data, capsys):
    # Mock preprocess_data to return sample_data
    monkeypatch.setattr("lib.preprocess_data", lambda: sample_data)

    # Run the main function
    main()

    # Capture output and verify yearly statistics in the output
    captured = capsys.readouterr()
    assert "Year" in captured.out
    assert "mean" in captured.out
    assert "median" in captured.out
    assert "std" in captured.out

    # Check if the plot image file is created
    assert os.path.exists("pictures/plot.png")

    # Clean up
    os.remove("pictures/plot.png")
