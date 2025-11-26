document.addEventListener('DOMContentLoaded', function () {
    const formReservaPaquete = document.getElementById('form-reserva-paquete');
    if (!formReservaPaquete) {
        console.error('Formulario de reserva de paquete no encontrado.');
        return;
    }

    const checkinInput = document.getElementById('checkin-paquete');
    const checkoutInput = document.getElementById('checkout-paquete');
    const btnReservar = document.getElementById('btn-reservar-paquete');
    const availabilityMessage = document.getElementById('availability-message');

    const paqueteId = formReservaPaquete.dataset.paqueteId;
    const roomTypeId = formReservaPaquete.dataset.roomTypeId;
    const nights = parseInt(formReservaPaquete.dataset.nights);

    // Función para calcular la fecha de checkout
    function calculateCheckoutDate(checkinDateStr, nights) {
        if (!checkinDateStr) return '';
        const checkin = new Date(checkinDateStr + 'T00:00:00'); // Añadir T00:00:00 para evitar problemas de zona horaria
        checkin.setDate(checkin.getDate() + nights);
        return checkin.toISOString().split('T')[0]; // Formato YYYY-MM-DD
    }

    // Función para actualizar la disponibilidad
    async function updateAvailability() {
        const checkinDate = checkinInput.value;

        if (!checkinDate) {
            btnReservar.disabled = true;
            availabilityMessage.textContent = 'Selecciona una fecha de Check-in.';
            availabilityMessage.style.color = 'var(--text-color)';
            checkoutInput.value = '';
            return;
        }

        const checkoutDate = calculateCheckoutDate(checkinDate, nights);
        checkoutInput.value = checkoutDate;

        if (new Date(checkoutDate) <= new Date(checkinDate)) {
            btnReservar.disabled = true;
            availabilityMessage.textContent = 'La fecha de Check-out debe ser posterior a la de Check-in.';
            availabilityMessage.style.color = 'var(--error-color)';
            return;
        }

        try {
            const response = await fetch(`/check-availability?checkin=${checkinDate}&checkout=${checkoutDate}`);
            const data = await response.json();

            if (response.ok && data.available_room_ids) {
                if (data.available_room_ids.includes(parseInt(roomTypeId))) {
                    btnReservar.disabled = false;
                    availabilityMessage.textContent = '¡Este paquete está disponible para las fechas seleccionadas!';
                    availabilityMessage.style.color = 'var(--success-color)';
                } else {
                    btnReservar.disabled = true;
                    availabilityMessage.textContent = 'Lo sentimos, este paquete no está disponible para las fechas seleccionadas.';
                    availabilityMessage.style.color = 'var(--error-color)';
                }
            } else {
                btnReservar.disabled = true;
                availabilityMessage.textContent = 'Error al verificar disponibilidad. Intenta de nuevo más tarde.';
                availabilityMessage.style.color = 'var(--error-color)';
                console.error('Error en la respuesta de disponibilidad:', data.error || 'Mensaje desconocido');
            }
        } catch (error) {
            btnReservar.disabled = true;
            availabilityMessage.textContent = 'No se pudo conectar con el servidor para verificar disponibilidad.';
            availabilityMessage.style.color = 'var(--error-color)';
            console.error('Fallo de conexión al verificar disponibilidad:', error);
        }
    }

    // Event listeners
    checkinInput.addEventListener('change', updateAvailability);

    // Inicializar el estado del formulario al cargar la página
    updateAvailability();


    // Listener para el envío del formulario de reserva de paquete
    formReservaPaquete.addEventListener('submit', async function(event) {
        event.preventDefault(); // Evita el envío tradicional del formulario

        if (btnReservar.disabled) {
            alert('Por favor, selecciona fechas válidas y verifica la disponibilidad antes de reservar.');
            return;
        }

        const checkinDate = checkinInput.value;
        const checkoutDate = checkoutInput.value; // Ya calculado por updateAvailability
        const customerName = document.getElementById('name-paquete').value;
        const customerEmail = document.getElementById('email-paquete').value;
        const adults = parseInt(document.getElementById('adults-paquete').value, 10);
        const children = parseInt(document.getElementById('children-paquete').value, 10);

        if (!checkinDate || !checkoutDate || !customerName || !customerEmail || isNaN(adults) || isNaN(children)) {
            alert('Por favor, completa todos los campos obligatorios.');
            return;
        }
        if (adults < 1) {
            alert('Debe haber al menos un adulto.');
            return;
        }
        if (children < 0) {
            alert('La cantidad de menores no puede ser negativa.');
            return;
        }

        const reservationData = {
            package_id: parseInt(paqueteId, 10),
            checkin_date: checkinDate,
            checkout_date: checkoutDate, // Pasamos el checkout calculado para mayor consistencia
            customer_name: customerName,
            customer_email: customerEmail,
            adults: adults,
            children: children
        };

        try {
            const response = await fetch('http://localhost:5001/reservations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(reservationData)
            });

            const result = await response.json();

            if (response.ok) {

                alert('¡Reserva de paquete creada con éxito!');
                const reservationMailData = {
                    reservation_type: "paquete",
                    package_id: parseInt(paqueteId, 10),
                    checkin_date: checkinDate,
                    checkout_date: checkoutDate,
                    customer_name: customerName,
                    customer_email: customerEmail,
                    adults: adults,
                    children: children
                }
                fetch ('/confirmacion-mail', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(reservationMailData)
                });
                window.location.href = '/confirmacion';
            } else {
                alert(`Error al crear la reserva: ${result.message || 'Error desconocido'}`);
                console.error('Error al crear la reserva:', result);
            }
        } catch (error) {
            alert('No se pudo conectar con el servidor para procesar la reserva.');
            console.error('Error de red al crear la reserva:', error);
        }
    });
});