from flask import Flask
from flask import request
from flask import jsonify
import mysql.connector
import json
import os

app = Flask(__name__)

with open("config.json", "r") as file:
    config = json.load(file)

host = config["host"]
user = config["user"]
password = config["password"]
database1 = config["database1"]


@app.route("/getcases", methods=["GET"])
def getcases():
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database1
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT c.id, c.id_normative, c.id_law, c.name, c.alias, n.alias as 'alias_normative', l.alias as 'alias_law' FROM cases c INNER JOIN laws l on c.id_law = l.id INNER JOIN normatives n on c.id_normative = n.id WHERE c.active = 1 and l.active = 1 and n.active = 1")

        q1 = mycursor.fetchall()

        Cases = list()

        if q1 is not None:
            Cases["code"] = 0
            Cases["message"] = "OK"
            for q in q1:
                caseItem = dict()
                caseItem["id"],caseItem["id_normative"],caseItem["id_law"],caseItem["name"],caseItem["alias"],caseItem["alias_normative"],caseItem["alias_law"] = q
                Cases.append(caseItem)
        else:
            Cases["code"] = -1
            Cases["message"] = "Register not found"

        return Cases
    except mysql.connector.Error as error:
        message = "Failed in database process. Error description: {}".format(error)
        return {"code": -1, "message": message}
    except Exception as error:
        message = "Error in process. Detail of error: {}".format(error)
        return {"code": -1, "message": message}
    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()

@app.route("/deletedocument/<int:docType>/<int:id>", methods=["DELETE"])
def deletedocument(docType, id):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database1
        )

        mycursor = mydb.cursor()

        if docType == 0:
            mycursor.execute("UPDATE normatives SET active = 0 WHERE id = %s AND active = 1",(id,))
            mycursor.execute("UPDATE principles SET active = 0 WHERE id_normative = %s AND active = 1",(id,))
        elif docType == 1:
            mycursor.execute("UPDATE laws SET active = 0 WHERE id = %s AND active = 1",(id,))
        else:
            return {"code": -1, "message": "Not valid document type"}
        
        mydb.commit()
        
        return {"code": 0, "message": "OK"}
    except mysql.connector.Error as error:
        message = "Failed in database process. Error description: {}".format(error)
        return {"code": -1, "message": message}
    except Exception as error:
        message = "Error in process. Detail of error: {}".format(error)
        return {"code": -1, "message": message}
    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()

@app.route("/getdocument/<int:docType>/<int:id>", methods=["GET"])
def getdocument(docType, id):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database1
        )

        mycursor = mydb.cursor()

        if docType == 0:
            mycursor.execute("SELECT id, name, alias, description FROM normatives WHERE id = %s AND active = 1",(id,))
        elif docType == 1:
            mycursor.execute("SELECT id, name, alias, description FROM laws WHERE id = %s AND active = 1",(id,))
        else:
            return {"code": -1, "message": "Not valid document type"}

        q1 = mycursor.fetchone()

        Document = dict()

        if q1 is not None:
            if docType == 0:
                mycursor.execute("SELECT principle, category_from, category_to FROM principles WHERE id_normative = %s AND active = 1 ORDER BY category_from,category_to,principle",(id,))
                q2 = mycursor.fetchall()

                if q2 is not None and len(q2) > 0:
                    Document["id"], Document["name"], Document["alias"], Document["description"] = q1
                    principles = list()
                    for q in q2:
                        principle = dict()
                        principle["principle"], principle["category_from"], principle["category_to"] = q  
                        principles.append(principle)
                    Document["principles"] = principles
                    Document["code"] = 0
                    Document["message"] = "OK"
                else:
                    Document["code"] = -1
                    Document["message"] = "Detail of principles not found"
            elif docType == 1:
                Document["id"], Document["name"], Document["alias"], Document["description"] = q1
                Document["code"] = 0
                Document["message"] = "OK"
        else:
            Document["code"] = -1
            Document["message"] = "Register not found"

        return Document
    except mysql.connector.Error as error:
        message = "Failed in database process. Error description: {}".format(error)
        return {"code": -1, "message": message}
    except Exception as error:
        message = "Error in process. Detail of error: {}".format(error)
        return {"code": -1, "message": message}
    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()


@app.route("/getdocuments/<int:docType>", methods=["GET"])
def getdocuments(docType):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database1
        )

        mycursor = mydb.cursor()
        if docType == 0:
            mycursor.execute("SELECT id, name, alias FROM normatives WHERE active = 1 ORDER BY id DESC")
        elif docType == 1:
            mycursor.execute("SELECT id, name, alias FROM laws WHERE active = 1 ORDER BY id DESC")
        else:
            return {"code": -1, "message": "Not valid document type"}

        q1 = mycursor.fetchall()

        Documents = dict()
        Documents["code"] = 0
        Documents["message"] = "OK"
        documents = list()

        for document in q1:
            documents.append({"id": document[0], "name": document[1], "alias": document[2]})

        Documents["documents"] = documents
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


@app.route("/createnormative", methods=["POST"])
def createnormative():
    try:
        data = request.form.get("json")
        payload = json.loads(data)
        name = payload["name"]
        alias = payload["alias"]
        description = payload["description"]
        docType = payload["docType"]

        if docType == 0:
            extension = ".txt"
        elif docType == 1:
            extension = ".pdf"
        else:
            return {"code": -1, "message": "Not valid document type"}

        myfile = request.files.get("file")

        # Save database
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database1
        )

        mycursor = mydb.cursor()

        if docType == 0:
            mycursor.execute("SELECT ID FROM normatives WHERE name = %s AND active = 1",(name,))
        elif docType == 1:
            mycursor.execute("SELECT ID FROM laws WHERE name = %s AND active = 1",(name,))

        q1 = mycursor.fetchone()

        if q1 is not None:
            return {"code": -1, "message": "Error: A register with the provided name already exists"}

        if docType == 0:
            mycursor.execute("SELECT ID FROM normatives WHERE alias = %s AND active = 1",(alias,))
        elif docType == 1:
            mycursor.execute("SELECT ID FROM laws WHERE alias = %s AND active = 1",(alias,))

        q1 = mycursor.fetchone()

        if q1 is not None:
            return {"code": -1, "message": "Error: A register with the provided alias already exists"}
        
        if docType == 0:
            mycursor.execute("SELECT MAX(id) FROM normatives")
        elif docType == 1:
            mycursor.execute("SELECT MAX(id) FROM laws")

        q2 = mycursor.fetchone()

        id = 1
        if q2 is not None and q2[0] is not None:
            id = q2[0] + 1

        if docType == 0:
            mycursor.execute("INSERT INTO normatives (id, name, alias, description, active) VALUES (%s, %s, %s, %s, %s)", (id, name, alias, description, 1))
        elif docType == 1:
            mycursor.execute("INSERT INTO laws (id, name, alias, description, active) VALUES (%s, %s, %s, %s, %s)", (id, name, alias, description, 1))
        
        # Principles
        if docType == 0:
            mycursor.execute("SELECT MAX(id) FROM principles")
            q3 = mycursor.fetchone()
            id_norm = 1
            if q3 is not None and q3[0] is not None:
                id_norm = q3[0] + 1

            principles = payload["principles"]
            
            for principle in principles:
                mycursor.execute("INSERT INTO principles (id, id_normative, principle, category_from, category_to, active) VALUES (%s, %s, %s, %s, %s, %s)", (id_norm, id, principle["principle"], principle["category_from"], principle["category_to"], 1))
                id_norm = id_norm + 1

        # Save file
        data_dir = os.path.join(os.getcwd(), "Data")

        if docType == 0:
            normatives_dir = os.path.join(data_dir, "Normatives")
        elif docType == 1:
            normatives_dir = os.path.join(data_dir, "Laws")

        folder_normative_dir = os.path.join(normatives_dir, str(id))

        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        if not os.path.exists(normatives_dir):
            os.mkdir(normatives_dir)

        if not os.path.exists(folder_normative_dir):
            os.mkdir(folder_normative_dir)

        myfile.save(os.path.join(folder_normative_dir,alias+extension))
        mydb.commit()
        return {"code": 0, "message": "Process executed successfully"}
    except mysql.connector.Error as error:
        message = ("Failed in database process. Error description: {}".format(error))
        return {"code": -1, "message": message}
    except Exception as e:
        message = "Error in process. Detail of error: "
        return {"code": -1, "message": message}
    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()

@app.route("/test", methods=["GET"])
def test():
    return "Api working!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)