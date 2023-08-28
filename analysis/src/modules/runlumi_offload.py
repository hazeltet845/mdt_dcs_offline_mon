#!/usr/bin/env python3

import requests
import pandas as pd
from datetime import datetime as dt

# Example: python3 runlumi-offload.py --run 452582
# Get run information from the ATLAS COOL API
def ts_convert(ts):
    tmp = dt.fromtimestamp((ts/1000000000)-7200)
    return tmp

def get_run_info(rlb):
    schema = 'ATLAS_COOLONL_TDAQ'
    node = '/TDAQ/RunCtrl/EOR'
    runsince = f'{rlb}-0'
    rununtil = f'{rlb}-0'
    iovtype = 'run-lumi'
    run_resp = requests.get(f'http://atlas-coolr-api.web.cern.ch/api/payloads?schema={schema}&node={node}&since={runsince}&until={rununtil}&iovtype={iovtype}')
    print(run_resp.json())
    if len(run_resp.json()['data_array']) == 0:
        print(f'No run information found for run {rlb}')
        return
    runinfo = run_resp.json()['data_array'][0]

    print(f'Found run information for run {runinfo["RunNumber"]}')
    # Get lumi block time info
    lb_schema = "ATLAS_COOLONL_TRIGGER"
    lb_node = '/TRIGGER/LUMI/LBTIME'
    lb_since = runinfo['SORTime']
    lb_until = runinfo['EORTime']
    # Load data from the Atlas COOL API
    runlumi_url = f'http://atlas-coolr-api.web.cern.ch/api/payloads?schema={lb_schema}&node={lb_node}&since={lb_since}&until={lb_until}'
    print(f'Get llb info from {runlumi_url}')
    rl_resp = requests.get(runlumi_url)
    rlb_array = rl_resp.json()['data_array']

    rlinfo_arr = []
    for m in rlb_array:
        rlinfo = ({ 'run': m['Run'], 'run_since': runinfo['SORTime'], 'run_until': runinfo['EORTime'], 
                'run_duration': runinfo['TotalTime'], 'run_stop': runinfo['CleanStop'], 'run_type': runinfo['RunType'],
                'lb': m['LumiBlock'], 'lb_since': m['IOV_SINCE'], 'lb_until': m['IOV_UNTIL'] })
        rlinfo_arr.append(rlinfo)

    rlinfo_df = pd.DataFrame(rlinfo_arr)
    table_name = "runlumi"
    eos_path = "../../run_files/" + str(rlb)
    fname = f"{eos_path}/run{rlb}_runInfo.parquet"
    rlinfo_df.to_parquet(fname)
    
