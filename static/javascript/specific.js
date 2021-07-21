let roomid, socket, button, textbox, form, chat, packets;

/*
 * 7/21/2021 00:06
 *
 *  HH      HH  II      CCCCCC  HH      HH  RRRRRRRR    II    SSSSSSSS
 *  HH      HH  II    CC        HH      HH  RR      RR  II  SS
 *  HH      HH  II    CC        HH      HH  RR      RR  II  SS
 *  HHHHHHHHHH  II    CC        HHHHHHHHHH  RRRRRRRR    II    SSSSSS
 *  HH      HH  II    CC        HH      HH  RR      RR  II          SS
 *  HH      HH  II    CC        HH      HH  RR      RR  II          SS
 *  HH      HH  II      CCCCCC  HH      HH  RR      RR  II  SSSSSSSS
 * 
 * chris is nice
 * so is perception
 * 
 * bad ascii art of chris:
 *          __
 *         "##|
 *        /^^^|
 *    _.~;\ I /
 *   "####;\~"
 * 
 * i think my iq is decreasing
 * 
 * 7/21/2021 00:13
 */

function createGUI(name, selection, optional) {
    $('.details form:last').before(
        $('<form/>').append(
            $('<fieldset/>').append(
                $('<legend/>').text('Condemn'),
                $('<select/>').append(
                    optional ? $('<option/>').prop('value', '').text('No selection') : undefined,
                    ...Object.entries(selection).map(([k, v])=>{
                        return $('<option/>').prop('value', v).text(k);
                    })
                ).change(function(){
                    socket.emit('gui', {[name]: $(this).find(':selected').prop('value')});
                })
            )
        ).prop('formname', name.toLowerCase().replaceAll(/[^a-z]/, ''))
    );
}

function freezeGUI(name) {
    $(`form[formname=${name.toLowerCase().replaceAll(/[^a-z]/, )}] > fieldset > select`).prop('disabled', true);
}

function deleteGUI(name) {
    $(`form[formname=${name.toLowerCase().replaceAll(/[^a-z]/, )}]`).remove();
}

function checkforsubmission() {
    let text = textbox.val();
    if (text)
        button.prop('disabled', false);
    else if (!text)
        button.prop('disabled', true);
}

function convertTimeToElement(msg) {
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
    form.submit(e=>{
        socket.emit('chat', textbox.val());
        textbox.val('');
        checkforsubmission();
        e.preventDefault();
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
    socket.on('gui', msg=>{
        $('<form/>').append(
            $('<fieldset/>').append(
                
            )
        )
    });
    socket.on('presence', msg=>{
        if (msg.player)
            $('input[type="submit"].playerup').prop('value', 'Player down');
        else
            $('input[type="submit"].playerup').prop('value', 'Player up');
        if (msg.host) {
            $('.gamelogic, .startgame').remove();
            $('.details form:last-child').append(
                $('<input>').prop('type', 'submit')
                            .prop('value', 'Edit Game logic')
                            .addClass('gamelogic')
                            .click(_=>
                                $('body').addClass('dark')
                                         .click(_=>{
                                            if (_.target==document.body)
                                                $('body').removeClass('dark')
                                                            .off('click')
                                                            .find('form.centered')
                                                            .remove();
                                        }).append(
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
                                                                        socket.emit('logic', $('form.centered input[type="text"]').prop('value'));
                                                                        $('body').click();
                                                                    })
                                                    )
                                                )
                                )
                            ),
                $('<input>').prop('type', 'submit')
                            .prop('value', 'Start game')
                            .addClass('startgame')
                            .click(_=>{
                                socket.emit('start', 'start');
                            })
            );
        }
    });
    socket.on('start', ()=>{}); // Future uses?
    socket.on('gui', msg=>createGUI(msg.name, msg.list, msg.optional));
    socket.on('guifreeze', name=>freezeGUI(name));
    socket.on('guidelete', name=>deleteGUI(name));
});