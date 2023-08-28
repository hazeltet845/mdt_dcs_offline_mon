import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime as dt
import sys
import os
import ROOT as rt
from EndcapInnerChart import *
from EndcapMiddleChart import*
from EndcapOuterChart import *
from BarrelInnerChart import *
from BarrelMiddleChart import *
from BarrelOuterChart import *
import time



class gen_graphics:
    def __init__(self,run_num,prev_run_num):
        #Initialize class variables
        print(f"#### run number = {run_num}; previous run number = {prev_run_num}####")
        self.prev_run_num = prev_run_num
        self.run_num = run_num
        self.final_lumi = 0
        self.err_JTAG = []
        self.init_JTAG = []
        self.init_af_err_JTAG = []
        
        self.err_ML2 = []
        self.init_ML2 = []
        self.init_af_err_ML2 = []
        
        self.err_ML2 = []
        self.init_ML2 = []
        self.init_af_err_ML2 = []
        
        self.err_LV = []
        self.init_LV = []
        self.init_af_err_LV = []
        
        #set path for output files and check if exists
        self.path = '../../../web/static/Runs/' + str(self.run_num)
        isExist = os.path.exists(self.path)
        if(not isExist):
            #create paths
            os.mkdir(self.path)
            os.mkdir(self.path + "/images")
            os.mkdir(self.path + "/root")
            os.mkdir(self.path + "/csv")

        #Initalize Dataframes
        self.df_prev_fsm = None
        self.colormap = None
        if((self.prev_run_num > 0) or (self.run_num == 427394)):
            self.df_prev_fsm = pd.read_parquet(f"../../run_files/{self.run_num}/run{self.run_num}_fsm_prev.parquet")
        self.df_ch = pd.read_csv("../../run_files/chamber_names.csv")
        self.df_LVmap = pd.read_csv("../../run_files/LV_mapping.csv")
        
        self.df_sb = pd.read_parquet(f"../../run_files/{self.run_num}/run{self.run_num}_stablebeam.parquet")
        self.lumiExist = os.path.exists(f"../../run_files/{self.run_num}/run{self.run_num}_lumi.parquet")
        
        self.lumiBad = False 
        if(self.lumiExist):
            self.df_lumi = pd.read_parquet(f"../../run_files/{self.run_num}/run{self.run_num}_lumi.parquet")
            dif = len(self.df_sb.index) - len(self.df_lumi.index)
            if(dif > 2 or dif < 0 ):
                self.lumiBad = True
        
        self.df_V0 = pd.read_parquet(f"../../run_files/{self.run_num}/run{self.run_num}_V0.parquet")
                
        self.df_VCC = pd.read_parquet(f"../../run_files/{self.run_num}/run{self.run_num}_VCC.parquet")
        self.df_HVVMon = pd.read_parquet(f"../../run_files/{self.run_num}/run{self.run_num}_HVVMon.parquet")
        self.df_LVVMon = pd.read_parquet(f"../../run_files/{self.run_num}/run{self.run_num}_LVVMon.parquet")
        self.df_LViMon = pd.read_parquet(f"../../run_files/{self.run_num}/run{self.run_num}_LViMon.parquet")

        #Pandas operations to make HV iMon df and fsm df in format for analysis
        df_HViMon_t = pd.read_parquet(f"../../run_files/{self.run_num}/run{self.run_num}_HViMon.parquet")
        dffsm = pd.read_parquet(f"../../run_files/{self.run_num}/run{self.run_num}_fsm.parquet")
        df = pd.read_parquet(f"../../run_files/{self.run_num}/run{self.run_num}_runInfo.parquet")
        df0 = df[['run', 'lb', 'lb_since']]
        df0 = df0.assign(run='lumiBlock')
        df0 = df0.assign(lb_since = df0['lb_since'].apply(self.ts_convert))
        
        df1_fsm = df0.rename(columns={'run': 'element_name', 'lb': 'value_string', 'lb_since': 'ts'})
        df1_HViMon = df0.rename(columns={'run': 'comment_', 'lb': 'value_number', 'lb_since': 'ts'})
        
        df2_fsm = pd.concat([dffsm, df1_fsm], sort = False)
        df2_fsm['ts'] = pd.to_datetime(df2_fsm['ts'])
        df2_fsm.sort_values(by = 'ts', inplace = True)
        self.df_fsm = df2_fsm[['element_name','value_string','ts']]
        self.df_fsm.to_csv(f"{self.path}/csv/run{self.run_num}_fsmWeb.csv", index = False)
        
        df2_HViMon = pd.concat([df_HViMon_t, df1_HViMon], sort = False)
        df2_HViMon['ts'] = pd.to_datetime(df2_HViMon['ts'])
        df2_HViMon.sort_values(by = 'ts', inplace = True)
        self.df_HViMon = df2_HViMon[['comment_','value_number','ts']]
        #self.df_HViMon.to_csv(f"./test_HViMon.csv", index = False)
        
        #V0 df configuration
        if((self.prev_run_num <= 0) or (self.run_num == 427394)):
            self.df_V0_name = self.df_ch
            lis = np.zeros((len(self.df_ch['element_name'].tolist()))).tolist()
            self.df_V0_name['LV_V0'] = lis
            #print(self.df_V0_name)
            self.df_V0_name = self.df_V0_name.set_index('element_name')
        
        else:
            self.df_V0_name = pd.read_parquet(f"../../run_files/{self.prev_run_num}/run{self.prev_run_num}_V0chamber.parquet")
            #print(self.df_V0_name)
            #self.df_V0_name = self.df_V0_name.set_index('element_name')
            
        #Opening ROOT file to store figures
        #self.myfile = rt.TFile( f'../../../web/static/Runs/{self.run_num}/root/chambers.root', 'RECREATE' )
        #rt.gROOT.SetBatch(rt.kTRUE)
        
        print(f"#### {self.run_num} ANALYSIS: Init Complete ####")
        
     
    def ts_convert(self,ts):
            #convert timestamp to date minus two hours (to correspond with dcs data times)
            tmp = dt.fromtimestamp((ts/1000000000)-7200)
            return tmp
    
    def V0_find(self,chamber):
        #Find and return LV V0 for each chamber
        df = self.df_LVmap[self.df_LVmap['comment_'].str.contains(f"{chamber}")]
        chnl_l = df[df['element_name'].str.contains("vMon")]['element_name'].tolist()
        if(len(chnl_l) > 0):
        #df1.to_csv("./test_V0find")
            chnl = chnl_l[-1]
            chnl = chnl[:-12]
            dfV0 = self.df_V0[self.df_V0['element_name'].str.contains(f"{chnl}")]['value_number'].tolist()
            if(len(dfV0) > 0 ):
                V0 = dfV0[-1]
                print(f"#### V0 value found for {chamber} #### \n")
            else:
                V0 = self.df_V0_name.loc[chamber,'LV_V0']
                print(f"#### No new V0 value for {chamber}, using previous V0 #### \n")
        else:
            V0 = self.df_V0_name.loc[chamber,'LV_V0']
            print("#### No Channel to map for LV V0 ####")
        
        
        self.df_V0_name.at[chamber,'LV_V0'] = V0
        return V0
        
        
        
    def VCC_V0(self,chamber):
        #Graphing for V0-VCC graph
        df = self.df_VCC[self.df_VCC['element_name'].str.contains(f"{chamber}")]
        V0_t = self.V0_find(chamber)
        #print(f"{chamber} V0 = {V0_t}")
        V0 = np.round(V0_t,1)
        VCC_min_V0 = V0 - np.array(df['value_number'].tolist())
        #VCC_min_V0 = np.array(df['value_number'].tolist())
        #print(VCC_min_V0)
        ts = df['ts'].tolist()
        timestamp = []
        for k in range(len(ts)):
            timestamp.append(ts[k].timestamp())
        #timestamp = (ts - datetime(1970, 1, 1)).total_seconds()
        ts = np.array(timestamp)
        
        #Graphing with PyRoot
        c1 = rt.TCanvas( 'c1', f'{chamber}_VCC', 200, 10, 700, 500 )
        c1.SetGrid()
        
        x = np.array(ts,dtype = float)
        y = np.array(VCC_min_V0,dtype = float)
        
        mg = rt.TMultiGraph()
        mg.SetName(f"{chamber}_VCC_V0")
        mg.SetTitle(f"{chamber} V0 - VCC")
        if(len(x) > 0):
            gr = rt.TGraph(len(x),x,y)
            gr.SetLineColor(1)
            gr.SetLineWidth(3)
            #gr.SetMarkerColor(2)
            mg.Add(gr)
            
       
        mg.Draw()
        mg.GetYaxis().SetTitle( f'V0 - VCC (V)' )
        mg.GetXaxis().SetTitle( 'ts (unix)' )
        
        pave = rt.TPaveText(0.75, 0.75, 0.95, 0.95,"NDC")
        pave.SetBorderSize(1)
        pave.SetFillColor(0)
        t1 = pave.AddText(f"LV V0 = {V0} V")
        pave.Draw()
        
        #Writing to Root file
        c1.Modified()
        c1.Update()
        if(len(x) > 0):
            mg.GetListOfGraphs().Add(pave)
        mg.Write()
        c1.Close()

        
    def HV_LV_list(self,chamber,ml,iMon = True,LV = False) :
        #Return iMon or VMon for LV or HV based on arguments
        if(iMon and not LV):
            df = self.df_HViMon[self.df_HViMon['comment_'].str.contains(f"{chamber} {ml}")]
        elif(not iMon and not LV):
            df = self.df_HVVMon[self.df_HVVMon['comment_'].str.contains(f"{chamber} {ml}")]
        elif(iMon and LV):
            df = self.df_LViMon[self.df_LViMon['comment_'].str.contains(f"{chamber}")] 
        else:
            df = self.df_LVVMon[self.df_LVVMon['comment_'].str.contains(f"{chamber}")]
            
        #Return value and timestamps
        val = df['value_number'].tolist()
        ts = df['ts'].tolist()
        timestamp = []
        for k in range(len(ts)):
            timestamp.append(ts[k].timestamp())
        #timestamp = (ts - datetime(1970, 1, 1)).total_seconds()
        ts = np.array(timestamp)
        
        return val, ts
    
    def LV_graph(self,chamber,iMon = True):
        #Graphing for LV iMon and Vmon 
        y, x = self.HV_LV_list(chamber,"",iMon,True)
        
        if(iMon):
            ch = "i"
            unit = "(#muA)"
        else:
            ch = "V"
            unit = "(V)"
        
        c1 = rt.TCanvas( 'c1', f'{chamber}_LV_{ch}Mon', 200, 10, 700, 500 )
        c1.SetGrid()
        
        x = np.array(x,dtype = float)
        y = np.array(y,dtype = float)
        
        mg = rt.TMultiGraph()
        mg.SetName(f"{chamber}_{ch}Mon")
        mg.SetTitle(f"{chamber} LV {ch}Mon")
        if(len(x) > 0):
            gr = rt.TGraph(len(x),x,y)
            gr.SetLineColor(2)
            gr.SetLineWidth(3)
            #gr.SetMarkerColor(2)
            mg.Add(gr)
        
       
        mg.Draw('AL')
        mg.GetYaxis().SetTitle( f'Chamber LV {ch}Mon {unit}' )
        mg.GetXaxis().SetTitle( 'ts (unix)' )
        
        c1.Modified()
        c1.Update()
        mg.Write()
        c1.Close()
        
    def HV_graph(self, chamber,iMon = True):
        #Graphing for HV iMon and Vmon for ML1/ML2
        y_ML1, x_ML1 = self.HV_LV_list(chamber,"ML1",iMon,False)
        y_ML2, x_ML2 = self.HV_LV_list(chamber,"ML2", iMon,False)
        
        if(iMon):
            ch = "i"
            unit = "(#muA)"
        else:
            ch = "V"
            unit = "(V)"
        
        c1 = rt.TCanvas( 'c1', f'{chamber}_iMon', 200, 10, 700, 500 )
        c1.SetGrid()

        x_ML1 = np.array(x_ML1,dtype = float)
        x_ML2 = np.array(x_ML2,dtype = float)
        y_ML1 = np.array(y_ML1,dtype = float)
        y_ML2 = np.array(y_ML2, dtype = float)
        
        mg = rt.TMultiGraph()
        mg.SetName(f"{chamber}_{ch}Mon")
        mg.SetTitle(f"{chamber} HV {ch}Mon")
        
        legend = rt.TLegend(0.15,0.7,0.3,0.85)
        legend.SetTextSize(0.04)
        
        if(len(y_ML1) > 0):
            gr = rt.TGraph(len(y_ML1),x_ML1,y_ML1)
            gr.SetTitle("ML1")           
            gr.SetLineColor(2)
            gr.SetLineWidth(3)
            mg.Add(gr)
            legend.AddEntry(gr,"ML1","pl")
            
        if(len(y_ML2) > 0):
            gr1 = rt.TGraph(len(y_ML2), x_ML2, y_ML2)

            gr1.SetTitle("ML2")
            gr1.SetLineColor(4)
            gr1.SetLineWidth(3)
            mg.Add(gr1)
            legend.AddEntry(gr1,"ML2","pl")
            
        
        mg.Draw('AL')
        mg.GetYaxis().SetTitle( f'Chamber HV {ch}Mon {unit}' )
        mg.GetXaxis().SetTitle( 'ts (unix)' )
        

        legend.Draw('same')

        c1.Modified()
        c1.Update()
        #rt.gROOT.GetListOfCanvases().Draw()
        if(len(y_ML2) > 0 or len(y_ML1) > 0):
            mg.GetListOfGraphs().Add(legend)
            
        mg.Write()
        c1.Close()
        
        
    def iMon_lumiblock(self,chamber, ml):
        #Returns list of lists for iMon
        #Each sublist represents a specific lumiblock containing the iMon data from that lumiblock
        #Returns instantaneous luminosity 
        
        sb_l = (self.df_sb['AtlasPhysics'] & self.df_sb['StableBeams']).tolist()
        #print(len(sb_l))
        lumi_l = self.df_lumi['LBAvInstLumi'].tolist()
        #print(len(lumi_l))

        lumi_start_ts = 0
        iMon_prev_flag = 0
        iMon_temp = []
        iMon_val = []
        lumi_f = []
        lumi = 0
        val_prev = 0
        value_number = self.df_HViMon['value_number'].tolist()
        comment = self.df_HViMon['comment_'].tolist()
        print(len(comment), "\n")
        for k in range(len(comment)):   
            val = value_number[k]
            element_name = comment[k]
            if("lumiBlock" in element_name):
                #iMon_val.append(iMon_temp[:])
                #print(sb_l[lumi])
                #print(lumi, "\n")
                if(len(iMon_temp) > 0 and sb_l[lumi]):
                    iMon_avg = sum(iMon_temp)/len(iMon_temp)
                    iMon_val.append(iMon_avg)
                    lumi_f.append(lumi_l[lumi-1])
                    
                iMon_prev_flag = 0
                lumi += 1
                if(lumi != val):
                    print("ERROR")
                    break
                iMon_temp.clear()
            elif((chamber in element_name) and (ml in element_name)):
                iMon_temp.append(val)
                iMon_prev_flag = 1

        #iMon_val.append(iMon_temp[:])
        if(len(iMon_temp) > 0 and sb_l[lumi]):
                iMon_avg = sum(iMon_temp)/len(iMon_temp)
                iMon_val.append(iMon_avg)
                lumi_f.append(lumi_l[lumi-1])
                
        #print("Time taken to run: ", time.time() - start_time)
        return iMon_val,lumi_f
   
    
    def iMon_lumi_graph(self,chamber, iMon_ML1, lumi_ML1,iMon_ML2, lumi_ML2):
        
        #Graphing HV iMon vs instantaneous luminosity
        #Shows linear fits
        
        c1 = rt.TCanvas( 'c1', f'Lumi_{chamber}_iMon', 200, 10, 700, 500 )
        c1.SetGrid()

        x_ML1 = np.array(lumi_ML1,dtype = float)
        x_ML2 = np.array(lumi_ML2,dtype = float)
        y_ML1 = np.array(iMon_ML1,dtype = float)
        y_ML2 = np.array(iMon_ML2, dtype = float)
        
        mg = rt.TMultiGraph()
        mg.SetName(f"{chamber}_lumi")
        mg.SetTitle(f"{chamber} HV iMon vs Luminosity")
        
        legend = rt.TLegend(0.15,0.7,0.3,0.85)
        legend.SetTextSize(0.04)
        
        if(len(y_ML1) > 0):
            gr = rt.TGraph(len(y_ML1),x_ML1,y_ML1)
            fit = rt.TF1("fS", "pol1", 0, 25000)
            gr.SetTitle("ML1")
            gr.SetMarkerStyle(8)
            gr.SetMarkerSize(0.8)
            gr.SetMarkerColor(2)
            fit.SetLineColor(2)
            fit.SetLineWidth(3)
            gr.Fit("fS","Q")
            mg.Add(gr)
            legend.AddEntry(gr,"ML1","pl")
            
        if(len(y_ML2) > 0):
            gr1 = rt.TGraph(len(y_ML2), x_ML2, y_ML2)
            fit1 = rt.TF1("fS1", "pol1", 0, 25000)

            gr1.SetTitle("ML2")
            gr1.SetMarkerStyle(8)
            gr1.SetMarkerSize(0.8)
            gr1.SetMarkerColor(4)
            fit1.SetLineColor(4)
            fit1.SetLineWidth(3)
            gr1.Fit("fS1","Q")
            mg.Add(gr1)
            legend.AddEntry(gr1,"ML2","pl")
            
        
        mg.Draw('AP')
        mg.GetYaxis().SetTitle( 'Chamber HV IMon (#muA)' )
        mg.GetXaxis().SetTitle( 'Instantaneous Luminosity (10^{30} cm^{-2} s^{-1}) ' )

        legend.Draw('same')

        c1.Modified()
        c1.Update()
        #rt.gROOT.GetListOfCanvases().Draw()
        if(len(y_ML2) > 0 or len(y_ML1) > 0):
            mg.GetListOfGraphs().Add(legend)
        mg.Write()
        c1.Close()
        
        
    def chamber_loop(self):
        #Loop through list of chambers to generate plots for each chamber
        #Saved in ROOT file
        start_time = time.time()
        self.myfile.mkdir("Lumi_iMon/")
        self.myfile.mkdir(f"HV_VMon/")
        self.myfile.mkdir(f"HV_iMon/")
        self.myfile.mkdir(f"LV_VMon/")
        self.myfile.mkdir(f"LV_iMon/")
        self.myfile.mkdir(f"VCC_V0/")
        
        count = 0
        names = self.df_ch['element_name'].tolist()
        for element_name in names:
            print(f"{count} of {len(names)}, {element_name}")
            
            #HV iMon vs Instantaneous Luminosity
            if(self.lumiExist and not self.lumiBad):
                self.myfile.cd("Lumi_iMon/")
                iMon_ML1,lumi_ML1 = self.iMon_lumiblock(element_name,"ML1")
                iMon_ML2,lumi_ML2 = self.iMon_lumiblock(element_name,"ML2")
                self.iMon_lumi_graph(element_name, iMon_ML1, lumi_ML1,iMon_ML2, lumi_ML2)
            
            
            #HV VMon vs timestamps (ts)
            self.myfile.cd(f"HV_VMon/")
            iMon = False
            self.HV_graph(element_name,iMon)
            
            #HV iMon vs timestamps (ts)
            self.myfile.cd(f"HV_iMon/")
            iMon = True
            self.HV_graph(element_name,iMon)
            
            #LV VMon vs timestamps (ts)
            self.myfile.cd(f"LV_VMon/")
            iMon = False
            self.LV_graph(element_name,iMon)
            
            #LV iMon vs timestamps (ts)
            self.myfile.cd(f"LV_iMon/")
            iMon = True
            self.LV_graph(element_name,iMon)
            
            #CSM VCC minus LV V0 vs timestamps (ts)
            self.myfile.cd(f"VCC_V0/")
            self.VCC_V0(element_name)
            
            #self.chamb_csv(element_name)
            #^^^^Generates fsm table on chamber webpage 
            #Currently done on web page level (each time the chamber page is clicked fsm table is generated)
            #Not needed to be done here 
            
            count += 1
        
        print(f"#### {self.run_num} ANALYSIS: ROOT Plots Complete ####")
        print("Time taken to run: ", time.time() - start_time, "\n")
        
    def close_file(self):
        #Destructor
        #Close Root file
        self.myfile.Close()
        #Save information
        self.df_V0_name.to_parquet(f"../../run_files/{self.run_num}/run{self.run_num}_V0chamber.parquet")
        
    def chamb_csv(self, chamber):
        #Generates fsm table for each chamber
        #Done on web page 
        df = self.df_fsm[self.df_fsm['element_name'].str.contains(f"{chamber}|lumiBlock")]
        df = df.reset_index(drop=True)
        loop = df['element_name'].tolist()

        prev_lumi = False
        #for index, row in df.iterrows():
            #element_name = row['element_name']
            
        for index in range(len(loop)):
            element_name = loop[index]
            if(True):
                if(element_name == "lumiBlock"):
                    if(prev_lumi ):
                        df=df.drop(index-1)
                        
                        
                    prev_lumi = True
                else:
                    prev_lumi = False
                    
        df = df.fillna("-")      
        df.loc[df['element_name'].str.contains("JTAG"), 'element_name'] = f"{chamber} JTAG fsm"
        df.loc[df['element_name'].str.contains("ML1"), 'element_name'] = f"{chamber} HV ML1 fsm"
        df.loc[df['element_name'].str.contains("ML2"), 'element_name'] = f"{chamber} HV ML2 fsm"
        #print(df)
        df.to_csv(self.path + f"/csv/{chamber}_fsm.csv",index = False)
        
        
    def JTAG_fail_finder(self,prev = False):
        #Look for JTAG failure
        #For time between end of previous run and end of current run
        if(not prev):
            df = self.df_fsm
        else:
            df = self.df_prev_fsm
    
        init = []
        err_l = []
        init_af_err = []
        tmp = 1
        val_prev = -1
        value_string = df['value_string'].tolist()
        comment = df['element_name'].tolist()
        for k in range(len(comment)):
            val_string = value_string[k]
            element_name = comment[k]
            #JTAG ------------------------------------------------
            if(not ("lumiBlock" in element_name) and ("JTAG" in element_name) and val_string != 'REQUEST' and val_string != 'PRELOAD' and val_string != 'RESET' and val_string != 'STRINGLOAD' and val_string != 'VERIFY' and val_string != 'INITIALIZED'):
                tmp = 1                                                                                                     
                if(not prev):
                    print(f"JTAG CHAMBER ERROR: {element_name[-24:-17]}; {val_string};")
                if(element_name[-20] == 'C'):
                    tmp = -1
                #print(element_name[-19:-17])
                err_tup = (element_name[-24:-21], np.ceil(int(element_name[-19:-17])/2),tmp*int(element_name[-21]))
                err_l.append(err_tup)
                    
                
            elif(not ("lumiBlock" in element_name) and ("JTAG" in element_name) and val_string == "INITIALIZED"):
                tmp = 1
                if(element_name[-20] == 'C'):
                    tmp = -1
                #print(element_name[-19:-17])
                init_tup = (element_name[-24:-21], np.ceil(int(element_name[-19:-17])/2),tmp*int(element_name[-21]))
           
                if(init_tup in err_l):
                    init_af_err.append(init_tup)
                
                else:
                    init.append(init_tup)
                    
                    
                
        init_af_err = list(dict.fromkeys(init_af_err))       
         
        #Save JTAG chamber failures to list    
        self.err_JTAG.append(err_l)
        #Save JTAG initialization to list
        self.init_JTAG.append(init)
        #Save JTAG failure then initialization to list
        self.init_af_err_JTAG.append(init_af_err)
        print(f"#### {self.run_num} ANALYSIS: JTAG Fail Finder Complete #### \n")
        
    def HV_fail_finder_ML1(self):
        #Look for HV PS ML1 failures
        init = []
        err_l = []
        init_af_err = []
        tmp = 1
        val_prev = -1
        df = self.df_fsm
        value_string = df['value_string'].tolist()
        comment = df['element_name'].tolist()
        for k in range(len(comment)):
            val_string = value_string[k]
            element_name = comment[k]
            #HV ML1 ------------------------------------------------
            if(not ("lumiBlock" in element_name) and ("ML1.fsm.currentState" in element_name) and val_string != 'RAMP_UP' and val_string != 'RAMP_DOWN' and val_string != 'ON' and val_string != 'STANDBY'):
                tmp = 1                                                                                                     
                print(f"HV ML1 CHAMBER ERROR: {element_name[-24:-17]}; {val_string}; ")
                if(element_name[-24] == 'C'):
                    tmp = -1
                #print(element_name[-19:-17])
                err_tup = (element_name[-28:-25], np.ceil(int(element_name[-23:-21])/2),tmp*int(element_name[-25]))
                err_l.append(err_tup)
                    
                
            elif(not ("lumiBlock" in element_name) and ("ML1.fsm.currentState" in element_name) and val_string == "ON"):
                tmp = 1
                if(element_name[-24] == 'C'):
                    tmp = -1
                #print(element_name[-19:-17])
                init_tup = (element_name[-28:-25], np.ceil(int(element_name[-23:-21])/2),tmp*int(element_name[-25]))
           
                if(init_tup in err_l):
                    init_af_err.append(init_tup)
                
                else:
                    init.append(init_tup)
                    
                    
        
        init_af_err = list(dict.fromkeys(init_af_err))       
        init = list(dict.fromkeys(init)) 
        #print(len(init))
        
        #Save failures to list
        self.err_ML1 = err_l
        #Save initializations to list
        self.init_ML1 = init
        #Save initialization after failure to list
        self.init_af_err_ML1 = init_af_err
        print(f"#### {self.run_num} ANALYSIS: HV PS ML1 Fail Finder Complete #### \n")
            
    
    def HV_fail_finder_ML2(self):
        #Look for HV PS ML1 failures
        init = []
        err_l = []
        init_af_err = []
        tmp = 1
        val_prev = -1
        df = self.df_fsm
        value_string = df['value_string'].tolist()
        comment = df['element_name'].tolist()
        for k in range(len(comment)):
            val_string = value_string[k]
            element_name = comment[k]
            #HV ML1 ------------------------------------------------
            if(not ("lumiBlock" in element_name) and ("ML2.fsm.currentState" in element_name) and val_string != 'RAMP_UP' and val_string != 'RAMP_DOWN' and val_string != "ON" and val_string != 'STANDBY'):
                tmp = 1                                                                                                     
                print(f"HV ML2 CHAMBER ERROR: {element_name[-28:-21]}; {val_string}; ")
                if(element_name[-24] == 'C'):
                    tmp = -1
                #print(element_name[-19:-17])
                err_tup = (element_name[-28:-25], np.ceil(int(element_name[-23:-21])/2),tmp*int(element_name[-25]))
                err_l.append(err_tup)
                
                #print(val_string, " err")
                    
                
            elif( not ("lumiBlock" in element_name) and ("ML2.fsm.currentState" in element_name) and val_string == "ON"):
                #print(val_string, " ON")
                tmp = 1
                if(element_name[-24] == 'C'):
                    tmp = -1
                #print(element_name[-19:-17])
                init_tup = (element_name[-28:-25], np.ceil(int(element_name[-23:-21])/2),tmp*int(element_name[-25]))
           
                if(init_tup in err_l):
                    init_af_err.append(init_tup)
                
                else:
                    init.append(init_tup)
            
                    
                    
                
        init_af_err = list(dict.fromkeys(init_af_err)) 
        init = list(dict.fromkeys(init)) 
                
        #Save failures to list
        self.err_ML2 = err_l
        #Save initializations to list
        self.init_ML2 = init
        #Save initialization after failure to list
        self.init_af_err_ML2 = init_af_err
        print(f"#### {self.run_num} ANALYSIS: HV PS ML1 Fail Finder Complete #### \n")
        
        
    def LV_fail_finder(self, prev = False):
        #Find LV PS failures 
        #For time between end of previous run and end of current run
        if(not prev):
            df = self.df_fsm
        else:
            df = self.df_prev_fsm
    
        init = []
        err_l = []
        init_af_err = []
        tmp = 1
        val_prev = -1
        value_string = df['value_string'].tolist()
        comment = df['element_name'].tolist()
        for k in range(len(comment)):
            val_string = value_string[k]
            element_name = comment[k]
            #LV ------------------------------------------------
            if(not ("lumiBlock" in element_name) and ("LV" in element_name) and val_string != 'ON' and val_string != 'OFF' and val_string != 'UNPLUGGED'):
                tmp = 1                                                                                                     
                if(not prev):
                    print(f"LV CHAMBER ERROR: {element_name[-27:-20]}; {val_string};")
                if(element_name[-23] == 'C'):
                    tmp = -1
                #print(element_name[-19:-17])
                err_tup = (element_name[-27:-24], np.ceil(int(element_name[-22:-20])/2),tmp*int(element_name[-24]))
                err_l.append(err_tup)
                    
                
            elif(not ("lumiBlock" in element_name) and ("LV" in element_name) and val_string == "ON"):
                tmp = 1
                if(element_name[-23] == 'C'):
                    tmp = -1
                #print(element_name[-19:-17])
                init_tup = (element_name[-27:-24], np.ceil(int(element_name[-22:-20])/2),tmp*int(element_name[-24]))

           
                if(init_tup in err_l):
                    init_af_err.append(init_tup)
                
                else:
                    init.append(init_tup)
                    

        init_af_err = list(dict.fromkeys(init_af_err))       
        
        #Save failures to list
        self.err_LV.append(err_l)
        #Save initializations to list
        self.init_LV.append(init)
        #Save initializations after a failure to list
        self.init_af_err_LV.append(init_af_err)
        print(f"#### {self.run_num} ANALYSIS: LV PS Fail Finder Complete #### \n")

    def colormap_gen(self):
        #Generate a colormap for JTAG, HV ML1, HV ML2, and LV fsm diagrams
        
        #Use colormap from previous run 
        if(self.prev_run_num > 0):
            colormap = pd.read_parquet(f"../../run_files/{self.prev_run_num}/run{self.prev_run_num}_colormap.parquet")
            it = 2
        else: 
            if(self.run_num == 427394):
                it = 2
            else:
                it = 1
            chamb = []
            tmp = 1
            for index, row in self.df_ch.iterrows(): #JTAG
                tmp = 1
                element_name = row['element_name']
                if(element_name[4] == 'C'):
                    tmp = -1
                chamb.append((element_name[:3], np.ceil(int(element_name[5:])/2),tmp*int(element_name[3])))
          
            colormap = pd.DataFrame(chamb, columns=['Abbrev','Phi','Eta'])
            #print(colormap)
        
            color_JTAG = []
            color_ML1 = []
            color_ML2 = []
            color_LV = []
            for k in range(len(chamb)):
                color_JTAG.append("#CCCCCC")
                color_ML1.append("#CCCCCC")
                color_ML2.append("#CCCCCC")
                color_LV.append("#CCCCCC")
    
            colormap['color_JTAG'] = color_JTAG
            colormap['color_HV_ML1'] = color_ML1
            colormap['color_HV_ML2'] = color_ML2
            colormap['color_LV'] = color_LV
        
        
        #Change colors of chambers in FSM diagram based on fsm information
        for k, row in colormap.iterrows():                  
            for i in range(it):
                for j in self.init_JTAG[i]:
                    if(row['Abbrev'] == j[0] and row['Phi'] == j[1] and row['Eta'] == j[2]):
                        colormap.loc[k,'color_JTAG'] = "#00FF00"
                    
                for j in self.err_JTAG[i]:
                    if(row['Abbrev'] == j[0] and row['Phi'] == j[1] and row['Eta'] == j[2]):
                        if(it == 2 and i == 0):
                            colormap.loc[k,'color_JTAG'] = "#CCCCCC"
                        else:
                            colormap.loc[k,'color_JTAG'] = "#FF0000"
 
                for j in self.init_af_err_JTAG[i]:
                    if(row['Abbrev'] == j[0] and row['Phi'] == j[1] and row['Eta'] == j[2]):
                        if(it == 2 and i == 0):
                            colormap.loc[k,'color_JTAG'] = "#00FF00"
                        else:
                            colormap.loc[k,'color_JTAG'] = "#0000FF"
                            
                            
                for j in self.init_LV[i]:
                    if(row['Abbrev'] == j[0] and row['Phi'] == j[1] and row['Eta'] == j[2]):
                        colormap.loc[k,'color_LV'] = "#00FF00"
                    
                for j in self.err_LV[i]:
                    if(row['Abbrev'] == j[0] and row['Phi'] == j[1] and row['Eta'] == j[2]):
                        if(it == 2 and i == 0):
                            colormap.loc[k,'color_LV'] = "#CCCCCC"
                        else:
                            colormap.loc[k,'color_LV'] = "#FF0000"
 
                for j in self.init_af_err_LV[i]:
                    if(row['Abbrev'] == j[0] and row['Phi'] == j[1] and row['Eta'] == j[2]):
                        if(it == 2 and i == 0):
                            colormap.loc[k,'color_LV'] = "#00FF00"
                        else:
                            colormap.loc[k,'color_LV'] = "#0000FF"           
                    
            for j in self.init_ML1:
                if(row['Abbrev'] == j[0] and row['Phi'] == j[1] and row['Eta'] == j[2]):
                    colormap.loc[k,'color_HV_ML1'] = "#00FF00"
                    
            for j in self.err_ML1:
                if(row['Abbrev'] == j[0] and row['Phi'] == j[1] and row['Eta'] == j[2]):
                    colormap.loc[k,'color_HV_ML1'] = "#FF0000"
      
            for j in self.init_af_err_ML1:
                if(row['Abbrev'] == j[0] and row['Phi'] == j[1] and row['Eta'] == j[2]):
                    colormap.loc[k,'color_HV_ML1'] = "#0000FF"
                    
            for j in self.init_ML2:
                if(row['Abbrev'] == j[0] and row['Phi'] == j[1] and row['Eta'] == j[2]):
                    colormap.loc[k,'color_HV_ML2'] = "#00FF00"
                    
            for j in self.err_ML2:
                if(row['Abbrev'] == j[0] and row['Phi'] == j[1] and row['Eta'] == j[2]):
                    colormap.loc[k,'color_HV_ML2'] = "#FF0000"
      
            for j in self.init_af_err_ML2:
                if(row['Abbrev'] == j[0] and row['Phi'] == j[1] and row['Eta'] == j[2]):
                    colormap.loc[k,'color_HV_ML2'] = "#0000FF"
                                  
        #print(colormap_ML1[colormap_ML1['Abbrev'] == 'BME'])
        if(self.run_num == 427394):
            colormap['color_LV'] = colormap['color_HV_ML1']
            #print(colormap)
        self.colormap = colormap
        #Save colormap to file
        self.colormap.to_parquet(f"../../run_files/{self.run_num}/run{self.run_num}_colormap.parquet")
        
    def draw_chambers_s(self, name):
        #Draw FSM diagrams for each of {JTAG, HV ML1, HV ML2, and LV}
        colormap_b = {}
        colormap_ec = {}
        colormap_ea =  {}
        
        bool_n = []
        for k, row in self.colormap.iterrows():
            tup = (row['Abbrev'],row['Phi'],row['Eta'])
            tup_ec = (row['Abbrev'],row['Phi'],-row['Eta'])
            if(self.colormap['Abbrev'].str.startswith('E')[k]):
                if(row['Eta'] < 0):
                    colormap_ec[tup_ec] = row[f'color_{name}']
                else:
                    colormap_ea[tup] = row[f'color_{name}']
                    
            else:
                colormap_b[tup] = row[f'color_{name}']
        
        im_ei_c = Image.new(mode="RGB", size=(300, 300), color="#ffffff")
        im_ei_a = Image.new(mode="RGB", size=(300, 300), color="#ffffff")
        im_em_c = Image.new(mode="RGB", size=(300, 300), color="#ffffff")
        im_em_a = Image.new(mode="RGB", size=(300, 300), color="#ffffff")
        im_eo_c = Image.new(mode="RGB", size=(300, 300), color="#ffffff")
        im_eo_a = Image.new(mode="RGB", size=(300, 300), color="#ffffff")
        im_bi = Image.new(mode="RGB", size=(300, 300), color="#ffffff")
        im_bm = Image.new(mode="RGB", size=(300, 300), color="#ffffff")
        im_bo = Image.new(mode="RGB", size=(300, 300), color="#ffffff")
        
        ei_c = EndcapInnerChart()
        ei_a = EndcapInnerChart()
        em_c = EndcapMiddleChart()
        em_a = EndcapMiddleChart()
        eo_c = EndcapOuterChart()
        eo_a = EndcapOuterChart()
        bi = BarrelInnerChart()
        bm = BarrelMiddleChart()
        bo = BarrelOuterChart()



        ei_c.Draw(im_ei_c, colormap_ec)
        ei_a.Draw(im_ei_a, colormap_ea)
        em_c.Draw(im_em_c, colormap_ec)
        em_a.Draw(im_em_a, colormap_ea)
        eo_c.Draw(im_eo_c, colormap_ec)
        eo_a.Draw(im_eo_a, colormap_ea)
        bi.Draw(im_bi, colormap_b)
        bm.Draw(im_bm, colormap_b)
        bo.Draw(im_bo, colormap_b)


        im_ei_c.save(self.path + f"/images/ei_c_{name}.png", "PNG")
        im_ei_a.save(self.path + f"/images/ei_a_{name}.png", "PNG")
        im_em_c.save(self.path + f"/images/em_c_{name}.png", "PNG")
        im_em_a.save(self.path + f"/images/em_a_{name}.png", "PNG")
        im_eo_c.save(self.path + f"/images/eo_c_{name}.png", "PNG")
        im_eo_a.save(self.path + f"/images/eo_a_{name}.png", "PNG")

        im_bi.save(self.path + f"/images/bi_{name}.png", "PNG")
        im_bm.save(self.path + f"/images/bm_{name}.png","PNG")
        im_bo.save(self.path + f"/images/bo_{name}.png","PNG")

    def draw_chambers(self):
        self.draw_chambers_s("JTAG")
        self.draw_chambers_s("HV_ML1")
        self.draw_chambers_s("HV_ML2")
        self.draw_chambers_s("LV")
        print(f"#### {self.run_num} ANALYSIS: Draw FSM Diagrams Complete #### \n")
        
              
        
