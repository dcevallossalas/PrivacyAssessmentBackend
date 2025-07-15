from flask import Flask
from flask import request
from flask import jsonify
import mysql.connector
import json
import os

app = Flask(__name__)

@app.route("/getdocuments/<type>", methods=["GET"])
def getdocuments(type):
    try:
        mydb = mysql.connector.connect(
            host="192.168.1.86",
            user="assessment",
            password="12345678",
            database="assessment"
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT id, name, alias FROM normatives WHERE active = 1 ORDER BY id DESC",(name,))
        q1 = mycursor.fetchall()

        Documents = dict()
        Documents["code"] = 0
        Documents["message"] = "OK"
        documents = list()

        for document in q1:
            documents.add({"id": document[0], "name": document[1], "alias": document[2]})

        return Documents
    except mysql.connector.Error as error:
        message = "Failed in database process. Error description: {}".format(error)
        return {"code": -1, "message": message}
    except Exception as error:
        message = "Error in process. Detail of error: {}".format(error)
        return {"code": -1, "message": message}
    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()


@app.route("/loadnormative", methods=["POST"])
def loadnormative():
    try:
        data = request.form.get("json")
        payload = json.loads(data)
        name = payload["name"]
        extension = payload["extension"]
        myfile = request.files.get("file")

        # Save database
        mydb = mysql.connector.connect(
            host="192.168.1.86",
            user="assessment",
            password="12345678",
            database="assessment"
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT ID FROM normatives WHERE name = %s AND active = 1",(name,))
        q1 = mycursor.fetchone()

        if q1 is not None:
            return jsonify({"code": -1, "message": "Error: A register with the provided name already exists"})
        
        mycursor.execute("SELECT MAX(ID) FROM normatives")
        q2 = mycursor.fetchone()
        id = 1
        if q2 is not None:
            if q2[0] is not None:
                id = q2[0] + 1

        mycursor.execute("INSERT INTO normatives (id, name, active) VALUES (%s, %s, %s)", (id, name, 1))
        mydb.commit()

        # Save file
        data_dir = os.path.join(os.getcwd(), "Data")
        normatives_dir = os.path.join(data_dir, "Normatives")
        folder_normative_dir = os.path.join(normatives_dir, str(id))

        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        if not os.path.exists(normatives_dir):
            os.mkdir(normatives_dir)

        if not os.path.exists(folder_normative_dir):
            os.mkdir(folder_normative_dir)

        myfile.save(os.path.join(folder_normative_dir,name+extension))
        return {"code": 0, "message": "Process executed successfully"}
    except mysql.connector.Error as error:
        message = ("Failed in database process. Error description: {}".format(error))
        return jsonify({"code": -1, "message": message})
    except Exception as e:
        message = "Error in process. Detail of error: "
        return jsonify({"code": -1, "message": message})
    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()

@app.route("/test", methods=["GET"])
def test():
    return "Api working!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)