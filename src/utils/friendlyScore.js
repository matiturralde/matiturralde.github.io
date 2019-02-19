export const friendlyScore = () => {
    (function (d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0],
            appID = d.getElementById("fs-widget-btn").getAttribute('data-fs-app-id');
        if (d.getElementById(id)) return;
        js = d.createElement(s);
        js.id = id;
        js.src = "https://cdn.friendlyscore.com/widget_v2.min.js?" + appID;
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'fs-widget'))
}