$(document).ready(function($) {
    setupContentMenu($);
    setupHandlers($);
    setupNavigation($);
});

function setupContentMenu($) {
    // insert content add-menu into document menu
    var objectMenu = $('#objectMenu').get(0);
    objectMenu.innerHTML = $('#collage-addmenu').get(0).innerHTML;
    
    // we must reinitialize all action-menus
    initializeMenus();
}

function setupHandlers($) {
    // setup collapsing blocks 
    $.each($("div.expandable-section/a.expandable-label"), function(i, o) {
	$(o).bind('click', function() {
	    var section = $(o).parent();
	    var content = $("div.expandable-content", section);
	    var container = section.parents('.collage-row').eq(0)
	    var url = $(o).attr('href');
		    
	    if ($(o).attr('class').indexOf('enabled') != -1) {
		// disable
		content.css('display', 'none');
		container.next('.collage-row').eq(0).css('margin-top', 0+'px');
	    } else {
		// enable
		content.css('display', 'block');

		// handle height (for IE6)
		container.next('.collage-row').eq(0).css('margin-top', 1+'px');
		
		// handle ajax sections
		$.each($(".expandable-ajax-content", section), function(j, p) {
		    $(p).load(url, function() {
			container.next('.collage-row').eq(0).css('margin-top', 1+'%');
			setupExistingItemsForm($);
		    });
		});
	    }
	    
	    $(o).toggleClass('enabled').blur();
	    return false;
	});
    });
}

function setupExistingItemsForm($) {
    $("form.collage-existing-items//select").change(function(event) {
	this.blur();

	// serialize form
	var form = $(this).parents('form').eq(0);
	var url = form.attr('action');
	var inputs = $(':input', form);

	// refresh form
	var section = $(this).parents('.expandable-ajax-content').eq(0);
	section.load(url, extractParams(inputs.serialize()),
		     function() { setupExistingItemsForm($); });
    });
}

function setupNavigation($) {
    // transform navigation links into ajax-methods
    $("a.collage-js-down").bind('click', {jquery: $}, triggerMoveDown);
    $("a.collage-js-up").bind('click', {jquery: $}, triggerMoveUp);
}

function postMessage(element, msg) {
    element._contents = element.innerHTML;
    element.innerHTML += ' ('+msg+')';
}

function restoreElement(element) {
    element.innerHTML = element._contents;
}

function doSimpleQuery(url, data) {
    // perform simple ajax-call
    var href = url.split('?');
    var url = href[0];
    data = (href.length > 1) ? extractParams(href[1]) : {};
	
    // avoid aggresive IE caching
    data['url'] = (new Date()).getTime();

    // set simple flag
    data['simple'] = 1
    
    // display a save message
    var heading = $('h1.documentFirstHeading').get(0);
    postMessage(heading, 'Saving...');

    $.post(url, data, function(data) {
	restoreElement(heading);
    });
}

function extractParams(query) {
    // convert a query-string into a dictionary
    var data = {};
    var params = query.split('&');
    for (var i=0; i<params.length; i++) {
	var pair = params[i].split('=');
	data[pair[0]] = pair[1];
    }

    return data;
}

function triggerMoveDown(event) {
    return triggerMove.call(this, event, +1);
}

function triggerMoveUp(event) {
    return triggerMove.call(this, event, -1);
}

function triggerMove(event, direction) {
    $ = event.data.jquery;
    event.preventDefault();

    var link = $(this);
    link.blur();
    
    var className = event.data.className;
    
    var row = link.parents('.collage-row').eq(0);
    var column = link.parents('.collage-column').eq(0);

    var destination = null;
    var origin = null;
    var items = null;
    
    if (column.length) {
	items = $('.collage-column', row);
	origin = $(column);
    } else {
	items = $('.collage-row');
	origin = $(row);
    }

    var index = items.index(origin.get(0));
    if (!(index+direction >= 0 && index+direction < items.length)) return false;
    
    destination = $(items[index+direction]);
    swap(origin, destination);

    doSimpleQuery(link.attr('href'));    
}

function swap(origin, destination) {
    var temp = origin.after('<span></span>').next();
    destination.after(origin);
    destination.insertBefore(temp);
    temp.remove();
}