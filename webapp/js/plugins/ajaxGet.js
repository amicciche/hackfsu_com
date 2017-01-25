/**
 * Ajax GET request wrapper with correct headers and using promises
 */

(function($) {

    var defaultAjaxSettings = {
        type: 'GET',
        headers: {
            'HTTP_X_CSRFTOKEN': Cookies.get('csrftoken')
        }
    };

    $.ajaxGet = function(options) {
        var o = $.extend({}, defaultAjaxSettings, options);

        if (!o.error) {
            o.error = function(response) {
                console.error('Server Error:', response);
                var err = JSON.parse(response.responseText);
                alert(err.cause + ': ' + err.message);
            }
        }

        return $.ajax(o);
    }
})(jQuery);