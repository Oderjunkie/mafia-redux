function beginAnimation() {
    let width = $('form').width();
    let height = $('form').height();
    let padding = $('form').css('padding');
    $('form').width('0')
             .height('0')
             .css({'padding': '0'});
    console.log(1);
    setTimeout(()=>{
        $('form').css({'display': 'initial'})
                 .height('50%');
        console.log(2);
    }, 200);
    setTimeout(()=>{
        $('form').css({'margin-top': '50vh'})
                 .height(0);
        $('body').css({'justify-content': 'flex-start'});
        console.log(3);
    }, 400);
    setTimeout(()=>{
        $('body').css({'justify-content': 'center'});
        $('form').css({'margin-top': '0px', 'padding': padding})
                 .width(width)
                 .height(height);
        console.log(4);
    }, 600);
}

function endAnimation() {
    $('form').width('0')
             .height('0')
             .css({'padding': '0'});
    console.log(4);
    setTimeout(()=>{
        $('form').css({'margin-top': '50vh'})
                 .height('50%');
        $('body').css({'justify-content': 'flex-start'});
        console.log(3);
    }, 200);
    setTimeout(()=>{
        $('body').css({'justify-content': 'flex-end'});
        $('form').css({'margin-top': '0px'})
                 .height(0);
        console.log(2);
    }, 400);
    setTimeout(()=>{
        $('form').css({'display': 'none'});
        console.log(1);
    }, 800);
}

function switchTo(action) {
    return function() {
        let items = $('body *'); // for the rare race condition.
        endAnimation();
        setTimeout(action, 800);
        setTimeout(items.remove, 1000);
    }
}

$(_=>{
    console.log(hasStarted_host);
    if (hasStarted_host) return;
    hasStarted_host = true;
    beginAnimation();
});