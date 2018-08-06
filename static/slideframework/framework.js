class SlideFramework {

    /**
     * Initialize SlideFramework with configuration.
     */
    static initialize(templateconfig = {}) {
	SlideFramework.configuration     = false;
	SlideFramework.eBody             = $('#slidesframework-body');
	SlideFramework.eControllers      = $('#slidesframework-controllers');
	SlideFramework.templateconfig    = templateconfig;
	
	$('body').on('slideframework__configuration__loaded', function() {
	    SlideFramework.loadUI();
	});
	
	$.getJSON('/config.json', function(data) {
	    SlideFramework.configuration = data;

	    // Broadcast a message warning that configuration is loaded now.
	    $('body').trigger('slideframework__configuration__loaded');
	});
    }

    /**
     * Load UI from configuration.
     */
    static loadUI() {
	SlideFramework.eControllers.append('<li id="slideframework-counter-slide"></li>');
	SlideFramework.eControllers.append('<li id="slideframework-previous-slide"><i class="fa fa-chevron-left"></i></li>');
	SlideFramework.eControllers.append('<li id="slideframework-next-slide"><i class="fa fa-chevron-right"></i></li>');

	var eCounter = $('#slideframework-counter-slide');
	eCounter.append('<span id="current-slide">1</span>');
	eCounter.append(' de <span>' + SlideFramework.configuration['slides'].length + '</span>');

	SlideFramework.currentSlide = $('#current-slide');

	if (location.hash !== '') {
	    SlideFramework.currentSlide.text(location.hash.substring(1));
	}
	
	$( "body" ).keyup(function(event) {
	    if (event.keyCode == 39) {
		SlideFramework.loadNextSlide();
	    } else if (event.keyCode == 37) {
		SlideFramework.loadPreviousSlide();
	    }
	});
	$('#slideframework-previous-slide').click(function() {
	    SlideFramework.loadPreviousSlide();
	});

	$('#slideframework-next-slide').click(function() {
	    SlideFramework.loadNextSlide();
	});

	SlideFramework.loadCurrentSlide();
    }

    /**
     * Load previous slide.
     */
    static loadPreviousSlide() {
	var currentSlide = parseInt(SlideFramework.currentSlide.text());

	if (currentSlide <= 1) {
	    return;
	}
	
	SlideFramework.currentSlide.html(currentSlide - 1);

	$('body').trigger('slideframework__previous__slide');
	SlideFramework.loadCurrentSlide();
    }

    /**
     * Load previous slide.
     */
    static loadNextSlide() {
	var currentSlide = parseInt(SlideFramework.currentSlide.text());

	if (currentSlide >= SlideFramework.configuration['slides'].length) {
	    return;
	}

	SlideFramework.currentSlide.html(currentSlide + 1);
	$('body').trigger('slideframework__next__slide');

	SlideFramework.loadCurrentSlide();
    }

    /**
     * Load the current selected slide.
     */
    static loadCurrentSlide() {
	var currentSlide = parseInt(SlideFramework.currentSlide.text()) - 1;

	if (currentSlide < 0 || currentSlide > SlideFramework.configuration['slides'].length) {
	    return;
	}

	location.hash = currentSlide + 1;

	var path = "/my-presentation/" + SlideFramework.configuration['slides'][currentSlide];

	SlideFramework.eBody.fadeOut('fast', function() {
	    $.get(path, function(data) {
		SlideFramework.eBody.html(data);

		SlideFramework.eBody.fadeIn('fast', function() {
		    $('body').trigger('slideframework__slide__loaded');
		});

		MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
	    });
	});
    }
}
