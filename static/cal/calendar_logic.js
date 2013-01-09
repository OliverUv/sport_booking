function generalOnDayClick(date, allDay, jsEvent, view, resource_id, reservation_url) {
    var theData = {};
    theData['timestamp'] = date.getTime()/1000;
    theData['resource_id'] = resource_id;
    $.ajax({
	url: reservation_url,
	type: "POST",
	dataType: "json",
	data: theData,
    }).done(function() {
	$('#calendar').fullCalendar('refetchEvents');
    }).fail(showAjaxFailure);
}

function deleteEvent(eventId, delete_url) {
    n = noty({
	text: "Do you want to remove event #" + eventId,
	type: 'error',
	dismissQueue: true,
	layout: 'center',
	buttons: [{
	addClass: 'btn btn-danger', text: 'Delete', onClick: function($noty) {
	    $noty.close();
	    $.ajax({
		url: delete_url,
		type: "POST",
		dataType: "json",
		data: {id: eventId},
	    }).done(function() {
		$('#calendar').fullCalendar('refetchEvents');
	    }).fail(showAjaxFailure);
	}
    },
      {
	  addClass: 'btn btn-primary', text: 'Cancel', onClick: function($noty) {
	      $noty.close();
	      $('#calendar').fullCalendar('refetchEvents');
	  }

      }]
    });
}

function showEventInfo(calEvent) {
    // TODO
}

function generalOnEventClick(calEvent, jsEvent, view, delete_url) {
    if (calEvent.is_own) {
	deleteEvent(calEvent.id, delete_url);
    } else {
	showEventInfo(calEvent);
    }
}

function initializeCalendar(resource_event_source_url, onDayClick, onEventClick) {
    $('#calendar').fullCalendar({
	firstDay: 1,
	defaultView: 'agendaWeek',
	editable: true,
	disableResizing: true,
	allDayDefault: false,
	allDaySlot: false,
	defaultEventMinutes: 60,
	firstHour: 10,
	columnFormat: 'ddd d/M',
	titleFormat: {
	    month: 'MMMM yyyy',                             // September 2009
	    week: "MMM d[',' yyyy]{ '&#8212;'[ MMM] d',' yyyy}", // Sep 7 - 13 2009
	    day: 'dddd, MMM d, yyyy'                  // Tuesday, Sep 8, 2009
	},
	eventSources: [{url: resource_event_source_url}],
	dayClick: onDayClick,
	eventClick: onEventClick
    });
}
