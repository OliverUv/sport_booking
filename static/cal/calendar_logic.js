function initializeCalendar(calendarData) {

    function onDayClick(date, allDay, jsEvent, view) {
	var theData = {};
	theData['timestamp'] = date.getTime()/1000;
	theData['resource_id'] = calendarData.resource_id;
	$.ajax({
	    url: calendarData.reservation_url,
	    type: "POST",
	    dataType: "json",
	    data: theData,
	}).done(function() {
	    $('#' + calendarData.element_id).fullCalendar('refetchEvents');
	}).fail(showAjaxFailure);
    }

    function deleteEvent(eventId) {
	n = noty({
	    text: "Do you want to remove event #" + eventId,
	    type: 'error',
	    dismissQueue: true,
	    layout: 'center',
	    buttons: [{
		addClass: 'btn btn-danger', text: 'Delete', onClick: function($noty) {
		    $noty.close();
		    $.ajax({
			url: calendarData.delete_url,
			type: "POST",
			dataType: "json",
			data: {id: eventId},
		    }).done(function() {
			$('#' + calendarData.element_id).fullCalendar('refetchEvents');
		    }).fail(showAjaxFailure);}}, {
		addClass: 'btn btn-primary', text: 'Cancel', onClick: function($noty) {
		    $noty.close();
		    $('#' + calendarData.element_id).fullCalendar('refetchEvents');
		}
	    }]
	});
    }

    function overwriteEvent(calEvent) {
	n = noty({
	    text: "Do you want to overwrite event #" + calEvent.id,
	    type: 'error',
	    dismissQueue: true,
	    layout: 'center',
	    buttons: [{
		addClass: 'btn btn-danger', text: 'Overwrite', onClick: function($noty) {
		    $noty.close();
		    $.ajax({
			url: calendarData.overwrite_url,
			type: "POST",
			dataType: "json",
			data: {id: calEvent.id},
		    }).done(function() {
			$('#' + calendarData.element_id).fullCalendar('refetchEvents');
		    }).fail(showAjaxFailure);}}, {
		addClass: 'btn btn-primary', text: 'Cancel', onClick: function($noty) {
		    $noty.close();
		    $('#' + calendarData.element_id).fullCalendar('refetchEvents');
		}
	    }]
	});
    }

    function onEventClick(calEvent, jsEvent, view) {
	if (calEvent.is_own) {
	    deleteEvent(calEvent.id);
	} else if (calEvent.solidity == "preliminary"){
	    overwriteEvent(calEvent);
	} else {
	    n = noty({
		text: "You cannot overwrite a solid reservation.",
		type: 'error',
		dismissQueue: true,
		layout: 'topRight',
		timeout: 3800
	    });
	}
    }

    calData = {
	firstDay: 1,
	defaultView: calendarData.view,
	editable: true,
	disableResizing: true,
	allDayDefault: false,
	allDaySlot: false,
	defaultEventMinutes: 60,
	firstHour: 10,
	height: 500,
	columnFormat: 'ddd d/M',
	titleFormat: {
	    month: 'MMMM yyyy',                             // September 2009
	    week: "MMM d[',' yyyy]{ '&#8212;'[ MMM] d',' yyyy}", // Sep 7 - 13 2009
	    day: 'dddd, MMM d, yyyy'                  // Tuesday, Sep 8, 2009
	},
	eventSources: [{url: calendarData.resource_event_url}],
	dayClick: onDayClick,
	eventClick: onEventClick
    };
    if (calendarData.hasOwnProperty('header')) {
	calData.header = calendarData.header;
    }
    $('#' + calendarData.element_id).fullCalendar(calData);
}
