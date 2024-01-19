#credit : https://gist.github.com/gauchy and https://github.com/vandaref 
import requests, json

#Notion's token and databaseId
token = '****'
databaseId = '****'

#Notion's headers
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

#Habitica's headers
headersHabitica = {

    "x-api-user": "****",
    "x-api-key": "****"
}

#Completed Status
def completed():
    return 'Completed';
    
def readDatabaseOfNotion(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    # print(res.text)

    with open('./notion.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)

def readHabiticaData(headersHabitica):
    url = "https://habitica.com/api/v3/tasks/user?type=todos"

    res = requests.request("GET", url, headers=headersHabitica)
    data = res.json()
    print(res.status_code)
    # print(res.text)

    with open('./habitica.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def readHabiticaDoneData(headersHabitica):
    url = "https://habitica.com/api/v3/tasks/user?type=completedTodos"

    res = requests.request("GET", url, headers=headersHabitica)
    data = res.json()
    print(res.status_code)
    # print(res.text)

    with open('./habitica_done.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def createTodoInHabitica(name, priority, headersHabitica):
    if priority == "Low":
        p = 1
    elif priority == "Medium":
        p = 1.5
    elif priority == "High":
        p = 2
    url = "https://habitica.com/api/v3/tasks/user"
    name = name
    res = requests.post(url, headers=headersHabitica, json={"text": name, "type": "todo", "priority":p})
    data = res.json()
    #print(res.text)


def scoreTaskInHabitica(id):
    url = f"https://habitica.com/api/v3/tasks/{id}/score/up"
    res = requests.post(url, headers=headersHabitica)
    print(res.status_code)
    
def scoreTaskInNotion(name, headers):
    url = f"https://api.notion.com/v1/pages/{name}"
    res = requests.patch(url, headers=headers, json={"properties": {"Status" : {"select" :{"name": completed()}}}})
    data = res.json()
    #print(res.text)
    print(res.status_code)


def isAbsentInHabitica(taskName, habiticaList):
    for i in habiticaList:
        if taskName == i['name']:
            return False
    return True

def getHabiticaList(habitica_file):
    lst = []
    with open(habitica_file, encoding="utf-8") as f:
        data = json.load(f)

    for i in data['data']:
        name = i['text']
        id = i['id']
        dict = {'name':name , 'id':id}
        lst.append(dict)
    f.close()
    return lst

def getNotionList(condn):
    lst = []
    with open("notion.json", encoding="utf-8") as f:
        data = json.load(f)

    for i in data['results']:
        name = i['properties']['Name']['title'][0]['text']['content']
        status = i['properties']['Status']['select']['name']
        priority = i['properties']['Priority']['select']['name']
        id = i['id']

        if condn(status):
            dict = {'name':name , 'priority':priority, 'id':id}
            lst.append(dict)
    f.close()
    return lst



def notionDoneCondn(status):
    return status == completed()


def notionNotDoneCondn(status):
    return status != completed()


def getDoneListOfNotion():
    return getNotionList(notionDoneCondn)


def getNotDoneListOfNotion():
    return getNotionList(notionNotDoneCondn)


def getTaskId(name, list):

    for i in list:
        if name == i['name']:
            return i['id']
    


def syncNotionToHabitica():
    print('==========================')
    print('Syncing Notion to Habitica')
    print('==========================')
    habiticaList = getHabiticaList("habitica.json")
    notionDoneList = getDoneListOfNotion()

    for task in notionDoneList:
        print('Processing Completed Notion Task in Habitica ' + task['name'])
        name = task['name']
        priority = task['priority']
        habiticaid = getTaskId(name,habiticaList)
        if habiticaid is not None:
            print('Scoring in Habitica for ' + name + ':' + habiticaid)
            scoreTaskInHabitica(habiticaid)

    notionNotDoneList = getNotDoneListOfNotion()

    for task in notionNotDoneList:
        print('Processing Incomplete Notion Task in Habitica ' + task['name'])
        if isAbsentInHabitica(task['name'],habiticaList):
            print('Missing in Habitica, Creating '+ task['name'] )
            createTodoInHabitica(task['name'], task['priority'], headersHabitica)
            


def syncHabiticaToNotion():
    print('==========================')
    print('Syncing Habitica to Notion')
    print('==========================')
    notionNotDoneList = getNotDoneListOfNotion()
    habiticaDoneList = getHabiticaList("habitica_done.json")
    for task in notionNotDoneList:
        try:
            print('Processing Notion task ' + task['name'])
            habitica_name = task['name']
            for i in habiticaDoneList :
                if habitica_name == i['name']:
                    print('Scoring in Notion for ' + habitica_name + ':' + task['id'])
                    scoreTaskInNotion(task['id'], headers)
            
        except Exception as e:
            #print(e)
            print('Cannot score : Old or absent Habitica todo ' + task['name'])
        
def readDB():
    print('==========================')
    print('Reading data')
    print('==========================')
    print('Reading Notion Data')
    readDatabaseOfNotion(databaseId, headers)
    print('Reading Habitica Data')
    readHabiticaData(headersHabitica)
    print('Reading Habitica Done Data')
    readHabiticaDoneData(headersHabitica)
    
    
readDB()
syncNotionToHabitica()
syncHabiticaToNotion()
