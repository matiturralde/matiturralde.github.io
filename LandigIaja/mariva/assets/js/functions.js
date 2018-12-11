var sendMonto = 150000; 
var sendPlazo = null;

jQuery(document).ready(function ($) {
    "use strict";
    // jQuery("body").niceScroll();
    var lastScrollTop = 0;
    jQuery(window).on("scroll", function () {
        var st = $(this).scrollTop();
        st > lastScrollTop ? $(".floating-nav").addClass("is-hidden") : $(window).scrollTop() > 200 ? ($(".floating-nav").removeClass("is-hidden"), setTimeout(function () {}, 200)) : $(".floating-nav").addClass("is-hidden"), lastScrollTop = st, 0 == $(this).scrollTop() && $(".floating-nav").addClass("is-hidden");
    });

    jQuery("#credit_range").ionRangeSlider({
        min: 50000,
        max: 500000,
        from: 150000,
        step: 10000,
        prefix: '$ '
    });

    jQuery("#credit_range2").ionRangeSlider({
        min: 3,
        max: 12,
        from: 6,
        step: 1,
        postfix: ' meses'
        
        
    });    

    jQuery('.testimonials-slider').owlCarousel({
        items: 1,
        loop: true,
        nav: true,
        center: true,
        autoplay: false,
        autoplayTimeout: 6000,
        // animateIn: 'fadeIn',
        // animateOut: 'fadeOut',
    });


}); /* end of as page load scripts */

AOS.init({
    easing: 'ease-in-out',
});

function currency(value) {
    var result = value.toFixed(0).replace(/./g, function (c, i, a) {
        return i && c !== "," && ((a.length - i) % 3 === 0) ? '.' + c : c;
    });
    return result;
}



function simularCreditoCuotas() {
    var monto = $('#credit_range').val() || 100000;
    monto = parseFloat(monto);

    var plazo = $('#credit_time').val();
    

    var cuotaMin = 0;
    var cuotaMax = 0;

    switch (plazo) {
        case 'false':
            cuotaMax = monto * 0.206577089589019;
            break;
        case 'true':
            cuotaMax = monto * 0.122245549919824;
            break;
        default:
            break;
    }

    var formattedMin = currency(cuotaMin);
    var formattedMax = currency(cuotaMax);

    window.sendMonto = $('#credit_range').val() || 100000;
    window.sendPlazo = $('#credit_time').val();

    var result = formattedMax;

    jQuery('.credit-calculator-value').html(result);
}


jQuery('#credit_range').change(function () {
    simularCreditoCuotas();
});

/*agregue esta funcion*/

jQuery('#changeTime').change(function () {
    simularCreditoCuotas();
});


jQuery('#credit_time').change(function () {
    var plazo = '';
    if ($('#credit_time').val() === 'false') {
        $('#credit_time').val('true');
    } else {
        $('#credit_time').val('false');
    }
    simularCreditoCuotas();
});

function doFunction() {
    if (window.sendPlazo == 'true') {
        window.location.href = "https://onboarding.credility.com/mariva/" + window.sendMonto + "/12";
    } else {
        window.location.href = "https://onboarding.credility.com/mariva/" + window.sendMonto + "/6";
    } 
}
