chrome.tabs.onUpdated.addListener(function (id,change,tab) {

	// after page loaded.
    if (tab.status == 'complete') { chrome.tabs.sendRequest(id, {action : 'getImagePath'}, function(imagePath) {}); }

});