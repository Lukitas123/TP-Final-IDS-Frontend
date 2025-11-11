document.addEventListener('DOMContentLoaded', () => {
  // === NAVBAR ===
  const hamburger = document.querySelector('.hamburger');
  const navList = document.querySelector('.nav__list');

  // Toggle menu
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navList.classList.toggle('active');
  });

  // Close menu when clicking outside
  document.addEventListener('click', (e) => {
    if (!hamburger.contains(e.target) && !navList.contains(e.target)) {
      hamburger.classList.remove('active');
      navList.classList.remove('active');
    }
  });

  // Close menu when clicking a link
  const navLinks = document.querySelectorAll('.nav__link');
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('active');
      navList.classList.remove('active');
    });
  });

  // === FORM STATUS ALERTS ===
  const urlParams = new URLSearchParams(window.location.search);
  const status = urlParams.get('status');

  if (status === 'success') {
    alert('¡Mensaje enviado con éxito!');
  } else if (status === 'error') {
    alert('Hubo un error al enviar el mensaje. Por favor, inténtalo de nuevo.');
  }

  // === TESTIMONIALS CAROUSEL ===
  const testimonialCards = document.querySelectorAll('.testimonial-card');
  const prevButton = document.querySelector('.carousel__btn.prev');
  const nextButton = document.querySelector('.carousel__btn.next');
  let currentIndex = 0;

  function updateCarousel() {
    testimonialCards.forEach((card, index) => {
      card.classList.remove('active', 'prev', 'next');
      if (index === currentIndex) {
        card.classList.add('active');
      } else if (index === (currentIndex - 1 + testimonialCards.length) % testimonialCards.length) {
        card.classList.add('prev');
      } else if (index === (currentIndex + 1) % testimonialCards.length) {
        card.classList.add('next');
      }
    });
  }

  prevButton.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + testimonialCards.length) % testimonialCards.length;
    updateCarousel();
  });

  nextButton.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % testimonialCards.length;
    updateCarousel();
  });

  // Inicializar
  updateCarousel();
});

// Carrusel simple para servicios
const carouselState = {};

function moveSlide(servicioId, direction) {
  const container = document.getElementById(`carousel-${servicioId}`);
  if (!container) return;

  const slides = container.children.length;
  carouselState[servicioId] = (carouselState[servicioId] || 0) + direction;

  if (carouselState[servicioId] < 0) carouselState[servicioId] = slides - 1;
  if (carouselState[servicioId] >= slides) carouselState[servicioId] = 0;

  container.style.transform = `translateX(-${carouselState[servicioId] * 100}%)`;
}