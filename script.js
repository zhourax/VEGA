let currentIndex = 0;

const carouselContainer = document.querySelector('.carousel-container');
const items = document.querySelectorAll('.carousel-item');
const totalItems = items.length;

document.querySelector('.prev').addEventListener('click', () => {
    currentIndex = (currentIndex === 0) ? totalItems - 1 : currentIndex - 1;
    updateCarousel();
});

document.querySelector('.next').addEventListener('click', () => {
    currentIndex = (currentIndex === totalItems - 1) ? 0 : currentIndex + 1;
    updateCarousel();
});

function updateCarousel() {
    const offset = -currentIndex * 100;
    carouselContainer.style.transform = `translateX(${offset}%)`;
}