function beginAnimation() {
    let width = $('.beam').width();
    let height = $('.beam').height();
    let padding = $('.beam').css('padding');
    $('.beam').width('0')
              .height('0');
              .css({'padding': '0'});
    console.log(1);
    setTimeout(()=>{
        $('.beam').css({'display': 'initial'})
                  .height('50%');
        console.log(2);
    }, 1000);
    setTimeout(()=>{
        $('.beam').css({'margin-top': '50vh'});
                  .height(0);
        $('body').css({'justify-content': 'flex-start'});
        console.log(3);
    }, 2000);
    setTimeout(()=>{
        $('body').css({'justify-content': 'center'});
        $('.beam').css({'margin-top': '0px', 'padding': padding})
                  .width(width)
                  .height(height);
        console.log(4);
    }, 3000);
}

function endAnimation() {
    $('.beam').width('0')
              .height('0')
              .css({'padding': '0'});
    console.log(4);
    setTimeout(()=>{
        $('.beam').css({'margin-top': '50vh'})
                  .height('50%');
        $('body').css({'justify-content': 'flex-start'});
        console.log(3);
    }, 1000);
    setTimeout(()=>{
        $('body').css({'justify-content': 'flex-end'});
        $('.beam').css({'margin-top': '0px'})
                  .height(0);
        console.log(2);
    }, 2000);
    setTimeout(()=>{
        $('.beam').css({'display': 'none'});
        console.log(1);
    }, 3000);
}

function switchTo(action) {
    return function() {
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
        let items = $('body *'); // for the rare race condition.
        setTimeout(()=>{
            $('.beam').css({'display': 'none'});
            action();
            console.log(1);
        }, 3000);
        setTimeout(()=>{
            items.remove();
        }, 4000);
    }
}

$(_=>{
    console.log(hasStarted_host);
    if (hasStarted_host) return;
    hasStarted_host = true;
    beginAnimation();
});