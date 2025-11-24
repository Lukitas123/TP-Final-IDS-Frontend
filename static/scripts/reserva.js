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


// Listener para el envío del formulario de reserva
document.querySelector('.reserva-personalizada__form').addEventListener('submit', function(event) {
    // Evita que el formulario se envíe de la manera tradicional
    event.preventDefault();

    // Recopila los datos del formulario
    const checkinDate = document.getElementById('checkin').value;
    const checkoutDate = document.getElementById('checkout').value;
    const roomTypeId = document.getElementById('room').value;
    const serviceId = document.getElementById('service').value;
    const activityId = document.getElementById('activity').value;
    const customerName = document.getElementById('name').value;
    const customerEmail = document.getElementById('email').value;

    // Construye el objeto JSON que se enviará al backend
    const reservationData = {
        room_type_id: parseInt(roomTypeId),
        checkin_date: checkinDate,
        checkout_date: checkoutDate,
        customer_name: customerName,
        customer_email: customerEmail,
        activity_ids: [parseInt(activityId)],
        service_ids: [parseInt(serviceId)]
    };

    // Envía la solicitud POST al backend
    // ATENCIÓN: La URL 'http://backend:5001/reservations' es para Docker. 
    // Si ejecutas localmente, deberás cambiarla a 'http://127.0.0.1:5001/reservations' o la que corresponda.
    fetch('http://backend:5001/reservations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reservationData)
    })
    .then(response => {
        if (response.ok) {
            // Si la reserva es exitosa, redirige a la página de confirmación
            window.location.href = '/confirmacion';
        } else {
            // Si hay un error, lo muestra en la consola
            response.json().then(data => {
                console.error('Error al crear la reserva:', data);
                alert('Hubo un error al procesar la reserva. Por favor, intente de nuevo.');
            });
        }
    })
    .catch(error => {
        console.error('Error de red:', error);
        alert('No se pudo conectar con el servidor. Revise su conexión o intente más tarde.');
    });
});
