import sys,os
sys.path.append(os.path.abspath("../modules"))
from offload import *
import argparse
import time
from pyspark.sql import SparkSession

def cmd_collect():
    #Get arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", default=None,type = int, help="Run Number")
    parser.add_argument("-p", default = 0, type = int, help = "Previous Run Number")
    return parser.parse_args()


def main():
    start_time = time.time()
    #Initialize spark session
    spark = (SparkSession.builder
            .appName("DCS dbimport")
            .master("local[*]")
            .config("spark.driver.memory", "2g")
            .config("spark.executor.memory", "16g")
            .config("spark.jars.packages", "com.oracle.database.jdbc:ojdbc8:21.7.0.0")
            .getOrCreate()
            )

    #Get arguments from command line
    option = cmd_collect()
    run_numb = option.r
    run_numb_prev = option.p

    #Run Offload
    off0 = offload(run_numb,run_numb_prev,spark)
    if(run_numb_prev > 0 or run_numb == 427394):
        off0.get_data_fsm_prev()

    off0.get_data_HViMon()
    off0.get_data_HVVMon()
    off0.get_data_LViMon()
    off0.get_data_LVVMon()
    off0.get_data_V0()
    off0.get_data_VCC()
    off0.get_data_lumi()
    off0.get_data_fsm()
    
    
    print()
    print("OFFLOAD COMPLETE: Time taken to run => ", time.time() - start_time)

    return





if __name__ == "__main__":
    main()


