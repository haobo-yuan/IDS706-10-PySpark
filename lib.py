from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, mean, stddev, expr
from datetime import datetime
import matplotlib.pyplot as plt

# Initialize SparkSession
spark = SparkSession.builder.appName("AAPL_Stock_Analysis").getOrCreate()

# Data Preprocessing
def preprocess_data():
    # Read the data from a CSV file using Spark
    stock = spark.read.csv("data/NASDAQ_100_Data_From_2010.csv", sep="\t", header=True, inferSchema=True)

    # Filter the data for AAPL stock only
    stock_AAPL = stock.filter(col("Name") == "AAPL")

    # Convert 'Date' column to date format and add a new 'Year' column
    stock_AAPL = stock_AAPL.withColumn("Date", expr("to_date(Date, 'yyyy-MM-dd')"))
    stock_AAPL = stock_AAPL.withColumn("Year", year("Date"))

    return stock_AAPL

# Plotting function for statistics
def generate_plot(yearly_stats):
    
    # Convert Spark DataFrame to Pandas DataFrame for plotting
    yearly_stats_pd = yearly_stats.toPandas()
    
    # Extract the data for plotting
    years = yearly_stats_pd["Year"].values
    means = yearly_stats_pd["mean"].values
    medians = yearly_stats_pd["median"].values
    stds = yearly_stats_pd["std"].values
    
    # Plot the statistics
    plt.figure(figsize=(15, 6))
    plt.plot(years, means, label="Mean", marker="o")
    plt.plot(years, medians, label="Median", marker="x")
    plt.plot(years, stds, label="Standard Deviation", marker="s")
    plt.grid(True)
    plt.title("AAPL Close Price Statistics (2010-2021)")
    plt.xlabel("Year")
    plt.ylabel("Price")
    plt.legend()

    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    plt.text(0.95, 0.01, f"Generated on: {timestamp}", 
             verticalalignment='bottom', horizontalalignment='right', 
             transform=plt.gca().transAxes, 
             color='gray', fontsize=8)
    
    plt.savefig("pictures/plot.png")
