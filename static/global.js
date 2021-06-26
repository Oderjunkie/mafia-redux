function navigateToIndex() {
    $.get('/', function(data, status){
        newdocument = $(new DOMParser().parseFromString(data, 'text/html'));
        newdocument.find('body').find('aside').css({marginTop: 0}).find('img').css({transform: 'translateY(-100%)'},);
        newdocument.find('body').find('ul').hide();
        newdocument.find('body').removeAttr('nofooter').attr('footer', '');
                       $('body').removeAttr('footer').attr('nofooter', '');
        let currentstylesheet = $('link[rel="stylesheet"][href^="/"]');
        $('head').append($('<link/>').attr({rel: 'stylesheet',
                                            type: 'text/css',
                                            href: '/style.css'}));
        currentstylesheet.remove();
        setTimeout(()=>{
            $('body').append(newdocument.find('body').children());
            $.get('/script.js', (d,s)=>eval(d));
            footerVisible(true);
            imageVisible(true);
            listitemsVisible(true);
        }, 1000);
    });
}

function navigateToPlay() {
    $.get('/play.html', function(data, status){
        newdocument = $(new DOMParser().parseFromString(data, 'text/html'));
        let currentstylesheet = $('link[rel="stylesheet"][href^="/"]');
        $('head').append($('<link/>').attr({rel: 'stylesheet',
                                            type: 'text/css',
                                            href: '/play.css'}));
        currentstylesheet.remove();
        setTimeout(()=>{
            $('body').append(newdocument.find('body').children());
            $.get('/play.js', (d,s)=>eval(d));
        }, 1000);
    });
}

function navigateToHost() {
    $.get('/host.html', function(data, status){
        newdocument = $(new DOMParser().parseFromString(data, 'text/html'));
        let currentstylesheet = $('link[rel="stylesheet"][href^="/"]');
        $('head').append($('<link/>').attr({rel: 'stylesheet',
                                            type: 'text/css',
                                            href: '/host.css'}));
        currentstylesheet.remove();
        setTimeout(()=>{
            $('body').append(newdocument.find('body').children());
            $.get('/host.js', (d,s)=>eval(d));
        }, 1000);
    });
}