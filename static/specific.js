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
        socket.emit('handshake', {'roomId': roomid, 'usertoken': $('meta[name="session"]').attr('content')});
    });
    socket.on('chat', msg=>{
        let date = new Date(msg.timestamp*1000);
        $('.chat').append(
            $('<message></message>').append(
                $('<time></time>').append(
                    `${date.getHours().toString().padStart(2, '0')}:`+
                    `${date.getMinutes().toString().padStart(2, '0')}:`+
                    `${date.getSeconds().toString().padStart(2, '0')}`
                ),
                $('<name></name>').append(msg.from),
                msg.message
            )
        );
    });
    socket.on('system', msg=>{
        let date = new Date(msg.timestamp*1000);
        $('.chat').append(
            $('<system></system>').append(
                $('<time></time>').append(
                    `${date.getHours().toString().padStart(2, '0')}:`+
                    `${date.getMinutes().toString().padStart(2, '0')}:`+
                    `${date.getSeconds().toString().padStart(2, '0')}`
                ),
                msg.message
            )
        );
    });
    socket.on('userJoin', msg=>{
        let date = new Date(msg.timestamp*1000);
        $('.chat').append(
            $('<internal></internal>').append(
                $('<time></time>').append(
                    `${date.getHours().toString().padStart(2, '0')}:`+
                    `${date.getMinutes().toString().padStart(2, '0')}:`+
                    `${date.getSeconds().toString().padStart(2, '0')}`
                ),
                $('<name></name>').append(msg.name),
                'has joined.'
            )
        );
    });
    socket.on('userExit', msg=>{
        let date = new Date(msg.timestamp*1000);
        $('.chat').append(
            $('<internal></internal>').append(
                $('<time></time>').append(
                    `${date.getHours().toString().padStart(2, '0')}:`+
                    `${date.getMinutes().toString().padStart(2, '0')}:`+
                    `${date.getSeconds().toString().padStart(2, '0')}`
                ),
                $('<name></name>').append(msg.name),
                'has exited.'
            )
        );
    });
});

/*

*/