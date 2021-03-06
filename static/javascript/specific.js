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

/**
 * Converts a user id into a username.
 * 
 * @param {string} id - The userid.
 * @returns {Promise<string>}
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

/**
 * Creates a GUI box based on a SocketIO event.
 * 
 * @param {Object} msg - The event.
 * @param {string} msg.name - The name of the GUI box.
 * @param {Object<string, *>} msg.list - An object containing the names and values of all options.
 * @param {string} msg.optional - Whether or not the GUI box has a "No selection" option.
 */

function createGUI({name, list: selection, optional}) {
    $('.details form:last').before(
        $('<form/>').append(
            $('<fieldset/>').append(
                $('<legend/>').text(name + ':'),
                $('<select/>').append(
                    optional ? $('<option/>').prop('value', '').text(optional) : undefined,
                    ...Object.entries(selection).map(([k, v])=>{
                        return $('<option/>').prop('value', v).text(k);
                    })
                ).change(function(){
                    socket.emit('gui', {[name]: $(this).find(':selected').prop('value')});
                })
            )
        ).attr('formname', encodeGUIname(name))
    );
}

/**
 * Freezes a specific GUI box from a SocketIO event.
 * 
 * @param {string} name - Name of the GUI box.
 */

function freezeGUI(name) {
    $('form[formname="' + encodeGUIname(name) + '"] > fieldset > select').prop('disabled', true);
}

/**
 * Deletes a specific GUI box from a SocketIO event.
 * 
 * @param {string} name - Name of the GUI box.
 */

function deleteGUI(name) {
    $('form[formname="' + encodeGUIname(name) +'"]').remove();
}

/**
 * Checks if the chat textbox has text in it or not.
 */

function checkforsubmission() {
    let text = textbox.val();
    if (text)
        button.prop('disabled', false);
    else if (!text)
        button.prop('disabled', true);
}

/**
 * Gets the time of a SocketIO event.
 * 
 * @param {Object} msg - The SocketIO event.
 * @param {string} msg.timestamp - The Unix Timestamp of the event.
 * @returns {jQuery}
 */

function convertTimeToElement({timestamp}) {
    let date = new Date(timestamp*1000);
    return $('<time></time>').append(
        date.getHours().toString().padStart(2, '0')+':'+
        date.getMinutes().toString().padStart(2, '0')+':'+
        date.getSeconds().toString().padStart(2, '0')
    );
}

/**
 * Appends an element to chat, and appropriately scrolls
 * the chat to the bottom.
 * 
 * @param {jQuery} el - The element to append.
 */

function addToChat(el) {
    let chatobj = chat[0];
    let max = chatobj.scrollHeight - chatobj.offsetHeight
    let old = chat.append(el).scrollTop();
    if (old == max) {
        let newmax = chatobj.scrollHeight - chatobj.offsetHeight
        chat.scrollTop(newmax);
    }
}

/**
 * Logs a SocketIO "chat" event.
 * 
 * @async
 * @param {Object} msg - The SocketIO event.
 * @param {string} msg.fromid - The userid of the author.
 * @param {string} msg.message - The contents of the message.
 * @returns {jQuery}
 */

async function createChatFrom(msg) {
    let from = await getNameFromId(msg.fromid);
    return $('<message></message>').append(
        convertTimeToElement(msg),
        $('<name></name>').append(from),
        msg.message
    );
}

/**
 * Logs a SocketIO "system" event.
 * 
 * @param {Object} msg - The SocketIO event.
 * @param {string} msg.message - The contents of the message.
 * @returns {jQuery}
 */

function createSystemFrom(msg) {
    return $('<system></system>').append(
        convertTimeToElement(msg),
        msg.message
    );
}

/**
 * Wrapper around `createChatFrom`, to add it
 * to chat and append it to the packet log.
 * 
 * @async
 * @param {Object} msg
 * @param {string} msg.fromid - The userid of the author.
 * @param {string} msg.message - The contents of the message.
 */

async function onchat(msg) {
    addToChat(await createChatFrom(msg));
    packets.push(['chat', msg]);
}

/**
 * Wrapper around `createSystemFrom`, to add it
 * to chat and append it to the packet log.
 * 
 * @async
 * @param {Object} msg
 * @param {string} msg.fromid - The userid of the author.
 * @param {string} msg.message - The contents of the message.
 */

async function onsystem(msg) {
    addToChat(await createSystemFrom(msg));
    packets.push(['system', msg]);
}

/**
 * Creates a pop-up box.
 * 
 * @param {string} name - The legend of the form.
 * @param {jQuery[]} appendables - The contents of the form.
 */

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
    );
}

/**
 * Changes the current phase.
 * 
 * @param {string} name - The name of the new phase.
 */

function onphase(name) {
    $('h1').text(name);
    chat.children().remove();
    packets.push(['phase', name]);
}

/**
 * Cancels form submissions.
 * 
 * @param {*} event - The event caused by the submission.
 * @returns {boolean} - `false`, to disable the form.
 */

function cancelform(event) {
    event.preventDefault();
    return false;
}

/**
 * Automatically sends messages when pressing enter.
 * 
 * @param {*} event - The event caused by the `onmousedown` hook.
 */

function autosend(event) {
    if (event.which==13)
        button.click();
}

/**
 * Sends a message.
 * 
 * @param {*} event - The event caused by the `onsubmit` hook.
 * @returns {boolean} - `false`, to disable the form.
 */

function chatout(event) {
    socket.emit('chat', textbox.val());
    textbox.val('');
    checkforsubmission();
    event.preventDefault();
    return false;
}

/**
 * Displays an error message in the form of a
 * pop-up box [using `createPopup`]
 * 
 * @param {string} msg - The error message to display.
 */

function handleError(msg) {
    createPopup('Error', [
        $('<p>').text(msg)
    ]);
}

/**
 * Updates the client's GUI to reflect their presence within the room.
 * 
 * @param {Object} msg - The SocketIO event.
 * @param {boolean} msg.player - Whether or not the client is playered up.
 * @param {boolean} msg.host - Whether or not the client is hosting the room.
 */

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

/**
 * Handles the client's side of the handshake process.
 * 
 * @param {*} msg - The events.
 */

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

/**
 * The main function.
 * Not very documentable, as it shouldn't be called.
 */

function main() {
    roomid = location.pathname.split('/')[2];
    packets = [];
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
    socket.on('gui', createGUI);
    socket.on('guifreeze', freezeGUI);
    socket.on('guidelete', deleteGUI);
    socket.on('error', handleError);
}

$(main);