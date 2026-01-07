from flask import Flask
from flask import request
from flask import jsonify
from pypdf import PdfReader
from decimal import Decimal, getcontext
import random
import mysql.connector
import json
import os
from assessment import queryGpt
from compliances import queryCompliances
from noncompliances import queryNoncompliances

app = Flask(__name__)

with open("config.json", "r") as file:
    config = json.load(file)

host = config["host"]
user = config["user"]
password = config["password"]
database1 = config["database1"]

@app.route("/generatefiles", methods=["POST"])
def generatefiles():
    try:
         # Save database
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database1
        )
        mycursor = mydb.cursor()

        data = request.form.get("json")
        payload = json.loads(data)
        text = "category,principle,goal,logprob"

        for item in payload:
            id = item["id"]
            id_normative = item["id_normative"]
            alias = item["alias"]

            if id > 0:
                # Single case
                mycursor.execute("SELECT b.principle, c.category, c.log_prob FROM cases a INNER JOIN principles b on a.id_normative = b.id_normative INNER JOIN annotations c on a.id = c.id_case and a.version = c.version WHERE c.log_prob <= 0 and c.category between b.category_from and b.category_to and a.id = %s and a.active = 1 and b.active = 1 and c.active = 1 ORDER BY b.principle, c.category, c.log_prob",(id,))
                q1 = mycursor.fetchall()
                for q in q1:
                    text = text + "\n" + alias + "," + str(q[0]) + "," + str(q[1]) + "," + str(q[2].replace(",","."))
            else:
                if id_normative == 0:
                    # Compound case
                    idCases = item["subcases"]
                    placeholders = ",".join(["%s"] * len(idCases))
                    query = f"SELECT b.principle, c.category, MAX(c.log_prob) as log_prob FROM cases a INNER JOIN principles b on a.id_normative = b.id_normative INNER JOIN annotations c on a.id = c.id_case and a.version = c.version WHERE c.log_prob <= 0 and c.category between b.category_from and b.category_to and a.id IN ({placeholders}) and a.active = 1 and b.active = 1 and c.active = 1 GROUP BY b.principle, c.category ORDER BY b.principle, c.category, log_prob"
                    mycursor.execute(query, tuple(idCases))
                    q1 = mycursor.fetchall()
                    for q in q1:
                        text = text + "\n" + alias + "," + str(q[0]) + "," + str(q[1]) + "," + str(q[2].replace(",","."))
                else:
                    # Normative case_
                    mycursor.execute("SELECT principle, category_from, category_to FROM principles where id_normative = %s and active = 1",(id_normative,))
                    q1 = mycursor.fetchall()
                    for q in q1:
                        principle = q[0]
                        min = q[1]
                        max = q[2]
                        for n in range(min, max+1):
                            text = text + "\n" + alias + "," + str(principle) + "," + str(n) + ",0"
        
        return {"code": 0, "message": "Process executed successfully", "text": text}
    except mysql.connector.Error as error:
        message = ("Failed in database process. Error description: {}".format(error))
        return {"code": -1, "message": message}
    except Exception as error:
        message = "Error in process. Detail of error: {}".format(error)
        return {"code": -1, "message": message}
    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()

@app.route("/generateview/<int:myType>/<int:mySubtype>/<int:id>", methods=["GET"])
def generateview(myType, mySubtype, id):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database1
        )

        mycursor = mydb.cursor()

        if myType == 0:
            mycursor.execute("SELECT alias FROM normatives WHERE id = %s AND active = 1", (id,))
            q1 = mycursor.fetchone()
            if q1 is None:
                return {"code": -1, "message": "Error: Normative not found"}
            path = os.path.join(os.getcwd(), "Data", "Normatives", str(id), q1[0] + ".txt")
        elif myType == 1:
            mycursor.execute("SELECT alias FROM laws WHERE id = %s AND active = 1", (id,))
            q1 = mycursor.fetchone()
            if q1 is None:
                return {"code": -1, "message": "Error: Law not found"}
            path = os.path.join(os.getcwd(), "Data", "Laws", str(id), q1[0] + ".pdf")
        elif myType == 2:
            mycursor.execute("SELECT version, version_cs, version_ncs FROM cases WHERE id = %s AND active = 1", (id,))
            q1 = mycursor.fetchone()
            if q1 is None:
                return {"code": -1, "message": "Error: Case not found"}

            if mySubtype == 0:
                path = os.path.join(os.getcwd(), "Data", "Cases", str(id), "gpt_"+ str(q1[0]) + ".json")
            elif mySubtype == 1:
                path = os.path.join(os.getcwd(), "Data", "Cases", str(id), "gpt_cs_"+ str(q1[1]) + ".txt")
            elif mySubtype == 2:
                path = os.path.join(os.getcwd(), "Data", "Cases", str(id), "gpt_ncs_"+ str(q1[2]) + ".txt")
            else:
                return {"code": -1, "message": "Error: Operation subtype not valid"}    
        else:
            return {"code": -1, "message": "Error: Operation type not valid"}

        if myType == 1:
            reader = PdfReader(path)
            number_of_pages = len(reader.pages)

            text = ""
            for page in range(len(reader.pages)):
                text = text + reader.pages[page].extract_text() + "\n"

            text = text.replace("\"","'")
            text = text.replace("\\","/")
        else:
            with open(path,"r") as handle:
                text = handle.read()

        return {"code": 0, "message": "View generated successfully", "text": text}
    except mysql.connector.Error as error:
        message = "Failed in database process. Error description: {}".format(error)
        return {"code": -1, "message": message}
    except Exception as error:
        message = "Error in process. Detail of error: {}".format(error)
        return {"code": -1, "message": message}
    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()

@app.route("/generatequery", methods=["POST"])
def generatequery():
    try:
        data = request.form.get("json")
        payload = json.loads(data)

        idCase = payload["idCase"]
        idNormative = payload["idNormative"]
        idLaw = payload["idLaw"]
        myType = payload["type"]
        apiKey = payload["apiKey"]

        # Save database
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database1
        )

        mycursor = mydb.cursor()

        # Case
        if myType == 0:
            mycursor.execute("SELECT version FROM cases WHERE id = %s AND active = 1",(idCase,))
        elif myType == 1:
            mycursor.execute("SELECT version_cs FROM cases WHERE id = %s AND active = 1",(idCase,))
        elif myType == 2:
            mycursor.execute("SELECT version_ncs FROM cases WHERE id = %s AND active = 1",(idCase,))
        else:
            return {"code": -1, "message": "Error: Operation type not valid"}
        
        q1 = mycursor.fetchone()
        if q1 is None:
            return {"code": -1, "message": "Error: Case register not found"}

        id = q1[0] + 1

        # Normative
        mycursor.execute("SELECT name, alias FROM normatives WHERE id = %s AND active = 1",(idNormative,))
        q1 = mycursor.fetchone()
        if q1 is None:
            return {"code": -1, "message": "Error: Normative register not found"}
        
        name_normative = q1[0]
        alias_normative = q1[1]
        dir = os.path.join(os.getcwd(), "Data", "Normatives", str(idNormative), alias_normative + ".txt")

        with open(dir,"r") as handle:
            txtNormative = handle.read()
        
        # Principles
        mycursor.execute("SELECT category_from, category_to FROM principles WHERE id_normative = %s AND active = 1",(idNormative,))
        q1 = mycursor.fetchall()
        if q1 is None:
            return {"code": -1, "message": "Error: Principles registers not found for normative id " + str(idNormative) + " " + name_normative + " (" + alias_normative + ")"}
        
        n = 0
        for q in q1:
            n = n + q[1] - q[0] + 1

        # Law
        mycursor.execute("SELECT name, alias FROM laws WHERE id = %s AND active = 1",(idLaw,))
        q1 = mycursor.fetchone()
        name_law = q1[0]
        alias_law = q1[1]
        if q1 is None:
            return {"code": -1, "message": "Error: Law register not found"}
        
        dir = os.path.join(os.getcwd(), "Data", "Laws", str(idLaw), alias_law + ".pdf")
        
        reader = PdfReader(dir)
        number_of_pages = len(reader.pages)

        txtLaw = ""
        for page in range(len(reader.pages)):
            txtLaw = txtLaw + reader.pages[page].extract_text() + "\n"

        txtLaw = txtLaw.replace("\"","'")
        txtLaw = txtLaw.replace("\\","/")
        
        # Gpt
        if myType == 0:
            result = queryGpt(apiKey, idNormative, name_normative, alias_normative, idLaw, name_law, alias_law, txtNormative, txtLaw, n)
        elif myType == 1:
            result = queryCompliances(apiKey, idNormative, name_normative, alias_normative, idLaw, name_law, alias_law, txtNormative, txtLaw, n)
        elif myType == 2:
            result = queryNoncompliances(apiKey, idNormative, name_normative, alias_normative, idLaw, name_law, alias_law, txtNormative, txtLaw, n)

        # SavePath
        if myType == 0:
            name = "gpt_"+ str(id) + ".json"
        elif myType == 1:
            name = "gpt_cs_"+ str(id) + ".txt"
        elif myType == 2:
            name = "gpt_ncs_"+ str(id) + ".txt"

        dir = os.path.join(os.getcwd(), "Data")
        if not os.path.exists(dir):
            os.mkdir(dir)
        dir = os.path.join(dir, "Cases")
        if not os.path.exists(dir):
            os.mkdir(dir)
        dir = os.path.join(dir, str(idCase))
        if not os.path.exists(dir):
            os.mkdir(dir)
        
        with open(os.path.join(dir, name), "w") as handle:
            json.dump(result, handle, indent=4)

        # Update database
        if myType == 0:
            mycursor.execute("SELECT MAX(id) FROM annotations")
            q2 = mycursor.fetchone()

            if q2 is not None and q2[0] is not None:
                seq = q2[0]
            else:
                seq = 0

            mycursor.execute("UPDATE cases SET version = %s WHERE id = %s AND active = 1",(id, idCase,))

            ls_categories = range(0,n)
            getcontext().prec = 40  # enough precision
            r = Decimal(random.random())
            num = Decimal('-100') + r * (Decimal('-10') - Decimal('-100'))
            num = num.quantize(Decimal('1.' + '0'*19))
            ls_logprobs = [num] * n

            for register in result["categories"]:
                if register["category"] == "None":
                    break
                else:
                    category = register["category"]
                    ls_logprobs[category] = register["log_prob"]

            for ls_category in ls_categories:
                seq = seq + 1
                mycursor.execute("INSERT INTO annotations (id, id_case, version, category , log_prob, active) values(%s,%s,%s,%s,%s,1)",(seq, idCase, id, ls_category, ls_logprobs[ls_category]))
        elif myType == 1:
            mycursor.execute("UPDATE cases SET version_cs = %s WHERE id = %s AND active = 1",(id, idCase,))
        elif myType == 2:
            mycursor.execute("UPDATE cases SET version_ncs = %s WHERE id = %s AND active = 1",(id, idCase,))

        mydb.commit()
        return {"code": 0, "message": "GPT query executed successfully", "id": id}
    except mysql.connector.Error as error:
        message = ("Failed in database process. Error description: {}".format(error))
        return {"code": -1, "message": message}
    except Exception as error:
        message = "Error in process. Detail of error: {}".format(error)
        return {"code": -1, "message": message}
    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()

@app.route("/deletecase/<int:id>", methods=["DELETE"])
def deletecase(id):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database1
        )

        mycursor = mydb.cursor()
        mycursor.execute("UPDATE cases SET active = 0 WHERE id = %s AND active = 1",(id,))
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


@app.route("/getcase/<int:idNormative>/<int:idLaw>", methods=["GET"])
def getcase(idNormative, idLaw):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database1
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT id, id_normative, id_law, name, alias, description, version, version_cs, Version_ncs FROM cases WHERE id_normative = %s AND id_law = %s AND active = 1", (idNormative, idLaw,))
        q1 = mycursor.fetchone()

        Response = dict()

        if q1 is not None:
            Response["code"] = 0
            Response["message"] = "OK"
            Response["id"] = q1[0]
            Response["extra_1"] = q1[1]
            Response["extra_2"] = q1[2]
            Response["name"] = q1[3]
            Response["alias"] = q1[4]
            Response["description"] = q1[5]
            Response["gpt"] = "gpt_"+ str(q1[6]) + ".json"
            Response["gpt_cs"] = "gpt_cs_"+ str(q1[7]) + ".txt"
            Response["gpt_ncs"] = "gpt_ncs_"+ str(q1[8]) + ".txt"

        else:
            Response["code"] = 0
            Response["message"] = "Register not found"
            Response["id"] = 0

        return Response
    except mysql.connector.Error as error:
        message = "Failed in database process. Error description: {}".format(error)
        return {"code": -1, "message": message}
    except Exception as error:
        message = "Error in process. Detail of error: {}".format(error)
        return {"code": -1, "message": message}
    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()

@app.route("/createcase", methods=["POST"])
def createcase():
    try:
        data = request.form.get("json")
        payload = json.loads(data)
        id_normative = payload["id_extra1"]
        id_law = payload["id_extra2"]
        name = payload["name"]
        alias = payload["alias"]
        description = payload["description"]
        version = 0
        version_cs = 0
        version_ncs = 0
        active = 1

        # Save database
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database1
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT ID FROM cases WHERE name = %s AND active = 1",(name,))

        q1 = mycursor.fetchone()

        if q1 is not None:
            return {"code": -1, "message": "Error: A register with the provided name already exists"}

        mycursor.execute("SELECT ID FROM cases WHERE alias = %s AND active = 1",(alias,))

        q1 = mycursor.fetchone()

        if q1 is not None:
            return {"code": -1, "message": "Error: A register with the provided alias already exists"}
        
        mycursor.execute("SELECT MAX(id) FROM cases")

        q2 = mycursor.fetchone()

        id = 1
        if q2 is not None and q2[0] is not None:
            id = q2[0] + 1

        mycursor.execute("INSERT INTO cases (id, id_normative, id_law, name, alias, description, version, version_cs, version_ncs, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, id_normative, id_law, name, alias, description, version, version_cs, version_ncs, 1))
        mydb.commit()
        return {"code": 0, "message": "Process executed successfully"}
    except mysql.connector.Error as error:
        message = ("Failed in database process. Error description: {}".format(error))
        return {"code": -1, "message": message}
    except Exception as e:
        message = "Error in process. Detail of error: {}".format(error)
        return {"code": -1, "message": message}
    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()


@app.route("/getversion/<int:id>", methods=["GET"])
def getversion(id):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database1
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT version FROM cases WHERE id = %s AND active = 1",(id,))
        q1 = mycursor.fetchone()

        Response = dict()

        if q1 is not None:
            Response["code"] = 0
            Response["message"] = "OK"
            Response["id"] = q1[0]
        else:
            Response["code"] = -1
            Response["message"] = "Register not found"

        return Response
    except mysql.connector.Error as error:
        message = "Failed in database process. Error description: {}".format(error)
        return {"code": -1, "message": message}
    except Exception as error:
        message = "Error in process. Detail of error: {}".format(error)
        return {"code": -1, "message": message}
    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()


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
        mycursor.execute("SELECT c.id, c.id_normative, c.id_law, c.name, c.alias, n.alias as 'alias_normative', l.alias as 'alias_law' FROM cases c INNER JOIN laws l on c.id_law = l.id INNER JOIN normatives n on c.id_normative = n.id WHERE c.active = 1 and l.active = 1 and n.active = 1 ORDER BY c.id DESC")

        q1 = mycursor.fetchall()

        Cases = dict()

        if q1 is not None:
            Cases["code"] = 0
            Cases["message"] = "OK"
            Cases["cases"] = list()

            for q in q1:
                caseItem = dict()
                caseItem["id"],caseItem["id_normative"],caseItem["id_law"],caseItem["name"],caseItem["alias"],caseItem["alias_normative"],caseItem["alias_law"] = q
                Cases["cases"].append(caseItem)
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
            mycursor.execute("UPDATE cases SET active = 0 WHERE id_normative = %s AND active = 1",(id,))
        elif docType == 1:
            mycursor.execute("UPDATE laws SET active = 0 WHERE id = %s AND active = 1",(id,))
            mycursor.execute("UPDATE cases SET active = 0 WHERE id_law = %s AND active = 1",(id,))
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
        message = "Error in process. Detail of error: {}".format(error)
        return {"code": -1, "message": message}
    finally:
        if mydb is not None and mydb.is_connected():
            mydb.close()

@app.route("/test", methods=["GET"])
def test():
    return "Api working!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)