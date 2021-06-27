let roomid, socket, button, textbox;

$(_=>{
    roomid = location.pathname.split('/')[2];
    button = $('.input > input[type=submit]');
    textbox = $('.input > input[type=text]');
    textbox.on('input', e=>{
        let disabled = button.attr('disabled');
        if (e.currentTarget.value && disabled)
            button.removeAttr('disabled');
        else if (!e.currentTarget.value && !disabled)
            button.attr('disabled', '');
    }).keypress(e=>{
        if (e.which==13)
            button.click();
    });
    socket = io();
    socket.on('connect', function() {
        socket.emit('chat', 'Hello!');
    });
});