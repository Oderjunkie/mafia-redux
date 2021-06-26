function footerVisible(hasfooter, callback) {
    if (hasfooter)
        return $('body').removeAttr('nofooter').attr('footer','');
    else
        return $('body').removeAttr('footer').attr('nofooter','');
}

function imageVisible(hasimg, callback) {
    if (hasimg)
        return $('aside').css({marginTop: 30}).find('img').css({transform: 'translateY(0%)'}, callback).parent(callback);
    else
        return $('aside').css({marginTop: 0}).find('img').css({transform: 'translateY(-100%)'}, callback).parent(callback);
}

function listitemsVisible(haslist, callback) {
    if (haslist)
        return $('ul').show(1000, callback);
    else
        return $('ul').hide(1000, callback);
}

$(()=>{

$('li.play').click(_=>{
    footerVisible(false);
    imageVisible(false);
    listitemsVisible(false);
    setTimeout(()=>$('footer, aside, ul').remove(), 1000);
});



});