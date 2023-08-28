from datetime import datetime as dt
import requests
import pandas as pd
from runlumi_offload import get_run_info
import os,sys,stat

class offload:
    def __init__(self,run_num,prev_run_num,spark):
        self.prev_run_num = prev_run_num
        self.run_num = run_num
        self.spark = spark
        
        #set path for output files and check if exists
        self.path = '../../run_files/'+ str(self.run_num)
        isExist = os.path.exists(self.path)
        if(not isExist):
            #create run folder
            os.mkdir(self.path)
            os.chmod(self.path,stat.S_IRWXG | stat.S_IRWXU |stat.S_IRWXO )
            
        #save run info into parquet file
        get_run_info(self.run_num)
        self.df_rinf = pd.read_parquet(f"{self.path}/run{self.run_num}_runInfo.parquet")
        
        #initialize specific run timestamps
        self.start_raw = (self.df_rinf['run_since'][0]/1000000000)-7200 
        self.ts_start = dt.fromtimestamp(self.start_raw)
        self.ts_end = dt.fromtimestamp((self.df_rinf['run_until'][0]/1000000000)-7200)
        
        print(f"Run {self.run_num} Start => {self.ts_start}")
        print(f"Run {self.run_num} End => {self.ts_end}")
        
        #Get data from time between end of previous run and current run
        self.df_prevrinf = None
        self.prev_ts_end = None
        
        #set ts to get data from before first run of Run 3
        if(self.run_num == 427394):
            self.prev_ts_end = dt.fromtimestamp(self.start_raw - 604800)
         
        #Get data from time between previous run and current run
        if(self.prev_run_num > 0):
            self.df_prevrinf = pd.read_parquet(f"../../run_files/{self.prev_run_num}/run{self.prev_run_num}_runInfo.parquet")
            self.prev_ts_end = dt.fromtimestamp((self.df_prevrinf['run_until'][0]/1000000000)-7200)
            
        #Initialize Dataframes with DCS data
        self.comments = self.spark.read.parquet("/atlas/dcs/PVSSMDT/comments_all.parquet")
        self.elements = self.spark.read.parquet("/atlas/dcs/PVSSMDT/elements_all.parquet")
        self.ev_hist  = self.spark.read.parquet("/atlas/dcs/PVSSMDT/eventhistory.parquet")
        lumin = self.spark.read.parquet("/atlas/conditions/ATLAS_LUMINOSITY/cool_luminosity.parquet")
        
        #For use with spark sql
        self.comments.createOrReplaceTempView("comments")
        self.elements.createOrReplaceTempView("elements")
        self.ev_hist.createOrReplaceTempView("ev_hist")
        lumin.createOrReplaceTempView("lumin")
        
        print(f"#### {self.run_num} OFFLOAD: Init Complete ####")
        
   
    def get_data_fsm(self):
        #Save PS fsm information to parquet 
        db0 = self.spark.sql(f"select elements.element_name, ev_hist.value_string,ev_hist.ts from ev_hist join elements on elements.element_id = ev_hist.element_id where elements.element_name like '%MDT%fsm.currentState%' and elements.valid_till is null and ts >= '{self.ts_start}' and ts <= '{self.ts_end}' order by ts asc")
        db_pd = db0.toPandas()
        db_pd.to_parquet(f"{self.path}/run{self.run_num}_fsm.parquet")
        os.chmod(f"{self.path}/run{self.run_num}_fsm.parquet", stat.S_IRWXG | stat.S_IRWXU |stat.S_IRWXO )
        print(f"#### {self.run_num} OFFLOAD: FSM Offload Complete ####")

    def get_data_fsm_prev(self):
        #Save PS fsm information from before current run to parquet 
        db0 = self.spark.sql(f"select elements.element_name, ev_hist.value_string,ev_hist.ts from ev_hist join elements on elements.element_id = ev_hist.element_id where elements.element_name like '%MDT%fsm.currentState%' and elements.valid_till is null and ts >= '{self.prev_ts_end}' and ts <= '{self.ts_start}' order by ts asc")
        db_pd = db0.toPandas()
        db_pd.to_parquet(f"{self.path}/run{self.run_num}_fsm_prev.parquet")
        os.chmod(f"{self.path}/run{self.run_num}_fsm_prev.parquet", stat.S_IRWXG | stat.S_IRWXU |stat.S_IRWXO )
        print(f"#### {self.run_num} OFFLOAD: Prev FSM Offload Complete ####")
        
    def get_data_HViMon(self):
        #Save HV PS iMon to parquet
        db0 = self.spark.sql(f"select comments.comment_,ev_hist.value_number,ev_hist.ts from ev_hist join comments on comments.element_id = ev_hist.element_id where (comments.comment_ like '%MDT%HV_Imon') and comments.valid_till is null and ts >= '{self.ts_start}' and ts <= '{self.ts_end}' order by ts asc")
        db_pd = db0.toPandas()
        db_pd.to_parquet(f"{self.path}/run{self.run_num}_HViMon.parquet")
        os.chmod(f"{self.path}/run{self.run_num}_HViMon.parquet", stat.S_IRWXG | stat.S_IRWXU |stat.S_IRWXO )
        print(f"#### {self.run_num} OFFLOAD: HV iMon Offload Complete ####")
        
    def get_data_V0(self):
        #Save V0 data to parquet
        db0 = self.spark.sql(f"select elements.element_name, ev_hist.value_number,ev_hist.ts from ev_hist join elements on elements.element_id = ev_hist.element_id where elements.element_name like '%MDT%readBackSettings.v0' and elements.valid_till is null and ts >= '{self.prev_ts_end}' and ts <= '{self.ts_end}' order by ts asc")
        db_pd = db0.toPandas()
        db_pd.to_parquet(f"{self.path}/run{self.run_num}_V0.parquet")
        os.chmod(f"{self.path}/run{self.run_num}_V0.parquet", stat.S_IRWXG | stat.S_IRWXU |stat.S_IRWXO ) 
        print(f"#### {self.run_num} OFFLOAD: V0 Offload Complete ####")
        
    def get_data_VCC(self):
        db0 = self.spark.sql(f"select elements.element_name, ev_hist.value_number,ev_hist.ts from ev_hist join elements on elements.element_id = ev_hist.element_id where elements.element_name like '%MDT%CSM.Vcc' and elements.valid_till is null and ts >= '{self.ts_start}' and ts <= '{self.ts_end}' order by ts asc")
        db_pd = db0.toPandas()
        db_pd.to_parquet(f"{self.path}/run{self.run_num}_VCC.parquet")
        os.chmod(f"{self.path}/run{self.run_num}_VCC.parquet", stat.S_IRWXG | stat.S_IRWXU |stat.S_IRWXO ) 
        print(f"#### {self.run_num} OFFLOAD: CSM VCC Offload Complete ####")
   
    def get_data_HVVMon(self):
        db0 = self.spark.sql(f"select comments.comment_,ev_hist.value_number,ev_hist.ts from ev_hist join comments on comments.element_id = ev_hist.element_id where (comments.comment_ like '%MDT%HV_Vmon') and comments.valid_till is null and ts >= '{self.ts_start}' and ts <= '{self.ts_end}' order by ts asc")
        db_pd = db0.toPandas()
        db_pd.to_parquet(f"{self.path}/run{self.run_num}_HVVMon.parquet")
        os.chmod(f"{self.path}/run{self.run_num}_HVVMon.parquet", stat.S_IRWXG | stat.S_IRWXU |stat.S_IRWXO )
        print(f"#### {self.run_num} OFFLOAD: HV VMon Offload Complete ####")
        
    def get_data_LVVMon(self):
        db0 = self.spark.sql(f"select comments.comment_,ev_hist.value_number,ev_hist.ts from ev_hist join comments on comments.element_id = ev_hist.element_id where (comments.comment_ like '%MDT%LV_Vmon') and comments.valid_till is null and ts >= '{self.ts_start}' and ts <= '{self.ts_end}' order by ts asc")
        db_pd = db0.toPandas()
        db_pd.to_parquet(f"{self.path}/run{self.run_num}_LVVMon.parquet")
        os.chmod(f"{self.path}/run{self.run_num}_LVVMon.parquet", stat.S_IRWXG | stat.S_IRWXU |stat.S_IRWXO )
        print(f"#### {self.run_num} OFFLOAD: LV VMon Offload Complete ####")
        
        
    def get_data_LViMon(self):
        db0 = self.spark.sql(f"select comments.comment_,ev_hist.value_number,ev_hist.ts from ev_hist join comments on comments.element_id = ev_hist.element_id where (comments.comment_ like '%MDT%LV_Imon') and comments.valid_till is null and ts >= '{self.ts_start}' and ts <= '{self.ts_end}' order by ts asc")
        db_pd = db0.toPandas()
        db_pd.to_parquet(f"{self.path}/run{self.run_num}_LViMon.parquet")
        os.chmod(f"{self.path}/run{self.run_num}_LViMon.parquet", stat.S_IRWXG | stat.S_IRWXU |stat.S_IRWXO )
        print(f"#### {self.run_num} OFFLOAD: LV iMon Offload Complete ####")
         
    def get_data_lumi(self):
        db = self.spark.sql(f"select run_number,LBAvInstLumi,Lumi_number from lumin where run_number = '{self.run_num}' order by lumi_number asc")
        if(db.count() > 0):
            db_pd = db.toPandas()
            db_pd.to_parquet(f"{self.path}/run{self.run_num}_lumi.parquet")
            os.chmod(f"{self.path}/run{self.run_num}_lumi.parquet", stat.S_IRWXG | stat.S_IRWXU |stat.S_IRWXO )
        else:
            print(f"ERROR:Instantaneous Luminosity data not available for run {self.run_num}")
        
        print(f"#### {self.run_num} OFFLOAD: Instantaneous Luminosity Offload Complete ####")
            
            
