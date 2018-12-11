$(window).on('load resize orientationchange', function() {
    $('.slider').each(function(){
        var $carousel = $(this);
        /* Initializes a slick carousel only on mobile screens */
        // slick on mobile
        if ($(window).width() > 768) {
            if ($carousel.hasClass('slick-initialized')) {
                $carousel.slick('unslick');
            }
        }
        else{
            if (!$carousel.hasClass('slick-initialized')) {
                $carousel.slick({
                    dots: true,
                    infinite: true,
                    speed: 300,
                    slidesToShow: 1,
                    //adaptiveHeight: true,
                    mobileFirst: true,
                });
            }
        }
    });
});

$(document).ready(function(){
    $('.testimonials').slick({
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1
      });
  });
