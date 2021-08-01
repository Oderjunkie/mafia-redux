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
    setTimeout(()=>{
        $('form').width('')
                 .height('');
        console.log('!');
    }, 800);
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
    return ()=>{
        let items = $('body *'); // for the rare race condition.
        endAnimation();
        setTimeout(action, 800);
        setTimeout(items.remove, 1000);
    }
}

function getDataOf(form) {
    return form.find('input:not([type="submit"])').map(function(){
        let current = $(this);
        return `${encodeURIComponent(current.prop('name'))}=${encodeURIComponent(current.val())}`;
    }).toArray().join('&');
}

function onSubmitBetter_form(event) {
    event.preventDefault();
    return false;
}

function onSubmitBetter_button() {
    let button = $(this);
    let form = button.closest('form');
    let data = getDataOf(form);
    let action = button.attr('formaction') ?? form.prop('action');
    let method = button.attr('formmethod') ?? form.prop('method');
    let error = form.find('.error');
    error.hide(500).text();
    return $.ajax({
        cache: false,
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
        data: data,
        dataType: 'text',
        method: method,
        url: action
    }).done($data=>{
        window.location.href = $data;
    }).fail(({responseText: $data})=>{
        error.text($data).show(500);
    });
}

$(_=>{
    console.log(hasStarted_login);
    if (hasStarted_login) return;
    hasStarted_host = true;
    $('form').submit(onSubmitBetter_form)
             .find('input[type="submit"]')
             .click(onSubmitBetter_button);
    beginAnimation();
});