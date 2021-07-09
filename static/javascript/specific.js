let roomid, socket, button, textbox, form, chat;

const checkforsubmission = e=>{
    let disabled = button.attr('disabled');
    let text = textbox.val();
    if (text && disabled)
        button.removeAttr('disabled');
    else if (!text && !disabled)
        button.attr('disabled', '');
};

const convertTimeToElement = msg=>{
    let date = new Date(msg.timestamp*1000);
    $('<time></time>').append(
        `${date.getHours().toString().padStart(2, '0')}:`+
        `${date.getMinutes().toString().padStart(2, '0')}:`+
        `${date.getSeconds().toString().padStart(2, '0')}`
    );
};

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
    let chat = $('.chat');
    socket = io();
    socket.on('connect', ()=>{
        socket.emit('handshake', {'roomId': roomid, 'usertoken': $('meta[name="session"]').attr('content')});
    });
    const addToChat = el=>{
        let chatobj = chat[0];
        let max = chatobj.scrollHeight - chatobj.offsetHeight
        let old = chat.append(el).scrollTop();
        if (old == max) {
            let newmax = chatobj.scrollHeight - chatobj.offsetHeight
            chat.scrollTop(newmax);
        }
    }
    const onchat = msg=>{
        addToChat(
            $('<message></message>').append(
                convertTimeToElement(msg),
                $('<name></name>').append(msg.from),
                msg.message
            )
        );
    }
    const onsystem = msg=>{
        addToChat(
            $('<system></system>').append(
                convertTimeToElement(msg),
                msg.message
            )
        );
    }
    socket.on('chat', onchat);
    socket.on('system', onsystem);
    socket.on('userJoin', msg=>{
        addToChat(
            $('<internal></internal>').append(
                convertTimeToElement(msg),
                $('<name></name>').append(msg.name),
                'has joined.'
            )
        );
    });
    socket.on('userExit', msg=>{
        addToChat(
            $('<internal></internal>').append(
                convertTimeToElement(msg),
                $('<name></name>').append(msg.name),
                'has exited.'
            )
        );
    });
});