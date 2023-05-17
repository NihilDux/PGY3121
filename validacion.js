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