console.log("kittens of the world, unite as one!");

let filenames = [
    "kittens/kitten1.png",
    "kittens/kitten2.png",
    "kittens/kitten3.png",
]

var imgs = document.getElementsByTagName('img');
var backImgs = document.querySelectorAll('[style^=background-image]');

var imgTagArray;
var backImgTagArray;

function saveImg() {
    console.log("save img");

    let link = document.location.href;

    let imgDataLength;
    let backImgDataLength;

    imgDataLength = imgs.length;
    imgTagArray = new Array(imgDataLength);

    backImgDataLength = backImgs.length;
    backImgTagArray = new Array(backImgDataLength);

    backImgTagArrayForReq = new Array(backImgDataLength);

    for (let i = 0 ; i < imgDataLength ; i++) {
        imgTagArray[i] = imgs[i].src;
    }

    for (let i = 0 ; i < backImgDataLength ; i++) {
        backImgTagArray[i] = backImgs[i].style.backgroundImage;
        if(backImgTagArray[i][0] == 'u' || backImgTagArray[i][0] == 'U') {
            backImgTagArrayForReq[i] = backImgTagArray[i].split('"')[1];
        }

        if(backImgTagArrayForReq[i][0] != 'h') {
            backImgTagArrayForReq[i] = link + backImgTagArrayForReq[i];
        }
    }

    chrome.runtime.sendMessage({todo: "sendImgSrc", tagImgs: imgTagArray, backImgs: backImgTagArrayForReq});
}

//recovery
chrome.runtime.onMessage.addListener(gotMessage);

function allRecovery() {
    console.log("all recovery started");

    for (i = 0; i < imgs.length; i++) {
        recoveryImg(0, i);
    }
    for (i = 0; i < backImgs.length; i++) {
        recoveryImg(1, i);
    }
}

function recovery(response) {
    console.log("recovery started");
    console.log(response);

    let result = JSON.parse(response);
    console.log(result);

    let frontResult = result.imgs.tagImg;
    let backResult = result.imgs.backImg;

    console.log(frontResult[0]);
    if(frontResult[0] != "NoImage") {
        for (i = 0; i < frontResult.length; i++) {
            console.log(frontResult[i]);
            if(frontResult[i] == "normal") {
                recoveryImg(0, i);
            }
            else {
                coverImg(0, i);
            }
        }
    }

    console.log(backResult[0]);
    if(backResult[0] != "NoImage") {
        for (i = 0; i < backResult.length; i++) {
            console.log(backResult[i]);
            if(backResult[i] == "normal") {
                recoveryImg(1, i);
            }
            else {
                coverImg(1, i);
            }
        }
    }
}

function recoveryImg(isBack, imgNumber) {
    console.log("recovery img: " + imgNumber);

    if (isBack == 0){
        console.log("img is front: " + imgNumber);
        imgs[imgNumber].style.setProperty("visibility", "visible");
    }
    else {
        console.log("img is back: " + imgNumber);
        backImgs[imgNumber].style.setProperty("visibility", "visible");
    }
}

function coverImg(isBack, imgNumber) {
    console.log("cover img: " + imgNumber);

    let r = Math.floor(Math.random() * filenames.length);
    let file =  filenames[r];
    let url = chrome.extension.getURL(file);

    if (isBack == 0){
        console.log("img is front: " + imgNumber);
        imgs[imgNumber].style.setProperty("visibility", "visible");
        imgs[imgNumber].style.setProperty("content", "url("+url+")");
        imgs[imgNumber].onclick = function() {
            imgs[imgNumber].style.setProperty("content", "url("+imgTagArray[imgNumber]+")");
        }
    }
    else {
        console.log("img is back: " + imgNumber);
        backImgs[imgNumber].style.setProperty("visibility", "visible");
        backImgs[imgNumber].style.setProperty("background-image", url);
        backImgs[imgNumber].onclick = function() {
            backImgs[imgNumber].style.setProperty("background-image", backImgTagArray[imgNumber]);
        }
    }
}

function gotMessage(request, sender, sendResponse) {
    console.log("got message");
    if (request.txt == "recoveryImg") {
        console.log("message is recovery");
        sendResponse("i received");
        recovery(request.response);
    }
    else if (request.txt == "fullyLoaded") {
        console.log("message is fully loaded");
        saveImg();
    }
    else if (request.txt == "allRecovery") {
        console.log("message is fully loaded");
        allRecovery();
    }
}