from bs4 import BeautifulSoup
import pandas as pd

def chamb_csv(run_num, chamber):
    #Create FSM chamber table
    path = './static/Runs/' + str(run_num)
    df_fsm = pd.read_csv(f"{path}/csv/run{run_num}_fsmWeb.csv")

    df = df_fsm[df_fsm['element_name'].str.contains(f"{chamber}|lumiBlock")]
    df = df.reset_index(drop=True)
    loop = df['element_name'].tolist()

    prev_lumi = False
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
    df.to_csv(path + f"/csv/{chamber}_fsm.csv",index = False)

def updateHTML(run_numb_int):
    #Add new row to Home page run table
    run_numb = str(run_numb_int)
    soup = BeautifulSoup(open('../../../web/templates/home.html'),'html.parser')
  
    new_tr = soup.new_tag("tr")

    #Add as many td (data) you want.
    new_td = soup.new_tag('td')
    new_td2 = soup.new_tag('td')
    new_td3 = soup.new_tag('td')

    new_a = soup.new_tag('a', href = "{{url_for('jtag')}}", onclick = "home_onclick(" + run_numb + ")")
    new_a.string = run_numb

    #new_td.string = run_numb # data
    new_td2.string = "-----"
    new_td3.string = "-----"

    new_td.append(new_a)
    new_tr.append(new_td)
    new_tr.append(new_td2)
    new_tr.append(new_td3)

    #Add whole 'tr'(row) to table.
    soup.table.insert(7,new_tr)
    soup.table.insert(8,'\n')
    #soup.table.append(new_tr)


    # print(soup.table.contents)
    df = pd.read_html(str(soup))
    print(df)


    with open('../../../web/templates/home.html', "w") as file:
        file.write(str(soup))

    file.close()

    print(f"#### {run_numb} UPDATE HTML COMPLETE ####")
