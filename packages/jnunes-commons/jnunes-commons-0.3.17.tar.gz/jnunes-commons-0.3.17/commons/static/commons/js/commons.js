/* global bootstrap: false */
(() => {
    'use strict'
    const tooltipTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.forEach(tooltipTriggerEl => {
        new bootstrap.Tooltip(tooltipTriggerEl)
    })
})()

// navigation
function navigate(page, ...callbacks) {
    let parameters = JSUtils.getQueryParameters();
    parameters.set('page', page);

    // function called to return next values
    callbacks.forEach(callback => callback(parameters))
}
