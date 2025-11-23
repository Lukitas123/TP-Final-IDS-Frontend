// se guardan en variables los elementos del formulario que se van a usar.
const checkinInput = document.getElementById('checkin');
const checkoutInput = document.getElementById('checkout');
const roomSelect = document.getElementById('room');

//función principal que se encargará de todo.
function actualizarDisponibilidad() {
    
    // Obtengo las fechas que el usuario seleccionó.
    const checkinDate = checkinInput.value;
    const checkoutDate = checkoutInput.value;

    //como el usuario selecciono ya las fechas, deshabilito la opcion.
    roomSelect.disabled = true;

    // Comprobación si el usuario ha elegido ambas fechas y si la fecha desalida es posterior a la de entrada.
    if (checkinDate && checkoutDate && new Date(checkoutDate) > new Date(checkinDate)) {
        
        // Si las fechas son válidas, tiro al endpoint para checkear disponibilidad.
        fetch(`/check-availability?checkin=${checkinDate}&checkout=${checkoutDate}`)
            .then(function(response) {
                // El servidor da una respuesta. Si la respuesta es exitosa parseo a jason.
                if (response.ok) {
                    return response.json();
                } else {
                    console.error('Error al verificar la disponibilidad.');
                }
            })
            .then(function(data) {
                const idsDisponibles = data.available_room_ids.map(String);

                // con la lista de disponibilidad se puede habilitar el selector de fechas.
                roomSelect.disabled = false;
                
                // recorro cada una de las opciones del selector de habitaciones.
                for (let option of roomSelect.options) {
                    // ignoro la primera opción, que es un texto de ayuda.
                    if (option.value === "") {
                        continue;
                    }

                    // Compruebo si el ID de la habitación actual está en la lista de disponibles.
                    if (idsDisponibles.includes(option.value)) {
                        // Si está, se puede seleccionar.
                        option.disabled = false;
                    } else {
                        // Si no está, se deshabilita.
                        option.disabled = true;
                    }
                }
            })
            .catch(function(error) {
                // Muestro errores en consola.
                console.error('Fallo de conexión:', error);
            });
    }
}
// Cada vez que el usuario cambie la fecha en cualquiera de los dos calendarios, se ejecutará la función 'actualizarDisponibilidad'.
checkinInput.addEventListener('change', actualizarDisponibilidad);
checkoutInput.addEventListener('change', actualizarDisponibilidad);
// Al cargar la página, me aseguro de que el selector de habitaciones esté deshabilitado desde el principio.
roomSelect.disabled = true;
