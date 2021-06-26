$(()=>{
    $('.beam').height('50vh');
    setTimeout(()=>{
        $('.beam').css({'margin-top': '50vh'});
        $('body').css({'justify-content': 'flex-start'});
        $('.beam').height(0);
    }, 1000);
    setTimeout(()=>{
        alert('done')
    }, 2000);
});