$(()=>{

$.ajax({
    url: '/api/rooms',
    dataType: 'json'
}),done($data=>{
    $('body').append(
        ...$data.map(e=>
            $('<form></form>').prop('action', `/game/${e.roomid}`)
                              .append(
                $('<name></name>').append(
                    e.name
                ),
                $('<input></input>').prop('value', 'Join')
                                    .prop('type', 'submit')
            )
        )
    );
});

});