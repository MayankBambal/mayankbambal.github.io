import './styles.scss';
import Flickity from 'flickity';

// Initialize Flickity carousel if element exists
document.addEventListener('DOMContentLoaded', () => {
  const carousel = document.querySelector('.carousel');
  if (carousel) {
    new Flickity(carousel, {
      cellAlign: 'left',
      contain: true,
      pageDots: false,
      wrapAround: true
    });
  }
}); 