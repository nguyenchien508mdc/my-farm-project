//  common_static\js\formHandler.js

export function displayFormErrors(formSelector, errors) {
    $(`${formSelector} .invalid-feedback`).remove();
    $(`${formSelector} .is-invalid`).removeClass('is-invalid');
    if (!errors) return;

    for (let field in errors) {
        const messages = errors[field];
        const fieldElem = $(`${formSelector} [name="${field}"]`);
        if (fieldElem.length) {
            fieldElem.addClass('is-invalid');
            messages.forEach(msg => {
                fieldElem.after(`<div class="invalid-feedback">${msg}</div>`);
            });
        }
    }
}
