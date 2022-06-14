// Offset for Site Navigation
$('#siteNav').affix({
	offset: {
		top: 100
	}
})
$("#SubmitButton").submit( function() {
    $('body').scrollTo('#result',{duration:2000});
    return false;
});