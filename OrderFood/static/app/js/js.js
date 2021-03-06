function formatoRut(rut) {
  // Despejar Puntos
  var valor = rut.value.replace('.', '');
  // Despejar Guión
  valor = valor.replace('-', '');

  // Aislar Cuerpo y Dígito Verificador
  cuerpo = valor.slice(0, -1);
  dv = valor.slice(-1).toUpperCase();

  // Formatear RUN
  rut.value = cuerpo + '-' + dv

  // Si no cumple con el mínimo ej. (n.nnn.nnn)
  if (cuerpo.length < 7) { rut.setCustomValidity("RUT Incompleto"); return false; }

  // Calcular Dígito Verificador
  suma = 0;
  multiplo = 2;

  // Para cada dígito del Cuerpo
  for (i = 1; i <= cuerpo.length; i++) {

    // Obtener su Producto con el Múltiplo Correspondiente
    index = multiplo * valor.charAt(cuerpo.length - i);

    // Sumar al Contador General
    suma = suma + index;

    // Consolidar Múltiplo dentro del rango [2,7]
    if (multiplo < 7) { multiplo = multiplo + 1; } else { multiplo = 2; }

  }

  // Calcular Dígito Verificador en base al Módulo 11
  dvEsperado = 11 - (suma % 11);

  // Casos Especiales (0 y K)
  dv = (dv == 'K') ? 10 : dv;
  dv = (dv == 0) ? 11 : dv;

  // Validar que el Cuerpo coincide con su Dígito Verificador
  if (dvEsperado != dv) { rut.setCustomValidity("RUT Inválido"); return false; }

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

  } else if (getSelectValue == "Bicicleta") {
    document.getElementById("bicicleta").style.display = "none";
    document.getElementById("patente_veh_moto").style.display = "none";
    document.getElementById("patente_veh_auto").style.display = "none";

  }
}

function tipoEntregaIn() {
  getSelectValue = document.getElementById("tipo_entrega").value;
  if (getSelectValue == "Delivery") {
    document.getElementById("ocultarCostoEnvenio").style.display = "inline-block";
  } else {
    document.getElementById("ocultarCostoEnvenio").style.display = "none";
  }
}

function mostrarContrasena() {
  var tipo = document.getElementById("password");
  if (tipo.type == "password") {
    tipo.type = "text";
  } else {
    tipo.type = "password";
  }
}

function mostrarContrasena1() {
  var tipo = document.getElementById("password1");
  if (tipo.type == "password") {
    tipo.type = "text";
  } else {
    tipo.type = "password";
  }
}

function mostrarContrasena2() {
  var tipo = document.getElementById("password2");
  if (tipo.type == "password") {
    tipo.type = "text";
  } else {
    tipo.type = "password";
  }
}



//input direccion ralizar pedido
function initMap() {
  var autocomplete = new google.maps.places.Autocomplete(
    document.getElementById("clientAddress"),
    {
      types: ['address'],
      componentRestrictions: { 'country': ['cl'] },
    })
  autocomplete.addListener('place_changed', function () {
    var place = autocomplete.getPlace();
    document.getElementById('location-snap').
      innerHTML = place.formatted_address;
    document.getElementById('lat-span').
      innerHTML = place.geometry.location.lat();
    document.getElementById('lon-span').
      innerHTML = place.geometry.location.lng();
  });
}