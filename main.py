from lib import preprocess_data, generate_plot
from pyspark.sql.functions import mean, stddev, expr

def main():
    # Load and preprocess data
    stock_AAPL = preprocess_data()

    # Calculate descriptive statistics by grouping by year
    yearly_stats = stock_AAPL.groupBy("Year").agg(
        mean("Close").alias("mean"),                   # Mean of 'Close' price per year
        expr("percentile_approx(Close, 0.5)").alias("median"),  # Approximate median of 'Close' price
        stddev("Close").alias("std")                   # Standard deviation of 'Close' price
    ).orderBy("Year")                                  # Ensure data is sorted by 'Year'

    # Show the results
    yearly_stats.show()
    
    # Generate visualization
    generate_plot(yearly_stats)

if __name__ == "__main__":
    main()
