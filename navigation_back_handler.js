window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        goBack: function(nClicks) {
            if (nClicks) {
                window.history.back();
            }
            return null;
        }
    }
});
