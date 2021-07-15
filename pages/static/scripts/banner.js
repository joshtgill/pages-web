var lastScroll = 0;

var content = document.getElementById('content');
var banner = document.getElementById('banner')

function scrollFunction() {
    if (((window.innerWidth > 0) ? window.innerWidth : screen.width) > 580) {
        return;
    }

    if (content.scrollTop == 0) {
        banner.className = 'banner';
        if (document.getElementsByClassName('message-container')[0]) {
            document.getElementsByClassName('message-container')[0].style.display = 'flex';
        }
    }
    else {
        banner.className = 'banner-condensed';
        if (document.getElementsByClassName('message-container')[0]) {
            document.getElementsByClassName('message-container')[0].style.display = 'none';
        }
    }
}

content.onscroll = scrollFunction;
