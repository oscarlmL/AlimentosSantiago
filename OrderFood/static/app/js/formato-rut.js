function formatoRut(rut_enc_conv) {
    rut_enc_conv.value = rut_enc_conv.value.replace(/[.-]/g, '')
        .replace(/^(\d{1,2})(\d{3})(\d{3})(\w{1})$/, '$1.$2.$3-$4')
}
