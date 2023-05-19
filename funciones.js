// FUNCION LOGIN (CON CORREO)
var expr = /^[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+$/;
$(document).ready(function() {
$("#enviar").click(function() {
    var email = $("#email").val();
    var pass = $("#pass").val();

    if (email === "" || !expr.test(email)) {
    $("#mensaje1").fadeIn();
    return false;
    } else {
    $("#mensaje1").fadeOut();
    }
    
    if (pass === "") {
    $("#mensaje2").fadeIn();
    return false;
    } else {
    $("#mensaje2").fadeOut();
    }
});
});

var email = document.getElementById('email');
var password = document.getElementById('password');
var error = document.getElementById('error');
error.style.color='red';

function enviarFormulario() {
    console.log('Enviando formulario...');
    var mensajeError =[];
    if(email.value===null||email.value==='') {
        mensajeError.push('DEBES INGRESAR TU CORREO ELECTRÓNICO');
    }
    if(password.value===null||password.value==='') {
        mensajeError.push('DEBES INGRESAR TU CONTRASEÑA');
    }
    error.innerHTML=mensajeError.join(' - ');
    return false;
}