// Smooth Scroll
function scrollToSection(id) {
  const section = document.querySelector(id);
  if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
  } else {
      console.warn(`Section ${id} not found.`);
  }
}

// Appointment Booking
const appointmentForm = document.querySelector('#appointment-form');
if (appointmentForm) {
  appointmentForm.addEventListener('submit', function (e) {
      e.preventDefault();
      alert('Your appointment has been booked successfully!');
      appointmentForm.reset(); // Clear the form after submission
  });
} else {
  console.warn('Appointment form not found.');
}

// Add to Cart
const shopButtons = document.querySelectorAll('#shop button');
if (shopButtons.length > 0) {
  shopButtons.forEach(button => {
      button.addEventListener('click', () => {
          alert('Item added to cart!');
      });
  });
} else {
  console.warn('No shop buttons found.');
}

// Newsletter Subscription
const newsletterForm = document.querySelector('#newsletter-form');
if (newsletterForm) {
  newsletterForm.addEventListener('submit', function (e) {
      e.preventDefault();
      alert('Thank you for subscribing to our newsletter!');
      newsletterForm.reset(); // Clear the form after submission
  });
} else {
  console.warn('Newsletter form not found.');
}

// Music Controls
const backgroundMusic = document.getElementById('background-music');
const playMusicButton = document.getElementById('play-music');
const pauseMusicButton = document.getElementById('pause-music');

if (backgroundMusic && playMusicButton && pauseMusicButton) {
  playMusicButton.addEventListener('click', () => {
      backgroundMusic.play().catch(error => {
          console.error('Error playing music:', error);
      });
  });

  pauseMusicButton.addEventListener('click', () => {
      backgroundMusic.pause();
  });
} else {
  console.warn('Music controls or background music element not found.');
}
