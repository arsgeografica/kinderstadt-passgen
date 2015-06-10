var $ = require('jquery'),
    throttle = require('lodash/function/throttle');


var body = $('body'),
    progress_bar = $('.progress .progress-bar');

var query = throttle(function() {
    var q = $.ajax({
        cache: false,
        dataType: 'json'
    });

    q.done(function query_success(order) {
        // Update progress bar
        progress_bar
            .css('width', order.progress + '%')
            .attr('aria-valuenow', order.progress)
            .text(order.progress + '%');

        // Advance status -> change view
        if(order.finished) {
            body.removeClass('waiting')
                .addClass('ready');
            progress_bar
                .removeClass('active')
                .removeClass('progress-bar-striped');
        } else {
            query();
        }
    });

    // On error -> show error view
    q.fail(function query_error() {
        body.removeClass('waiting')
            .addClass('error');
    });
}, 2500);

query();
