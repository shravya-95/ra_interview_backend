from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
import mysql.connector
import json




def getDbConn():
    #connect to the db and return the connection object
    conn = mysql.connector.connect(
        host="dummy",
        user="dummy",
        password="dummy",
        database = "game"
    )

    print(conn)
    return conn
    pass

@app.route('/api')
def hello_world():
    return 'RESTful API for the game data'

@app.route('/api/users/<username>/comments', methods=["GET"]) #No need for qeury params here
# @crossdomain(origin='*')
def comments(username):

    conn=getDbConn()
    mycursor = conn.cursor()

    mycursor.execute("select username, author, comment, TIMESTAMPDIFF(minute,timestamp, UTC_TIMESTAMP()) as timeelapsed from game.comments where username like '%s'" % (username))
    print("select username, author, comment, TIMESTAMPDIFF(minute,timestamp, UTC_TIMESTAMP()) as timeelapsed from game.comments where username like '%s'" % (username))
    myresult = mycursor.fetchall()

    row_headers = [x[0] for x in mycursor.description]  # this will extract row headers
    json_data = []
    for result in myresult:
        json_data.append(dict(zip(row_headers, result)))
    # return json.dumps(json_data)
    return json.dumps(json_data)


@app.route('/api/users/<username>/counts', methods=["GET"])
def counts(username):
    conn = getDbConn()
    mycursor = conn.cursor()

    mycursor.execute("select taggedcount, capturedcount from game.users where username like '%s'" % (username))
    print("select taggedcount, capturedcount from game.users where username like '%s'" % (username))
    myresult = mycursor.fetchall()

    row_headers = [x[0] for x in mycursor.description]  # this will extract row headers
    json_data = []
    for result in myresult:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)

@app.route('/api/users/<username>/ranking', methods=["GET"])
def ranking(username):
    conn = getDbConn()
    mycursor = conn.cursor()

    mycursor.execute(
        "select  count(distinct username) as total from game.users")
    # print("select * from game.users where username like '%s'" % (username))
    myresult = mycursor.fetchall()

    row_headers = [x[0] for x in mycursor.description]  # this will extract row headers
    json_data = []
    for result in myresult:
        json_data.append(dict(zip(row_headers, result)))
    # return json.dumps(json_data)


    mycursor.execute("select ranking from (select  username,row_number() over (order by sum(taggedcount+capturedcount) desc) as ranking from game.users group by username) a where username like '%s'"  %(username));
    print("select ranking from (select  username,row_number() over (order by sum(taggedcount+capturedcount) desc) as ranking from game.users group by username) a where username like '%s'"  %(username));

    myresult = mycursor.fetchall()

    row_headers = [x[0] for x in mycursor.description]  # this will extract row headers
    # json_data = []
    for result in myresult:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)


if __name__ == '__main__':
    app.run()
