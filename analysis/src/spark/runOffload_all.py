import argparse
import sys,os
sys.path.append(os.path.abspath("../modules"))
from offload import *
import time
import pandas as pd
from pyspark.sql import SparkSession

def cmd_collect():
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", default=None,type = int, help="Year")
    parser.add_argument("-r", default=0,type = int, help="Starting run")
    return parser.parse_args()

def main():
    start_time = time.time()
    spark = (SparkSession.builder
            .appName("DCS dbimport")
            .master("local[*]")
            .config("spark.driver.memory", "2g")
            .config("spark.executor.memory", "16g")
            .config("spark.jars.packages", "com.oracle.database.jdbc:ojdbc8:21.7.0.0")
            .getOrCreate()
            )
    
    option = cmd_collect()
    year = option.y
    run_start = option.r
    if(year == 2023):
        run_numb_prev = 440613
    else:
        run_numb_prev = 0

    df = pd.read_csv(f"../../run_files/runtable{year}.csv") 
    df1 = df['Run'].sort_values(ascending = True)
    #print(df1)
    for k,run_numb in df1.items():
        print(f"({run_numb},{run_numb_prev})")
        if(run_numb >= run_start):
            off0 = offload(run_numb,run_numb_prev,spark)
            print("#################OFFLOADING INIT COMPLETE #########################")
            if(run_numb_prev > 0 or run_numb == 427394):
                off0.get_data_fsm_prev()
                print("#################FSM PREV COMPLETE #########################")

            off0.get_data_HViMon()
            print("#################IMON COMPLETE #########################")
            off0.get_data_VCC()
            off0.get_data_lumi()
            off0.get_data_fsm()
        run_numb_prev = run_numb

    print()
    print("Time taken to run: ", time.time() - start_time)
    return





if __name__ == "__main__":
    main()


