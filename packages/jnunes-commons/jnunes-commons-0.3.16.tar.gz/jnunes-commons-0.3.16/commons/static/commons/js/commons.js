/* global bootstrap: false */
(() => {
    'use strict'
    const tooltipTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.forEach(tooltipTriggerEl => {
        new bootstrap.Tooltip(tooltipTriggerEl)
    })
})()

/* function used 'pagination' component with ajax*/
function navigate(page, callbackList) {
    let parameters = JSUtils.getQueryParameters();
    parameters.set('page', page);

    // function called to return next values
    Array.from(callbackList.join()).forEach(callback => callback(parameters))
}
