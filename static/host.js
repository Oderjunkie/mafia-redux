function beginAnimation() {
    let width = $('.beam').width();
    let height = $('.beam').height();
    $('.beam').width('0');
    $('.beam').height('0');
    setTimeout(()=>{
        $('.beam').css({'display': 'initial'});
        $('.beam').height('50%');
    }, 1000);
    setTimeout(()=>{
        $('.beam').css({'margin-top': '50vh'});
        $('body').css({'justify-content': 'flex-start'});
        $('.beam').height(0);
    }, 2000);
    setTimeout(()=>{
        $('body').css({'justify-content': 'center'});
        $('.beam').css({'margin-top': '0px'});
        $('.beam').width(width);
        $('.beam').height(height);
    }, 3000);
}

function endAnimation() {
    $('.beam').width('0');
    $('.beam').height('0');
    setTimeout(()=>{
        $('.beam').css({'margin-top': '50vh'});
        $('body').css({'justify-content': 'flex-start'});
        $('.beam').height('50%');
    }, 1000);
    setTimeout(()=>{
        $('body').css({'justify-content': 'flex-end'});
        $('.beam').css({'margin-top': '0px'});
        $('.beam').height(0);
    }, 2000);
    setTimeout(()=>{
        $('.beam').css({'display': 'none'});
    }, 3000);
}

$(()=>{
    beginAnimation();
});