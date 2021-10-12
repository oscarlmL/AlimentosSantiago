

$("formulario_registro").validate({
    rules: {
        nombre: {
            required: true,
            minlength: 3,
            maxlength: 30
        }
    }
})

$("#guardar").click(function() {
    if ($('#formulario_registro').valid() == false) {
        return;
    }
    let rut = $("rut").val()


})