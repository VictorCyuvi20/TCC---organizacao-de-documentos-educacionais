const goBackButton = document.querySelector('#go-back');

if (goBackButton){
    if (document.URL.at(-1) === '/'){
        goBackButton.style.display = 'none';
        return;
    };

    goBackButton.addEventListener('onClick', function(){
        window.history.back();
    });
};