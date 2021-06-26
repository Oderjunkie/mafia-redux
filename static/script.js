function footerVisible(hasfooter) {
    if (hasfooter)
        $('body').removeAttr('nofooter').attr('footer','');
    else
        $('body').removeAttr('footer').attr('nofooter','');
}

function imageVisible(hasimg) {
    if (hasimg)
        $('aside').css({marginTop: 30}).find('img').css({transform: 'translateY(0%)'});
    else
        $('aside').css({marginTop: 0}).find('img').css({transform: 'translateY(-100%)'});
}

function listitemsVisible(haslist) {
    if (haslist)
        $('ul').show();
    else
        $('ul').hide();
}

$(()=>{

$('li.play').click(_=>{
    footerVisible(false);
    imageVisible(false);
    listitemsVisible(false);
});



});