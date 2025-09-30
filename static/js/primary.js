document.addEventListener('DOMContentLoaded', function(){
    const goBackButton = document.querySelector('#goback');

    if (goBackButton){
        if (document.URL.at(-1) === '/'){
            goBackButton.style.display = 'none';
            return;
        };

        goBackButton.addEventListener('onClick', function(){
            window.history.back();
        });
    };
})