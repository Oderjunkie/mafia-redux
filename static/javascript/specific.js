let roomid, socket, button, textbox, form, chat, packets;

function checkforsubmission() {
    let text = textbox.val();
    if (text)
        button.prop('disabled', false);
    else if (!text)
        button.prop('disabled', true);
}

function convertTimeToElement() {
    let date = new Date(msg.timestamp*1000);
    $('<time></time>').append(
        `${date.getHours().toString().padStart(2, '0')}:`+
        `${date.getMinutes().toString().padStart(2, '0')}:`+
        `${date.getSeconds().toString().padStart(2, '0')}`
    );
}

function addToChat(el) {
    let chatobj = chat[0];
    let max = chatobj.scrollHeight - chatobj.offsetHeight
    let old = chat.append(el).scrollTop();
    if (old == max) {
        let newmax = chatobj.scrollHeight - chatobj.offsetHeight
        chat.scrollTop(newmax);
    }
}

function createChatFrom(msg) {
    return $('<message></message>').append(
        convertTimeToElement(msg),
        $('<name></name>').append(msg.from),
        msg.message
    );
}

function createSystemFrom(msg) {
    return $('<system></system>').append(
        convertTimeToElement(msg),
        msg.message
    );
}

function onchat(msg) {
    addToChat(createChatFrom(msg));
    packets.push(['chat', msg]);
}

function onsystem(msg) {
    addToChat(createSystemFrom(msg));
    packets.push(['system', msg]);
}

function onphase(msg) {
    $('h1').text(msg.name);
    chat.children().remove();
    packets.push(['phase', msg]);
}

function cancelform (event) {
    event.preventDefault();
    return false;
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
    chat = $('.chat');
    $('.details form').submit(
        cancelform
    ).find('input[type="submit"].playerup').click(_=>{
        socket.emit('presence', {'player': true});
    });
    socket = io();
    socket.on('connect', ()=>{
        socket.emit('handshake', {'roomId': roomid, 'usertoken': $('meta[name="session"]').attr('content')});
    });
    socket.on('handshake', events=>{
        packets = events;
        let currentphaseind = events.map(e=>e[0]=='phase').lastIndexOf(true);
        let currentevents = events.slice(0, currentphaseind);
        if (currentphaseind != -1) {
            let currentphase = events[currentphaseind];
            onphase({'name': currentphase});
            $('.details form').remove();
        }
        for (let [type, msg] of currentevents) {
            switch (type) {
                case 'chat':
                    onchat(msg);
                    break;
                case 'system':
                    onsystem(msg);
                    break;
            }
        }
    }); 
    socket.on('chat', onchat);
    socket.on('system', onsystem);
    socket.on('phase', onphase);
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
    socket.on('presence', msg=>{
        if (msg.player)
            $('input[type="submit"].playerup').prop('value', 'Player down');
        else
            $('input[type="submit"].playerup').prop('value', 'Player up');
        if (msg.host)
            $('.details form').append(
                $('<input>').prop('type', 'submit')
                            .prop('value', 'Edit Game logic')
                            .addClass('gamelogic')
                            .click(_=>{
                                $('body').addClass('dark')
                                         .click(_=>{
                                            if (_.target==document.body)
                                                $('body').removeClass('dark')
                                                            .off('click')
                                                            .find('form.centered')
                                                            .remove();
                                        });
                                $('<form>').submit(cancelform)
                                            .addClass('centered')
                                            .append(
                                                $('<fieldset>').append(
                                                    $('<legend>').text('Edit Game logic'),
                                                    $('<label>').prop('for', 'gamelogiclink')
                                                                .text('Pastebin Link:'),
                                                    $('<br>'),
                                                    $('<input>').prop({
                                                                    type: 'text',
                                                                    id: 'gamelogiclink'
                                                                }),
                                                    $('<br>'),
                                                    $('<input>').prop({
                                                                    type: 'submit',
                                                                    value: 'Change logic'
                                                                }).click(_=>{
                                                                    socket.emit('logic', {
                                                                        'link': $('form.centered input[type="text"]').prop('value')
                                                                    });
                                                                    $('body').click();
                                                                })
                                                )
                                            )
                            }),
                $('<input>').prop('type', 'submit')
                            .prop('value', 'Start game')
                            .addClass('startgame')
                            .click(_=>{
                                socket.emit('start');
                            })
            );
    });
    socket.on('start', ()=>{}); // Future uses?
});