## process_request.py
# Primary Owner: Andrew Downie

import jsonOpConverter
import error_message
import standards
import json

#####
##### Json To Sql Parms
#####
def JsonToSqlParms(jsonRequest):
    loadedJson = ""


    ###
    ### Load the Json request
    ###
    try:
        loadedJson = json.loads(jsonRequest)
    except:
    	return standards.InvalidJSON()


    ###
    ### Check that required keys are present
    ###
    if 'operation' not in loadedJson:
    	return standards.MissingOperation()
    elif 'animals' not in loadedJson:
    	return standards.MissingAnimal()
    elif 'field' not in loadedJson:
    	return standards.MissingField()


    ###
    ### Collect values of required keys
    ###
    operation = loadedJson['operation']
    animals = loadedJson['animals']
    fields = loadedJson['field']

    sqlParms = ParseJsonBranch(fields, None)
    return sqlParms


def ParseJsonBranch(jsonBranch, lastOperator):
    try:
        if(type(jsonBranch) == type(dict())):
            for key, val in jsonBranch.items():
                if(str(key)[0] == "$"):
                    return ParseJsonBranch(val, str(key)[1:])
                else:
                    return JsonToSqlParm(jsonBranch)
        elif(type(jsonBranch) == type(list())):
            sqlPiece = "("
            for i in range(0, len(jsonBranch)):
                sqlPiece += ParseJsonBranch(jsonBranch[i], lastOperator)
                if(i < len(jsonBranch)-1):
                    sqlPiece += " " + str(lastOperator) + " "


            sqlPiece += ")"
            return sqlPiece

    except Exception as e:
        print(">>ERROR2: " + str(e) + "\n")
        return None



def JsonToSqlParm(jsonLeaf):
    try:
        for field, jsonKeyVal in jsonLeaf.items():
            for operator, value in jsonKeyVal.items():
                return str(field) + " " + jsonOpConverter.Convert(operator) + " " + str(value)
    except Exception as e:
        print(">>ERROR3: " + str(e) + "\n")