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
    parser.add_argument("-y", default=None,type = int, help="Year")
    parser.add_argument("-r", default=0,type = int, help="Starting run")
    return parser.parse_args()

def main():
    
    start_time = time.time()
    option = cmd_collect()
    year = option.y
    run_start = option.r
    if(year == 2023):
        run_numb_prev = 440613
    else:
        run_numb_prev = 0

    df = pd.read_csv(f"../../run_files/runtable{year}.csv", index_col=False)
    df1 = df['Run'].sort_values(ascending = True).tolist()
    for run_numb in df1:
        print(f"({run_numb},{run_numb_prev})")
        if(run_numb >= run_start):
            x = gen_graphics(run_numb,run_numb_prev)
            x.HV_fail_finder_ML1()
            x.HV_fail_finder_ML2()
            if(run_numb_prev > 0 or run_numb == 427394):  
                x.LV_fail_finder(prev = True)
                x.JTAG_fail_finder(prev = True)
            x.JTAG_fail_finder(prev = False)
            x.LV_fail_finder(prev = False)
            x.colormap_gen()
            x.draw_chambers()       
        run_numb_prev = run_numb
    
    print("Time taken to run: ", time.time() - start_time)
    

    return


if __name__ == "__main__":
    main()

            #x.chamb_csv_loop()
            #x.chamber_loop()
    
        #    x.HV_fail_finder_ML1()
         #   x.HV_fail_finder_ML2()
          #  if(run_numb_prev > 0 or run_numb == 427394):  
           #     x.LV_fail_finder(prev = True)
            #    x.JTAG_fail_finder(prev = True)
#            x.JTAG_fail_finder(prev = False)
 #           x.LV_fail_finder(prev = False)
  #          x.colormap_gen()
   #         x.draw_chambers()
    #        x.close_file()
     #       
      #      updateHTML(run_numb) 
       
 


