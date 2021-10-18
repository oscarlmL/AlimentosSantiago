function formatoRut(rut) {
  rut.value = rut.value.replace(/[.-]/g, '')
    .replace(/^(\d{1,2})(\d{3})(\d{3})(\w{1})$/, '$1.$2.$3-$4')
}

function formatoPatenteMoto(patente_veh) {
  patente_veh.value = patente_veh.value.replace(/[•]/g, '')
    .replace(/^(\w{3})(\d{2})$/, '$1•$2')
}

function formatoPatenteAuto(patente_veh) {
  patente_veh.value = patente_veh.value.replace(/[•]/g, '')
    .replace(/^(\w{2})(\w{2})(\d{2})$/, '$1•$2•$3')
}


// function formatoPatente(patente_veh) {
//   if (patente_veh.target.value.length==5){
//     patente_veh = patente_veh.value.replace(/[•]/g, '')
//     .replace(/^(\w{3})(\d{2})$/, '$1•$2')
//   }else{
//     patente_veh = patente_veh.value.replace(/[•]/g, '')
//     .replace(/^(\w{2})(\w{2})(\d{2})$/, '$1•$2•$3')
//   }
// }
// moto 3 letras y dos numeros y el auto 2 letras 2 letras y 2 numeros


//Obtener input patente vehiculo segun el select tipo vehiculo
function showInp() {
  getSelectValue = document.getElementById("tipo_veh").value;
  if (getSelectValue == "Moto") {
    document.getElementById("patente_veh_moto").style.display = "inline-block";
    document.getElementById("patente_veh_auto").style.display = "none";
  } else if (getSelectValue == "Auto") {
    document.getElementById("patente_veh_auto").style.display = "inline-block";
    document.getElementById("patente_veh_moto").style.display = "none";
  }
}
