export HADOOP_EXE='/usr/bin/hadoop'
export HADOOP_LIBPATH='/opt/cloudera/parcels/CDH/lib'
export HADOOP_STREAMING='hadoop-mapreduce/hadoop-streaming.jar'


module load python/gcc/3.7.9
module load spark/3.0.1

alias hfs="$HADOOP_EXE fs"
alias spark-submit='PYSPARK_PYTHON=$(which python) spark-submit --conf  spark.dynamicAllocation.enabled=true --conf spark.shuffle.service.enabled=false --conf spark.dynamicAllocation.shuffleTracking.enabled=true'
alias hjs="$HADOOP_EXE jar $HADOOP_LIBPATH/$HADOOP_STREAMING"


