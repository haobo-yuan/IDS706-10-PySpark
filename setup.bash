# Install Java (Spark's dependency)
sudo apt update
sudo apt install -y openjdk-11-jdk

# Download and install Spark
wget https://downloads.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz
tar xvf spark-3.2.1-bin-hadoop3.2.tgz
sudo mv spark-3.2.1-bin-hadoop3.2 /opt/spark

# Set environment variables
echo "export SPARK_HOME=/opt/spark" >> ~/.bashrc
echo "export PATH=$SPARK_HOME/bin:$PATH" >> ~/.bashrc
echo "export PYSPARK_PYTHON=/home/codespace/venv/bin/python" >> ~/.bashrc
source ~/.bashrc

# Install PySpark
pip install pyspark
