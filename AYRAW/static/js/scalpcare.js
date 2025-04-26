function scrollLeft() {
    document.getElementById('productCarousel').scrollBy({
        left: -300,
        behavior: 'smooth'
    });
}

function scrollRight() {
    document.getElementById('productCarousel').scrollBy({
        left: 300,
        behavior: 'smooth'
    });
}
