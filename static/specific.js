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
    socket.on('connect', ()=>{
        socket.emit('handshake', {'roomId': roomid, 'userId': 1337});
    });
    socket.on('chat', msg=>{
        let date = new Date(msg.timestamp()*1000);
        $('.chat').append(
            $('<message></message>').append(
                $('<time></time>').append(
                    `${a.getHours().toString().padStart(2, '0')}:`+
                    `${a.getMinutes().toString().padStart(2, '0')}:`+
                    `${a.getSeconds().toString().padStart(2, '0')}`
                ),
                $('<name></name>').append(msg.from),
                msg.message
            )
        );
    });
});

/*

*/