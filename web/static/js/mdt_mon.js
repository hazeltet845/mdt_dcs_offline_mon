function getCSV(chamber, run_numb){
    //Grab CSV containing FSM chamber table 
    //Present as HTML table
    let table = document.getElementById("demoTable");
  
    // (B) READ CSV ON FILE PICK
    //picker.onchange = () => reader.readAsText("BOL1C09_fsm.csv");
   // fetch("./static/Runs/"+ run_numb + "csv/" + chamber + "_fsm.csv")
    fetch("/static/Runs/" + run_numb + "/csv/" + chamber + "_fsm.csv")
      .then((res) => res.text())
      .then((text) => {
        table.innerHTML = "";
        for (let row of CSV.parse(text)) {
          let tr = table.insertRow();
          for (let col of row) {
            let td = tr.insertCell();
            if(col == "FAILED" || col == "CAN_ELMB_NOOP"){
              let col_n = col.bold()
              let col_f = col_n.fontcolor("red")
              td.innerHTML = col_f
            }else if(col == "ON" || col == "INITIALIZED"){
              td.innerHTML = col.bold().fontcolor("green");
            }else{
              td.innerHTML = col;
            }
          }
        }
      })
      .catch((e) => console.error(e));
}

function sendData(chamber, run_numb) {
  //Send chamber name to python flask
  $.ajax({
      url: '/chamber/process',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ 'chamber': chamber, 'run_numb':run_numb }),
      error: function(error) {
          console.log(error);
      }
  });
}

function chamb_gen(chamber,run_numb){

    document.getElementById("chamber_label").innerHTML = chamber;
    //const img = document.querySelector("img"); 
    //img.src = "../static/Runs/"+run_numb+"/Images/fsm_diagrams/" + chamber + ".png";
    sendData(chamber,run_numb);


    getCSV(chamber,run_numb);
    //window.location.reload();

  
	JSROOT.openFile("../static/Runs/" + run_numb + "/root/chambers.root")
		.then(file => file.readObject("/Lumi_iMon/"+chamber+"_lumi;1"))
		.then(obj => {
							  
			JSROOT.draw("d3", obj, "AP");
		});

	JSROOT.openFile("../static/Runs/" + run_numb + "/root/chambers.root")
		.then(file => file.readObject("/HV_iMon/"+chamber+"_iMon;1"))
		.then(obj => {
							  
			JSROOT.draw("d4", obj, "AL");
		});


	JSROOT.openFile("../static/Runs/" + run_numb + "/root/chambers.root")
		.then(file => file.readObject("/HV_VMon/"+chamber+"_VMon;1"))
		.then(obj => {
							  
			JSROOT.draw("d5", obj, "AL");
		});


	JSROOT.openFile("../static/Runs/" + run_numb + "/root/chambers.root")
		.then(file => file.readObject("/LV_iMon/"+chamber+"_iMon;1"))
		.then(obj => {
							  
			JSROOT.draw("d6", obj, "AL");
		});

    JSROOT.openFile("../static/Runs/" + run_numb + "/root/chambers.root")
        .then(file => file.readObject("/LV_VMon/"+chamber+"_VMon;1"))
        .then(obj => {
                              
            JSROOT.draw("d7", obj, "AL");
        });
 
    JSROOT.openFile("../static/Runs/" + run_numb + "/root/chambers.root")
        .then(file => file.readObject("/VCC_V0/"+chamber+"_VCC_V0;1"))
        .then(obj => {
                              
            JSROOT.draw("d8", obj, "AL");
        });

    return;
}

function run_numb_gen(){
    run_numb = localStorage.getItem("run_numb")
    document.getElementById("home_label").innerHTML = "Run " + run_numb;


}

function chamb_button(){
    var abbrev = document.getElementById("Abbrev");

    var eta = document.getElementById("Eta");

    var a_c = document.getElementById("A_C");

    var phi = document.getElementById("Phi");

    var chamber = abbrev.value + eta.value + a_c.value + phi.value;
    //console.log(chamber);
    localStorage.setItem("chamber", chamber);

    run_numb = localStorage.getItem("run_numb")

    chamb_gen(chamber,run_numb);

    window.location.reload()

    
    return;
}

function chamb_onload(){
    chamber = localStorage.getItem("chamber")

    var abbrev = document.getElementById("Abbrev");
    abbrev.value = chamber.slice(0,3);

    var eta = document.getElementById("Eta");
    eta.value = chamber.slice(3,4);

    var a_c = document.getElementById("A_C");
    a_c.value = chamber.slice(4,5);

    var phi = document.getElementById("Phi");
    phi.value = chamber.slice(5);

    run_numb = localStorage.getItem("run_numb")
    document.getElementById("home_label").innerHTML = "Run " + run_numb;

    chamb_gen(chamber,run_numb);

    return;
}

function JTAG_onclick(chamber_name){
    localStorage.setItem("chamber", chamber_name);
}

function JTAG_onload(){
    run_numb_gen()

    const img0 = document.getElementById("ei_c")
    img0.src = "../static/Runs/"+run_numb+"/Images/ei_c_JTAG.png";

    const img1 = document.getElementById("bi")
    img1.src = "../static/Runs/"+run_numb+"/Images/bi_JTAG.png";

    const img2 = document.getElementById("ei_a")
    img2.src = "../static/Runs/"+run_numb+"/Images/ei_a_JTAG.png";

    const img3 = document.getElementById("em_c")
    img3.src = "../static/Runs/"+run_numb+"/Images/em_c_JTAG.png";

    const img4 = document.getElementById("bm")
    img4.src = "../static/Runs/"+run_numb+"/Images/bm_JTAG.png";

    const img5 = document.getElementById("em_a")
    img5.src = "../static/Runs/"+run_numb+"/Images/em_a_JTAG.png";

    const img6 = document.getElementById("eo_c")
    img6.src = "../static/Runs/"+run_numb+"/Images/eo_c_JTAG.png";

    const img7 = document.getElementById("bo")
    img7.src = "../static/Runs/"+run_numb+"/Images/bo_JTAG.png";

    const img8 = document.getElementById("eo_a")
    img8.src = "../static/Runs/"+run_numb+"/Images/eo_a_JTAG.png";
}

function LV_onload(){
    run_numb_gen()

    const img0 = document.getElementById("ei_c")
    img0.src = "../static/Runs/"+run_numb+"/Images/ei_c_LV.png";

    const img1 = document.getElementById("bi")
    img1.src = "../static/Runs/"+run_numb+"/Images/bi_LV.png";

    const img2 = document.getElementById("ei_a")
    img2.src = "../static/Runs/"+run_numb+"/Images/ei_a_LV.png";

    const img3 = document.getElementById("em_c")
    img3.src = "../static/Runs/"+run_numb+"/Images/em_c_LV.png";

    const img4 = document.getElementById("bm")
    img4.src = "../static/Runs/"+run_numb+"/Images/bm_LV.png";

    const img5 = document.getElementById("em_a")
    img5.src = "../static/Runs/"+run_numb+"/Images/em_a_LV.png";

    const img6 = document.getElementById("eo_c")
    img6.src = "../static/Runs/"+run_numb+"/Images/eo_c_LV.png";

    const img7 = document.getElementById("bo")
    img7.src = "../static/Runs/"+run_numb+"/Images/bo_LV.png";

    const img8 = document.getElementById("eo_a")
    img8.src = "../static/Runs/"+run_numb+"/Images/eo_a_LV.png";

}

function HV_ML1_onload(){
    run_numb_gen()

    const img0 = document.getElementById("ei_c")
    img0.src = "../static/Runs/"+run_numb+"/Images/ei_c_HV_ML1.png";

    const img1 = document.getElementById("bi")
    img1.src = "../static/Runs/"+run_numb+"/Images/bi_HV_ML1.png";

    const img2 = document.getElementById("ei_a")
    img2.src = "../static/Runs/"+run_numb+"/Images/ei_a_HV_ML1.png";

    const img3 = document.getElementById("em_c")
    img3.src = "../static/Runs/"+run_numb+"/Images/em_c_HV_ML1.png";

    const img4 = document.getElementById("bm")
    img4.src = "../static/Runs/"+run_numb+"/Images/bm_HV_ML1.png";

    const img5 = document.getElementById("em_a")
    img5.src = "../static/Runs/"+run_numb+"/Images/em_a_HV_ML1.png";

    const img6 = document.getElementById("eo_c")
    img6.src = "../static/Runs/"+run_numb+"/Images/eo_c_HV_ML1.png";

    const img7 = document.getElementById("bo")
    img7.src = "../static/Runs/"+run_numb+"/Images/bo_HV_ML1.png";

    const img8 = document.getElementById("eo_a")
    img8.src = "../static/Runs/"+run_numb+"/Images/eo_a_HV_ML1.png";

}

function HV_ML2_onload(){
    run_numb_gen()

    const img0 = document.getElementById("ei_c")
    img0.src = "../static/Runs/"+run_numb+"/Images/ei_c_HV_ML2.png";

    const img1 = document.getElementById("bi")
    img1.src = "../static/Runs/"+run_numb+"/Images/bi_HV_ML2.png";

    const img2 = document.getElementById("ei_a")
    img2.src = "../static/Runs/"+run_numb+"/Images/ei_a_HV_ML2.png";

    const img3 = document.getElementById("em_c")
    img3.src = "../static/Runs/"+run_numb+"/Images/em_c_HV_ML2.png";

    const img4 = document.getElementById("bm")
    img4.src = "../static/Runs/"+run_numb+"/Images/bm_HV_ML2.png";

    const img5 = document.getElementById("em_a")
    img5.src = "../static/Runs/"+run_numb+"/Images/em_a_HV_ML2.png";

    const img6 = document.getElementById("eo_c")
    img6.src = "../static/Runs/"+run_numb+"/Images/eo_c_HV_ML2.png";

    const img7 = document.getElementById("bo")
    img7.src = "../static/Runs/"+run_numb+"/Images/bo_HV_ML2.png";

    const img8 = document.getElementById("eo_a")
    img8.src = "../static/Runs/"+run_numb+"/Images/eo_a_HV_ML2.png";

}

function home_onclick(run_numb){
    localStorage.setItem("run_numb",run_numb);
}

