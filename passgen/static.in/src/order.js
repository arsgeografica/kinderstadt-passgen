var $ = require('jquery'),
    throttle = require('lodash/function/throttle');


var body = $('body');

var query = throttle(function() {
    var q = $.ajax({
        cache: false,
        dataType: 'json'
    });

    q.done(function query_success(order) {
        if(order.finished) {
            body.removeClass('waiting')
                .addClass('ready');
        } else {
            query();
        }
    });

    q.fail(function query_error() {
        body.removeClass('waiting')
            .addClass('error');
    });
}, 2500);

query();
