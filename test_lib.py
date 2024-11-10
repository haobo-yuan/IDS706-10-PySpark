import pytest
from lib import preprocess_data, generate_plot, spark
from pyspark.sql import Row
from pyspark.sql.functions import mean, stddev, expr, year  # Add `year` import
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
    df = spark.createDataFrame(data)
    
    # Add 'Year' column by extracting year from 'Date'
    df = df.withColumn("Date", expr("to_date(Date, 'yyyy-MM-dd')"))  # Convert Date to date type
    df = df.withColumn("Year", year("Date"))  # Add Year column
    return df

def test_preprocess_data(sample_data, monkeypatch):
    # Mock reading CSV to use sample_data instead
    monkeypatch.setattr("lib.spark.read.csv", lambda *args, **kwargs: sample_data)
    
    # Process the data
    result = preprocess_data()
    
    # Check if 'Year' column is added
    assert "Year" in result.columns

    # Check if filtering for AAPL stock worked correctly
    assert result.filter(result.Name != "AAPL").count() == 0

    # Check if Date is converted to date type
    assert result.schema["Date"].dataType.typeName() == "date"

def test_generate_plot(sample_data):
    # Aggregate statistics on sample data to pass to the plotting function
    yearly_stats = sample_data.groupBy("Year").agg(
        mean("Close").alias("mean"),
        expr("percentile_approx(Close, 0.5)").alias("median"),
        stddev("Close").alias("std")
    ).orderBy("Year")

    # Generate the plot
    generate_plot(yearly_stats)

    # Check if the plot image file is created
    assert os.path.exists("pictures/plot.png")

    # Clean up
    os.remove("pictures/plot.png")
