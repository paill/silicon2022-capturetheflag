var express = require('express');
var sessions = require('express-session');
var app = express();
var path = require('path');
var fs = require('fs');


var FLAG = process.env.FLAG;
var SECRET_PATH = "/" + process.env.SECRET_PATH;
var HOSTING_PATH = process.env.HOSTING_PATH;

var myLogger = function (req, res, next) {
    console.log('GET ' + req.path);
    next();
}

app.use(myLogger);
app.use(express.static(HOSTING_PATH + "/static/"));

app.use(sessions({
    secret: 'sNKXtE2A5Jmt#MK+!=UHW!N@zU+AZAd7aH!tcF_J',
    resave: false,
    saveUninitialized: true
}));

// viewed at http://localhost:8080
app.get('/', function (req, res, next) {
    if (!req.session.initialised) {
        req.session.initialised = true;
        req.session.x = 0;
    }

    if (req.session.x >= FLAG.length) {
        req.session.x = 0;
    }

    res.sendFile(path.join(__dirname + '/index.htm'));
});

app.get('/map', function(req, res, next) {
    if (!req.session.initialised) {
        req.session.initialised = true;
        req.session.x = 0;
    }

    var flagXPos, flagYPos;

    var flagCharacterCodeString = SECRET_PATH.charCodeAt(req.session.x).toString();
    
    if (flagCharacterCodeString.length == 3) {
        flagXPos = Number(flagCharacterCodeString.substring(0,2));
        flagYPos = Number(flagCharacterCodeString.substring(2,3));
    } else {
        flagXPos = Number(flagCharacterCodeString.substring(0,1));
        flagYPos = Number(flagCharacterCodeString.substring(1,2));
    }
    
    var mapData = JSON.parse(fs.readFileSync(HOSTING_PATH + '/static/data/map.json', 'utf8'));
    mapData.posY[flagYPos - 1].posX[flagXPos - 1].type = "xwall";
    req.session.x += 1;

    if (req.session.x >= SECRET_PATH.length) {
        req.session.x = 0;
    }

    res.json(mapData);
});

app.get(SECRET_PATH, function(req, res, next) {
    data = {
        "messages":[
            {
                "from": "bowser",
                "to": "koopa",
                "message": "Have you aquired Princess Toadstool yet?"
            },
            {
                "from": "koopa",
                "to": "bowser",
                "message": "Yes, we successfully pwned their web server King Bowser!"
            },
            {
                "from": "bowser",
                "to": "koopa",
                "message": "Good work. Gwa ha ha ha ha, we will put those Mario bros out of business once and for all! "
            }
        ],
        "flag":FLAG
    }
    res.json(data);
});

var PORT = process.env.PORT || 8080;

app.listen(PORT, () => console.log('Server started at http://localhost:' + PORT));
