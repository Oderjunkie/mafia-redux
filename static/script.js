let hasStarted_index = false;

function footerVisible(hasfooter) {
    if (hasfooter)
        return $('body').removeAttr('nofooter').attr('footer', '');
    else
        return $('body').removeAttr('footer').attr('nofooter', '');
}

function imageVisible(hasimg) {
    if (hasimg)
        return $('aside').css({marginTop: 30}).find('img').css({transform: 'translateY(0%)'}).parent();
    else
        return $('aside').css({marginTop: 0}).find('img').css({transform: 'translateY(-100%)'}).parent();
}

function listitemsVisible(haslist) {
    if (haslist)
        return $('ul').show(1000);
    else
        return $('ul').hide(1000);
}

function clickHandler(action) {
    return function() {
        footerVisible(false);
        imageVisible(false);
        listitemsVisible(false);
        let items = $('body *'); // for the rare race condition.
        action();
        setTimeout(()=>items.remove(), 1000);
    }
}

$(_=>{
    if (hasStarted_index) return else hasStarted_index = true;
    $('li.play').click(clickHandler(navigateToPlay));
    $('li.host').click(clickHandler(navigateToHost));
    $('li.about').css({opacity: 0.2}); // plz don click
});