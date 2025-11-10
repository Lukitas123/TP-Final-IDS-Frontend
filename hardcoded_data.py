from typing import Dict, List, Any

DATA: Dict[str, List[Any]] = {
    "tipo_habitacion": [
        {
            "id": 1,
            "nombre": "Estándar Clásica",
            "descripcion": """
            Nuestra habitación Estándar es el refugio perfecto para el viajero eficiente.
            - **Distribución:** 25m² optimizados. Habitación monoambiente con cama Queen (1.60m x 2.00m) y un baño privado completo con ducha de alta presión.
            - **Especificaciones:** Escritorio de trabajo ergonómico, Wi-Fi de alta velocidad (100mbps), y un Smart TV de 40" con acceso a streaming.
            - **Lujos:** Incluye una mini-nevera surtida (costo adicional), sábanas de algodón de 200 hilos y set de amenities básicos de bienvenida.
            """,
            "galeria": "['/images/tipo_habitacion/estandar/estandar-1.png', '/images/tipo_habitacion/estandar/estandar-2.png', '/images/tipo_habitacion/estandar/estandar-3.png']",
        },
        {
            "id": 2,
            "nombre": "Doble Superior (Vista Jardín)",
            "descripcion": """
            Espaciosa y luminosa, la Doble Superior de 35m² está diseñada para compartir sin sacrificar confort.
            - **Distribución:** Habitación amplia con dos camas Matrimoniales (1.40m x 1.90m), asegurando el descanso de hasta 4 huéspedes.
            - **Especificaciones:** Gran ventanal con vistas a los jardines interiores del hotel. El baño es amplio, con doble lavamanos y bañera.
            - **Lujos:** Cafetera Nespresso con 4 cápsulas de cortesía por día, Smart TV de 50" y un pequeño rincón de lectura con sillón.
            """,
            "galeria": "['/images/tipo_habitacion/doble-superio/doble-superior-1.jpg', '/images/tipo_habitacion/doble-superio/doble-superior-2.jpg', '/images/tipo_habitacion/doble-superio/doble-superior-3.jpg']",
        },
        {
            "id": 3,
            "nombre": "Junior Suite Ejecutiva",
            "descripcion": """
            Un upgrade de lujo en un solo ambiente de 50m², pensada para el viajero de negocios o el placer exigente.
            - **Distribución:** Cama King Size (2.00m x 2.00m) con sábanas de algodón egipcio de 400 hilos. La distribución integra una sala de estar con sofá y mesa de centro.
            - **Especificaciones:** Baño revestido en mármol, equipado con bañera de hidromasaje y ducha escocesa separada.
            - **Lujos:** Smart TV curvo de 60", sistema de sonido Bluetooth, y acceso exclusivo a nuestro 'Executive Lounge' (desayuno privado y cócteles de cortesía por la tarde).
            """,
            "galeria": "['/images/tipo_habitacion/junior/junior-1.jpg', '/images/tipo_habitacion/junior/junior-2.jpg', '/images/tipo_habitacion/junior/junior-3.jpg', '/images/tipo_habitacion/junior/junior-4.jpg']",
        },
        {
            "id": 4,
            "nombre": "Suite 'Nido de Amor'",
            "descripcion": """
            Diseñada exclusivamente para parejas que buscan... reconectar. La experiencia definitiva para una escapada romántica.
            - **Distribución:** 70m² de puro romance. Es una suite dúplex: la planta baja cuenta con una sala de estar privada, chimenea eléctrica y un balcón con hamaca para dos. La planta alta es el dormitorio principal.
            - **Especificaciones:** La legendaria cama King Size redonda (2.20m diámetro) con sábanas de seda y un discreto (pero estratégico) espejo en el techo.
            - **Lujos:** El protagonista es el jacuzzi doble con cromoterapia situado DENTRO del dormitorio, junto a un ventanal con vistas a la ciudad. Incluye 'Kit Romántico' de bienvenida (botella de champagne, fresas con chocolate y aceites de masaje). Sistema de sonido envolvente con playlist 'Reavivando la Llama' pre-cargada. Privacidad 100% garantizada.
            """,
            "galeria": "['/images/tipo_habitacion/parejas/parejas-1.jpg', '/images/tipo_habitacion/parejas/parejas-2.jpg', '/images/tipo_habitacion/parejas/parejas-3.jpg']",
        },
    ],
    "servicio": [
        {
            "nombre": "Recepción 24 horas",
            "descripcion": "Asistencia a los huespedes en todo momento",
            "imagen": 'images/servicios/recepcion.jpeg',
            "icono": "🛎️"
        },
        {
            "nombre": "Limpieza",
            "descripcion": "Servicio regular de limpieza y mantenimiento",
            "imagen": 'images/servicios/limpieza.jpg',
            "icono": "🫧"
        },
        {
            "nombre": "Conectividad",
            "descripcion": "Acceso a internet Wi-Fi",
            "imagen": 'images/servicios/conectividad.jepg',
            "icono": "🛜"
        },
        {
            "nombre": "Restauración",
            "descripcion": "Desayuno, almuerzo y cena. Servicio a la habitación o restaurantes",
            "imagen": 'images/servicios/restauracion.jpeg',
            "icono": "🍱"

        }
    ],
    "actividad": [
        {
            "id": 1,
            "nombre": "Tour turístico",
            "descripcion": "Viaje en micro turístico de 2 pisos a través de los puntos centrales e icónicos de la ciudad",
            "precio": "30 USD",
            "galeria": 'images/actividades/actividad-1.jpeg',
	        "cronograma": "Lunes a Viernes, salida a las 10, 11, 13 y 15hs",
        }, 
       {
            "id": 2,
            "nombre": "Visita a museos",
            "descripcion": "Visita a museos selectos guiados por nuestro staff. Salida desde la puerta del hotel en vehículo de la empresa",
            "precio": "10 USD",
            "galeria": 'images/actividades/actividad-2.jpeg',
	        "cronograma": "Lunes a Viernes, salida a las 11hs y las 13hs",
        },
         {
            "id": 3,
            "nombre": "Visita a bodegas y degustación de vinos",
            "descripcion": "Visita a las bodegas afiliadas donde podrán degustar los deliciosos vinos regionales. Salida desde la puerta del hotel en vehículo de la empresa. Actividad no permitida para menores de 18 años",
            "precio": "25 USD",
            "galeria": 'images/actividades/actividad-3.jpeg',
	        "cronograma": "Miercoles y Viernes, salida a las 11hs",
        }, 

         {
            "id": 4,
            "nombre": "Paseo en aeronave",
            "descripcion":  "Paseo en aeroplano donde podrá disfrutar de la hermosa vista y tener una experiencia única",
            "precio": "70 USD",
            "galeria": 'images/actividades/actividad-4.jpeg',
	         "cronograma": "Sabados a las 9, 13 y 17hs",
        }, 
    ],
    "paquete": [
        {
            "id": 1,
            "nombre": "Escapada Romántica Deluxe",
            "descripcion": """
        Ideal para parejas que buscan desconectar del mundo y reconectar entre sí.
        - **Duración:** 2 noches / 3 días.
        - **Hospedaje:** Suite "Nido de Amor" con jacuzzi doble y vista panorámica.
        - **Gastronomía:** Cena romántica de 5 pasos en el restaurante 'Cielos del Valle', con maridaje premium.
        - **Experiencia:** Masaje relajante en pareja (60 minutos) y acceso ilimitado al spa termal.
        """,
            "incluye": [
                "Desayuno buffet gourmet en habitación.",
                "Kit romántico de bienvenida (champagne + fresas con chocolate).",
                "Late check-out hasta las 14:00 hs (sujeto a disponibilidad).",
            ],
            "precio": 165000,
            "galeria": "['#', '#', '#']",
        },
        {
            "id": 2,
            "nombre": "Experiencia Wellness & Spa Total",
            "descripcion": """
        Un retiro de bienestar corporal y mental en el corazón del hotel.
        - **Duración:** 3 noches / 4 días.
        - **Hospedaje:** Junior Suite Ejecutiva con acceso exclusivo al Lounge.
        - **Gastronomía:** Menú saludable diseñado por nuestro chef nutricionista.
        - **Experiencia:** Circuito completo de hidroterapia, sauna seco, baño de vapor y masajes holísticos.
        """,
            "incluye": [
                "Clase privada de yoga al amanecer.",
                "Infusiones naturales y snacks saludables durante toda la estadía.",
                "Acceso ilimitado al gimnasio y piscina climatizada interior.",
            ],
            "precio": 210000,
            "galeria": "['#', '#', '#']",
        },
        {
            "id": 3,
            "nombre": "Escapada Gourmet & Vinos",
            "descripcion": """
        Una experiencia gastronómica exclusiva para paladares exigentes.
        - **Duración:** 2 noches / 3 días.
        - **Hospedaje:** Doble Superior con vista a los jardines.
        - **Gastronomía:** Degustación privada de 6 vinos argentinos con sommelier del hotel.
        - **Experiencia:** Taller de cocina regional con nuestro chef ejecutivo.
        """,
            "incluye": [
                "Desayuno buffet con estación de pastelería artesanal.",
                "Cena temática de 4 pasos con maridaje.",
                "Tour por bodega boutique asociada (transporte incluido).",
            ],
            "precio": 185000,
            "galeria": "['#', '#', '#']",
        },
        {
            "id": 4,
            "nombre": "Semana Ejecutiva Premium",
            "descripcion": """
        Perfecto para profesionales que necesitan equilibrio entre trabajo y descanso.
        - **Duración:** 5 noches / 6 días.
        - **Hospedaje:** Junior Suite Ejecutiva con escritorio ergonómico y vista panorámica.
        - **Servicios:** Espacio de coworking, coffee break diario y asistencia personalizada.
        - **Experiencia:** Masaje antiestrés express y afterwork de bienvenida en el Lounge.
        """,
            "incluye": [
                "Desayuno ejecutivo diario.",
                "Servicio de lavandería express gratuito (hasta 5 prendas).",
                "Upgrade de Wi-Fi a 300 Mbps y prioridad de habitación silenciosa.",
            ],
            "precio": 245000,
            "galeria": "['#', '#', '#']",
        },
    ],
}