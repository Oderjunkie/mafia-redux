let roomid, socket, button, textbox, form;

const checkforsubmission = e=>{
    let disabled = button.attr('disabled');
    let text = textbox.val();
    if (text && disabled)
        button.removeAttr('disabled');
    else if (!text && !disabled)
        button.attr('disabled', '');
}

$(_=>{
    roomid = location.pathname.split('/')[2];
    form = $('.input');
    button = $('.input > input[type=submit]');
    textbox = $('.input > input[type=text]');
    textbox.on('input', checkforsubmission).keypress(e=>{
        if (e.which==13)
            button.click();
    });
    form.submit(()=>{
        socket.emit('chat', textbox.val());
        textbox.val('');
        checkforsubmission();
        return false;
    });
    socket = io();
    socket.on('connect',()=>{});
});