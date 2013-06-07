/*jslint sloppy: true, vars: true, white: true, plusplus: true, newcap: true */
/*global window, $*/

$(function() {
    $(window).resize(function() {
        $("h1, h2, h3, p").css("z-index", 1);
    });
});