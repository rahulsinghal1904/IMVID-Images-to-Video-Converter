// Offset for Site Navigation
$('#siteNav').affix({
	offset: {
		top: 100
	}
})
$("#SeeVideo").click(function() {
    $('html, body').animate({
        scrollTop: $("#video").offset().top
    }, 2000);
});