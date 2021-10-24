// function formatoRut(rut) {
//   rut.value = rut.value.replace(/[.-]/g, '')
//     .replace(/^(\d{1,2})(\d{3})(\d{3})(\w{1})$/, '$1.$2.$3-$4')
// }

function formatoRut(rut) {
  // Despejar Puntos
  var valor = rut.value.replace('.','');
  // Despejar Guión
  valor = valor.replace('-','');
  
  // Aislar Cuerpo y Dígito Verificador
  cuerpo = valor.slice(0,-1);
  dv = valor.slice(-1).toUpperCase();
  
  // Formatear RUN
  rut.value = cuerpo + '-'+ dv
  
  // Si no cumple con el mínimo ej. (n.nnn.nnn)
  if(cuerpo.length < 7) { rut.setCustomValidity("RUT Incompleto"); return false;}
  
  // Calcular Dígito Verificador
  suma = 0;
  multiplo = 2;
  
  // Para cada dígito del Cuerpo
  for(i=1;i<=cuerpo.length;i++) {
  
      // Obtener su Producto con el Múltiplo Correspondiente
      index = multiplo * valor.charAt(cuerpo.length - i);
      
      // Sumar al Contador General
      suma = suma + index;
      
      // Consolidar Múltiplo dentro del rango [2,7]
      if(multiplo < 7) { multiplo = multiplo + 1; } else { multiplo = 2; }

  }
  
  // Calcular Dígito Verificador en base al Módulo 11
  dvEsperado = 11 - (suma % 11);
  
  // Casos Especiales (0 y K)
  dv = (dv == 'K')?10:dv;
  dv = (dv == 0)?11:dv;
  
  // Validar que el Cuerpo coincide con su Dígito Verificador
  if(dvEsperado != dv) { rut.setCustomValidity("RUT Inválido"); return false; }
  
  // Si todo sale bien, eliminar errores (decretar que es válido)
  rut.setCustomValidity('');
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
    document.getElementById("bicicleta").style.display = "none";

  } else if (getSelectValue == "Auto") {
    document.getElementById("patente_veh_auto").style.display = "inline-block";
    document.getElementById("patente_veh_moto").style.display = "none";
    document.getElementById("bicicleta").style.display = "none";

  }else if (getSelectValue == "Bicicleta") {
    document.getElementById("Bicicleta").style.display = "inline-block";
    document.getElementById("patente_veh_moto").style.display = "none";
    document.getElementById("patente_veh_auto").style.display = "none";

  }
}
