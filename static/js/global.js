function updateFaviconTheme(){
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        favicon.href = "/static/images/logo/white-notext48x48.png";
    }else{
        favicon.href = "/static/images/logo/black-notext48x48.png";
    };
};

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateFaviconTheme);
updateFaviconTheme();