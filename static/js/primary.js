document.addEventListener('DOMContentLoaded', function(){
    const goBackButton = document.querySelector('#goback');
    const navButtons = document.querySelectorAll('.navbar-option')

    if (goBackButton){
        if (document.URL.at(-1) === '/'){
            goBackButton.style.display = 'none';
            return;
        };

        goBackButton.addEventListener('click', function(){
            window.history.back();
        });
    };

    navButtons.forEach(button => {
        if (!button.tagName == 'A') return;

        if (button.pathname === window.location.pathname){
            button.classList.add('selected');
            console.log(button.pathname, window.location.pathname)
        };
    });
});