import requests
import json
import os
from http import cookies
from pprint import pprint

provinceJSON = "province.json"
kabupatenJSON = "kabupaten.json"
kecamatanJSON = "kecamatan.json"
kelurahanJSON = "kelurahan.json"
oauthFile = "oauth_location.txt"

hostAPI = 'https://x.rajaapi.com/'
getTokenURI = hostAPI + 'poe'

# UTILS:
def getProvincesURI(token):
    URI = hostAPI + 'MeP7c5ne' + token + '/m/wilayah/provinsi'
    return URI
def getKabupatenURI(token, provinceID):
    URI = hostAPI + 'MeP7c5ne' + token + '/m/wilayah/kabupaten?idpropinsi=' + str(provinceID)
    return URI
def getKecamatanURI(token, kabupatenID):
    URI = hostAPI + 'MeP7c5ne' + token + '/m/wilayah/kecamatan?idkabupaten=' + str(kabupatenID)
    return URI
def getKelurahanURI(token, kecamatanID):
    URI = hostAPI + 'MeP7c5ne' + token + '/m/wilayah/kelurahan?idkecamatan=' + str(kecamatanID)
    return URI

def writeFile(fileName, fileData):
    file = open(fileName, "w")
    file.write(fileData)
    file.close()

def readFile(fileName):
    file = open(fileName, "r")
    res = file.read()
    file.close()

    return res

def readFileJSON(fileName):
    with open(fileName) as json_file:
        data = json.load(json_file)

    res = [p for p in data]

    return data

def validateFileJSON(fileName, callBack):
    result = ''
    try:
        result = readFile(fileName)
    except Exception as e:
        print(e, 'creating new file', fileName)
        writeFile(fileName, json.dumps([]))
        result = readFile(fileName)
        pass

    return callBack()

def deleteFile(fileName):
    if os.path.exists(fileName):
      os.remove(fileName)
    else:
      print(fileName, 'does not exists')

# OAUTH:
def fetchToken():
    r = requests.get(getTokenURI)
    res = r.json()
    writeFile(oauthFile, res.get("token"))

def returnToken():
    token = readFile(oauthFile)

    return token

def validateToken():
    token = ''
    try:
        token = returnToken()
    except Exception as e:
        print(e, 'creating new token file')
        fetchToken()
        token = returnToken()
        pass

    return token

# ACTUAL MINING
def getProvinces():
    token = validateToken()
    r = requests.get(getProvincesURI(token))
    res = r.json()
    data = json.dumps(res.get("data"))
    pprint(data)
    writeFile(provinceJSON, data)

def getKabupaten():
    token = validateToken()
    province = readFileJSON(provinceJSON)
    for p in province:

        r = requests.get(getKabupatenURI(token, p.get("id")))
        res = r.json()
        kabupaten = readFileJSON(kabupatenJSON)
        data = json.dumps(kabupaten + res.get("data"))
        pprint(data)
        writeFile(kabupatenJSON, data)

def getKecamatan():
    token = validateToken()
    kabupaten = readFileJSON(kabupatenJSON)
    for k in kabupaten:

        r = requests.get(getKecamatanURI(token, k.get("id")))
        res = r.json()
        kecamatan = readFileJSON(kecamatanJSON)
        data = json.dumps(kecamatan + res.get("data"))
        pprint(data)
        writeFile(kecamatanJSON, data)

def getKelurahan():
    token = validateToken()
    kecamatan = readFileJSON(kecamatanJSON)
    for k in kecamatan:

        r = requests.get(getKecamatanURI(token, k.get("id")))
        res = r.json()
        kelurahan = readFileJSON(kelurahanJSON)
        data = json.dumps(kelurahan + res.get("data"))
        pprint(data)
        writeFile(kelurahanJSON, data)
print('==================================================cleaning files==================================================')
deleteFile(provinceJSON)
deleteFile(kabupatenJSON)
deleteFile(kecamatanJSON)
deleteFile(kelurahanJSON)

print('==================================================validate provinces==================================================')
getProvinces()
print('==================================================validate kabupaten==================================================')
validateFileJSON(kabupatenJSON, getKabupaten)
print('==================================================validate kecamatan==================================================')
validateFileJSON(kecamatanJSON, getKecamatan)
print('==================================================validate kelurahan==================================================')
validateFileJSON(kelurahanJSON, getKelurahan)
