var didScroll;
var nav = $('.js-nav');

$(document).ready(function() {

    /* Custom scroll event */
	$(window).scroll(function(event){
		didScroll = true;
	});

	// run hasScrolled() and reset didScroll status
	setInterval(function() {
		if (didScroll) {
		  hasScrolled();
		  didScroll = false;
		}
    }, 10);

    // Scroll functions
	function hasScrolled() {
        // Header
       nav.toggleClass('-scrolled', $(window).scrollTop() > 0 /* header.outerHeight() */ );
        $("nav a.btn-white").toggleClass("btn-primary", $(window).scrollTop() > 0);
    };
    
    hasScrolled();

    $('.navbar-toggler').click(function() {
        if ($(window).scrollTop() <= 0) { 
            nav.toggleClass('-scrolled');
            $("nav a.btn-white").toggleClass("btn-primary");
        }
    });

});


