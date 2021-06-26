function beginAnimation() {
    let width = $('.beam').width();
    let height = $('.beam').height();
    $('.beam').width('0');
    $('.beam').height('0');
    console.log(1);
    setTimeout(()=>{
        $('.beam').css({'display': 'initial'});
        $('.beam').height('50%');
        console.log(2);
    }, 1000);
    setTimeout(()=>{
        $('.beam').css({'margin-top': '50vh'});
        $('body').css({'justify-content': 'flex-start'});
        $('.beam').height(0);
        console.log(3);
    }, 2000);
    setTimeout(()=>{
        $('body').css({'justify-content': 'center'});
        $('.beam').css({'margin-top': '0px'});
        $('.beam').width(width);
        $('.beam').height(height);
        console.log(4);
    }, 3000);
}

function endAnimation() {
    $('.beam').width('0');
    $('.beam').height('0');
    console.log(4);
    setTimeout(()=>{
        $('.beam').css({'margin-top': '50vh'});
        $('body').css({'justify-content': 'flex-start'});
        $('.beam').height('50%');
        console.log(3);
    }, 1000);
    setTimeout(()=>{
        $('body').css({'justify-content': 'flex-end'});
        $('.beam').css({'margin-top': '0px'});
        $('.beam').height(0);
        console.log(2);
    }, 2000);
    setTimeout(()=>{
        $('.beam').css({'display': 'none'});
        console.log(1);
    }, 3000);
}

$(_=>{
    console.log(hasStarted_host);
    if (hasStarted_host) return;
    hasStarted_host = true;
    beginAnimation();
});