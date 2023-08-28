function chamb_gen(chamber){

    document.getElementById("chamber_label").innerHTML = chamber;
    const img = document.querySelector("img"); 
    img.src = "../Images/fsm_diagrams/" + chamber + ".png";

    return;
}

function chamb_button(){
    var abbrev = document.getElementById("Abbrev");

    var eta = document.getElementById("Eta");

    var a_c = document.getElementById("A_C");

    var phi = document.getElementById("Phi");

    var chamber = abbrev.value + eta.value + a_c.value + phi.value;
    //console.log(chamber);
    localStorage.setItem("chamber", chamber);

    chamb_gen(chamber);

    
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

    chamb_gen(chamber);

    return;
}

function JTAG_onclick(chamber_name){
    localStorage.setItem("chamber", chamber_name);
}
