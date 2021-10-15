

$("formulario").validate({
    rules: {
        nombre: {
            required: true,
            minlength: 3,
            maxlength: 30
        }
    }
})

$("#guardar").click(function() {
    if ($('#formulario').valid() == false) {
        return;
    }
    let nombre = $("nombre").val()


})