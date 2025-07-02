from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/loadnormative", methods=["POST"])
def loadnormative(normative):
    try:
        name = request.headers.get("name")
        with open(name+".pdf","wb") as file:
            file.write(normative)
        
        mydb = mysql.connector.connect(
            host="192.168.1.86",
            user="root",
            password="12345678",
            database="assessment"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO normatives (id, name, active) VALUES (%s, %s, %s)"
        val = (1, name, 1)
        mycursor.execute(sql, val)

        mydb.commit()

        return {"code":0,"message":"OK"}
    except mysql.connector.Error as error:
        message = ("Failed to insert into MySQL table {}".format(error))
        return {"code":-1,"message":message}
    finally:
        if mydb.is_connected():
            mydb.close()
            mydb.close()

@app.route("/test", methods=["GET"])
def test():
    return "Api working!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
