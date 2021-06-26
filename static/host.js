$(()=>{
    $('.beam').height('50%');
    setTimeout(()=>{
        $('.beam').css({'margin-top': '50vh'});
        $('body').css({'justify-content': 'flex-start'});
        $('.beam').height(0);
    }, 1000);
    setTimeout(()=>{
        $('body').css({'justify-content': 'center'});
        $('.beam').css({'margin-top': '0px'});
        $('.beam').css({'width': 'initial'});
        $('.beam').css({'height': 'initial'});
    }, 2000);
});