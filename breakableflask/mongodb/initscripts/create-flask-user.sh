mongo --eval "\
    db = connect('localhost:27017/admin'); \
    db.auth('$MONGO_INITDB_ROOT_USERNAME', '$MONGO_INITDB_ROOT_PASSWORD'); \
    db = db.getSiblingDB('$MONGO_FLASK_DATABASE'); \
    db.createUser({ \
        user: '$MONGO_FLASK_USER_NAME', \
        pwd: '$MONGO_FLASK_USER_PASSWORD', \
        roles: [{ \
            role: 'read', \
            db: '$MONGO_FLASK_DATABASE' \
        }] \
    });"
