let width, height;

$(()=>{
    width = $('.beam').width();
    height = $('.beam').height();
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
        $('.beam').css({'width': `${width}px`});
        $('.beam').css({'height': `${height}px`});
    }, 3000);
});