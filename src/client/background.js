console.log("background is running");

function debug() {
    console.log("ok..");
}

chrome.tabs.onUpdated.addListener(function(tabId, info, tab){
    if (info.status == 'complete') {
        let msg = {
            txt: "fullyLoaded"
        }
        chrome.tabs.sendMessage(tab.id, msg);
    }
});


function sendRequest(tagImg, backImg) {
    let currentTab;
    let httpRequest = new XMLHttpRequest();

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        console.log(tabs[0]);
        currentTab = tabs[0];
    });

    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState == XMLHttpRequest.DONE && httpRequest.status == 200 ) {
            document.getElementById("text").innerHTML = httpRequest.responseText;
        }
    };

    // POST 방식의 요청은 데이터를 Http 헤더에 포함시켜 전송함.
    httpRequest.open("POST", "http://202.31.202.253:5000/", true);
    httpRequest.onreadystatechange = function() {
        if(httpRequest.readyState == 4) {
            switch (httpRequest.readyState) {       //readyState가 아닌 status보고 정해라
                case XMLHttpRequest.UNSET:
                    break;
                case XMLHttpRequest.OPENED:
                    break;
                case XMLHttpRequest.HEADERS_RECIEVED:
                    break;
                case XMLHttpRequest.LOADING:
                    break;      
                case XMLHttpRequest.DONE:
                    console.log(httpRequest.responseText);
                    console.log("receive response");

                    let msg = {
                        txt: "recoveryImg",
                        response: httpRequest.responseText
                    };

                    chrome.tabs.sendMessage(currentTab.id, msg, function(response) {
                        console.log("send to front");
                    });

                    break;
            }
        }
    }
    httpRequest.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    let packet = {"imgs": {tagImg, backImg}};

    httpRequest.send(JSON.stringify(packet));
}

chrome.browserAction.onClicked.addListener(buttonClicked);

function buttonClicked(tab) {
    let msg = {
        txt: "allRecovery"
    }

    chrome.tabs.sendMessage(tab.id, msg);
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
    console.log("got message");
    console.log(request);
    if(request.todo == "sendImgSrc") {
        console.log("send img src");
        sendRequest(request.tagImgs, request.backImgs);
    }
});