function generatePassword(length) {
    var charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        retVal = "";
    for (var i = 0, n = charset.length; i < length; ++i) {
        retVal += charset.charAt(Math.floor(Math.random() * n));
    }
    return retVal;
}

db = new Mongo().getDB("nosqli");

db.createCollection('users', { capped: false });

db.users.insert([
    { "username": "paul", "password": generatePassword(32)  },
    { "username": "cory", "password": generatePassword(32) },
    { "username": "ryan", "password": generatePassword(32) },
    { "username": "jon", "password": generatePassword(32) },
    { "username": "andrew", "password": generatePassword(32) }
]);