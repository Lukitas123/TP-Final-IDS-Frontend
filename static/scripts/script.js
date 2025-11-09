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
