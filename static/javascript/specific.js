let roomid, socket, button, textbox, form, chat, packets, ishost;

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

function getNameFromId(id) {
    return new Promise(resolve =>
        $.post('/graphql', {query: '{ user(id:' + JSON.stringify(id) + ') { username } }'}, res=>{
            resolve(res.data.user[0].username);
        })
    );
}

const encodeGUIname = btoa;

// function encodeGUIname(name) {
//     return name.toLowerCase().replace(/[^a-z]/g, '');
// }

function createGUI(name, selection, optional) {
    $('.details form:last').before(
        $('<form/>').append(
            $('<fieldset/>').append(
                $('<legend/>').text(name + ':'),
                $('<select/>').append(
                    optional ? $('<option/>').prop('value', '').text('No selection') : undefined,
                    ...Object.entries(selection).map(([k, v])=>{
                        return $('<option/>').prop('value', v).text(k);
                    })
                ).change(function(){
                    socket.emit('gui', {[name]: $(this).find(':selected').prop('value')});
                })
            )
        ).prop('formname', encodeGUIname(name))
    );
}

function freezeGUI(name) {
    $('form[formname="' + encodeGUIname(name) + '"] > fieldset > select').prop('disabled', true);
}

function deleteGUI(name) {
    $('form[formname="' + encodeGUIname(name) +'"]').remove();
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
        date.getHours().toString().padStart(2, '0')+':'+
        date.getMinutes().toString().padStart(2, '0')+':'+
        date.getSeconds().toString().padStart(2, '0')
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

async function createChatFrom(msg) {
    let from = await getNameFromId(msg.fromid);
    return $('<message></message>').append(
        convertTimeToElement(msg),
        $('<name></name>').append(from),
        msg.message
    );
}

function createSystemFrom(msg) {
    return $('<system></system>').append(
        convertTimeToElement(msg),
        msg.message
    );
}

async function onchat(msg) {
    addToChat(await createChatFrom(msg));
    packets.push(['chat', msg]);
}

async function onsystem(msg) {
    addToChat(await createSystemFrom(msg));
    packets.push(['system', msg]);
}

function createPopup(name, appendables) {
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
                            $('<legend>').text(name),
                            ...appendables
                        )
                    )
    )
}

function onphase(name) {
    $('h1').text(name);
    chat.children().remove();
    packets.push(['phase', name]);
}

function cancelform (event) {
    event.preventDefault();
    return false;
}

function autosend(event) {
    if (event.which==13)
        button.click();
}

function chatout(event) {
    socket.emit('chat', textbox.val());
    textbox.val('');
    checkforsubmission();
    event.preventDefault();
    return false;
}

function updatepresence(msg) {
    if (msg.player)
        $('input[type="submit"].playerup').prop('value', 'Player down');
    else
        $('input[type="submit"].playerup').prop('value', 'Player up');
    ishost = msg.host;
    if (ishost) {
        $('.gamelogic, .startgame').remove();
        $('.details form:last').append(
            $('<input>').prop('type', 'submit')
                        .prop('value', 'Edit Game logic')
                        .addClass('gamelogic')
                        .click(_=>
                            createPopup('Edit Game logic', [
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
                            ])
                        ),
            $('<input>').prop({
                            type: 'submit',
                            value:'Start game'
                        }).addClass('startgame')
                        .click(_=>{
                            socket.emit('start', 'start');
                        })
        );
    }
}

async function onhandshake(events) {
    let currentphaseind = events.map(e=>e[0]=='phase').lastIndexOf(true);
    let currentevents = events.slice(0, currentphaseind);
    if (currentphaseind != -1) {
        let currentphase = events[currentphaseind][1];
        onphase(currentphase);
        $('.details form').remove();
    }
    for (let [type, msg] of currentevents)
        switch (type) {
            case 'chat':
                await onchat(msg);
                break;
            case 'system':
                await onsystem(msg);
                break;
        }
}

function main() {
    roomid = location.pathname.split('/')[2];
    form = $('.input');
    button = $('.input > input[type=submit]');
    textbox = $('.input > input[type=text]');
    textbox.on('input', checkforsubmission).keypress(autosend);
    form.submit(chatout);
    chat = $('.chat');
    $('.details form').submit(cancelform).find('input[type="submit"].playerup').click(_=>
        socket.emit('presence', {'player': true, 'host': ishost})
    );
    socket = io();
    socket.on('connect', ()=>
        socket.emit('handshake', {'roomId': roomid, 'usertoken': $('meta[name="session"]').attr('content')})
    );
    socket.on('handshake', onhandshake); 
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
    socket.on('presence', updatepresence);
    // socket.on('start', ()=>{}); // Future uses?
    socket.on('gui', msg=>createGUI(msg.name, msg.list, msg.optional));
    socket.on('guifreeze', name=>freezeGUI(name));
    socket.on('guidelete', name=>deleteGUI(name));
}

$(main);