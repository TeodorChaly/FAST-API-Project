
function changeLanguage(selectedLanguage) {
    const urlParts = window.location.pathname.split('/');
    urlParts[1] = selectedLanguage;
    window.location.pathname = urlParts.join('/');
}