#!/usr/bin/env python3
#https://atlas-coolr.web.cern.ch/api/payloads?schema=ATLAS_COOLOFL_TRIGGER&node=/TRIGGER/OFLLUMI/LumiAccounting&tag=OflLumiAcct-Run3-003&since=1688641086209631200&until=9688641086209631200


import requests
import pandas as pd

# Example: python3 runlumi-offload.py --run 452582
# Get run information from the ATLAS COOL API
def get_stablebeam(rlb):
    df_runtime = pd.read_parquet(f"../../run_files/{rlb}/run{rlb}_runInfo.parquet")
    runsince = df_runtime['run_since'][0]
    rununtil = df_runtime['run_until'][0]
    schema = 'ATLAS_COOLOFL_TRIGGER'
    node = '/TRIGGER/OFLLUMI/LumiAccounting'
    tag = 'OflLumiAcct-Run3-003'
    run_resp = requests.get(f'http://atlas-coolr-api.web.cern.ch/api/payloads?schema={schema}&node={node}&tag={tag}&since={runsince}&until={rununtil}')
#    print(run_resp.json())
    if len(run_resp.json()['data_array']) == 0:
        print(f'No run information found for run {rlb}')
        return
    runinfo = run_resp.json()['data_array']

    rlinfo_arr = []
    for m in runinfo:
        rlinfo = ({ 'LumiBlock': m['LumiBlock'],'AtlasPhysics': m['AtlasPhysics'], 'StableBeams': m['StableBeams']})
        rlinfo_arr.append(rlinfo)

    rlinfo_df = pd.DataFrame(rlinfo_arr[1:])
    eos_path = "../../run_files/" + str(rlb)
    fname = f"{eos_path}/run{rlb}_stablebeam.parquet"
    rlinfo_df.to_parquet(fname)



