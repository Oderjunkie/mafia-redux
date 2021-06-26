function footer(hasfooter) {
    if (hasfooter)
        $('body').removeAttr('footer').attr('nofooter','');
    else
        $('body').removeAttr('nofooter').attr('footer','');
}