var hasStarted_index = false;
var hasStarted_login = false;
var hasStarted_play = false;
var hasStarted_host = false;

window.onpopstate = function(event) {
    switch (location.pathname) {
        case '/':
            return switchTo(navigateToIndex)();
        case '/play.html':
            return switchTo(navigateToPlay)();
        case '/host.html':
            return switchTo(navigateToHost)();
    }
}

function navigateToIndex() {
    $.get('/', function(data, status){
        newdocument = $(new DOMParser().parseFromString(data, 'text/html'));
        newdocument.find('body').find('aside').css({marginTop: 0}).find('img').css({transform: 'translateY(-100%)'},);
        newdocument.find('body').find('ul').hide();
        newdocument.find('body').removeAttr('nofooter').attr('footer', '');
                       $('body').removeAttr('footer').attr('nofooter', '');
        let currentstylesheet = $('link[rel="stylesheet"][href^="/"]');
        setTimeout(()=>{
            $('html').css({'background-color': $('body').css('background-color')});
            $('body').css({'display': 'none'});
            $('head').append($('<link/>').attr({rel: 'stylesheet',
                                                type: 'text/css',
                                                href: '/style.css'}));
            currentstylesheet.remove();
            history.pushState({}, newdocument.find('title').text(), '/');
            $('body').append(newdocument.find('body').children());
            hasStarted_index = false;
            $.ajax({
                method: 'GET',
                url: '/script.js',
                dataType: 'script'
            });
            footerVisible(true);
            imageVisible(true);
            listitemsVisible(true);
            hasStarted_login = false;
            hasStarted_play = false;
            hasStarted_host = false;
        }, 1000);
    });
}

function navigateToPlay() {
    $.get('/play.html', function(data, status){
        newdocument = $(new DOMParser().parseFromString(data, 'text/html'));
        setTimeout(()=>{
            let currentstylesheet = $('link[rel="stylesheet"][href^="/"]');
            $('html').css({'background-color': $('body').css('background-color')});
            $('body').css({'display': 'none'});
            $('head').append($('<link/>').attr({rel: 'stylesheet',
                                                type: 'text/css',
                                                href: '/play.css'}));
            currentstylesheet.remove();
            history.pushState({}, newdocument.find('title').text(), '/play.html');
            $('body').append(newdocument.find('body').children());
            hasStarted_play = false;
            $.ajax({
                method: 'GET',
                url: '/play.js',
                dataType: 'script'
            });
            hasStarted_login = false;
            hasStarted_index = false;
            hasStarted_host = false;
        }, 1000);
    });
}

function navigateToHost() {
    $.get('/host.html', function(data, status){
        newdocument = $(new DOMParser().parseFromString(data, 'text/html'));
        let currentstylesheet = $('link[rel="stylesheet"][href^="/"]');
        setTimeout(()=>{
            $('html').css({'background-color': $('body').css('background-color')});
            $('body').css({'display': 'none'});
            $('head').append($('<link/>').attr({rel: 'stylesheet',
                                                type: 'text/css',
                                                href: '/host.css'}));
            currentstylesheet.remove();
            history.pushState({}, newdocument.find('title').text(), '/host.html');
            $('body').append(newdocument.find('body').children());
            $.ajax({
                method: 'GET',
                url: '/host.js',
                dataType: 'script'
            });
            hasStarted_login = false;
            hasStarted_index = false;
            hasStarted_play = false;
        }, 1000);
    });
}

function navigateToLogin() {
    $.get('/login.html', function(data, status){
        newdocument = $(new DOMParser().parseFromString(data, 'text/html'));
        let currentstylesheet = $('link[rel="stylesheet"][href^="/"]');
        setTimeout(()=>{
            $('html').css({'background-color': $('body').css('background-color')});
            $('body').css({'display': 'none'});
            $('head').append($('<link/>').attr({rel: 'stylesheet',
                                                type: 'text/css',
                                                href: '/host.css'}));
            currentstylesheet.remove();
            history.pushState({}, newdocument.find('title').text(), '/login.html');
            $('body').append(newdocument.find('body').children());
            hasStarted_host = false;
            $.ajax({
                method: 'GET',
                url: '/login.js',
                dataType: 'script'
            });
            hasStarted_login = false;
            hasStarted_index = false;
            hasStarted_play = false;
        }, 1000);
    });
}