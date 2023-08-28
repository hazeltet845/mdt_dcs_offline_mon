import argparse
import sys
import os
sys.path.append(os.path.abspath("../modules"))
from gen_graphics import *
sys.path.append(os.path.abspath("../../../web"))
from updateHTML import *
import time

def cmd_collect():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", default=None,type = int, help="Run Number")
    parser.add_argument("-p", default = 0, type = int, help = "Previous ATLAS Run Number")
    parser
    return parser.parse_args()

def main():
    start_time = time.time()
    option = cmd_collect()
    run_numb = option.r
    run_numb_prev = option.p
    print(run_numb_prev)
    
    x = gen_graphics(run_numb,run_numb_prev)
    #x.chamb_csv_loop()
    x.chamber_loop()
    
    
    x.HV_fail_finder_ML1()
    x.HV_fail_finder_ML2()
    if(run_numb_prev > 0 or run_numb == 427394):  
        x.LV_fail_finder(prev = True)
        x.JTAG_fail_finder(prev = True)
    x.JTAG_fail_finder(prev = False)
    x.LV_fail_finder(prev = False)
    x.colormap_gen()
    x.draw_chambers()
    x.close_file()
    
    print("Time taken to run: ", time.time() - start_time)
    updateHTML(run_numb)
    

    
    return

  



if __name__ == "__main__":
    main()

