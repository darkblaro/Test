import csv, json


gJsonList=[]
listOfIds=[]

def getNode(name, description,parent, readOnly=0):
    index=int(listOfIds[-1]+1)
    el={"id":index,"name":name, "description":description,"parent":parent,"read_only":readOnly,"children":[]}
    return el
    

def createJson(file):
'''
Function createJson() gets file *.csv and builds JSON tree.
If node has subnode (or children), the subnode will be placed in parent's array named 'childre'.
'''
    global gJsonList
    with open(file) as myFile:
        lines=myFile.read().split('\n')
        lines=lines[1:]
    
    entry={}
    jsonList=[]
    for d in lines:
        if d=="":
            continue
        id, name, description, parent, readOnly = d.split('\t')
        entry={'id':int(id),'name':name,'description':description,'parent':int(parent),'read_only':int(readOnly),"children":[]}
        listOfIds.append(entry['id'])
        if entry['parent']==0:
            jsonList.append(entry)
        else:
            ind=int(entry['parent'])-1
            if ind<len(jsonList):
                jsonList[ind]['children'].append(entry)
            else:
                for i in range(len(jsonList)):
                    for j in range(len(jsonList[i]['children'])):
                        if jsonList[i]['children'][j]['id']==entry['parent']:
                            jsonList[i]['children'][j]['children'].append(entry)
                        else:
                            for k in range(len(jsonList[i]['children'][j]['children'])):
                                if jsonList[i]['children'][j]['children'][k]['id']==entry['parent']:
                                    jsonList[i]['children'][j]['children'][k]['children'].append(entry)
                                else:
                                    for l in range(len(jsonList[i]['children'][j]['children'][k]['children'])):
                                        if jsonList[i]['children'][j]['children'][k]['children'][l]['id']==entry['parent']:
                                            jsonList[i]['children'][j]['children'][k]['children'][l]['children'].append(entry)
    gJsonList=list(jsonList)

def update_node(id, name):
'''
This function gets node's ID and name to update.
The function checkes if ID is in list (or ID does exist), finds the node by ID
and updates its name. If ID does not exist, the function will print error message.
The function also checks if the node is 'read_only'. If read_only=1 tne node cannot be changed
'''
    if id in listOfIds:
        for i in range(len(gJsonList)):
            if gJsonList[i]['id']==id:
                if not gJsonList[i]['read_only']:
                    print("Cannot update the node. Read only node")
                    return 0
                gJsonList[i]['name']=name
                return 1
            else:
                childs=gJsonList[i]['children']
                for j in range(len(childs)):
                    if childs[j]['id']==id:
                        if childs[j]['read_only']:
                            print("Unable to modify the node. Read only node")
                            return 0
                        gJsonList[i]['children'][j]['name']=name
                        return 1
                    else:
                        innerchild=childs[j]["children"]
                        for k in range(len(innerchild)):
                            if innerchild[k]["id"]==id:
                                if innerchild[k]['read_only']:
                                    print("Unable to modify the node. Read only node")
                                    return 0
                                gJsonList[i]['children'][j]['children'][k]['name']=name
                                return 1
                            else:
                                innerchild2=innerchild[k]['children']
                                for l in range(len(innerchild2)):
                                    if innerchild2[l]['id']==id:
                                        if innerchild2[l]['read_only']:
                                            print("Unable to modify the node. Read only node")
                                            return 0
                                        gJsonList[i]['children'][j]['children'][k]['children'][l]['name']=name
                                        return 1
    else:
        print("Unable to update the node. Id does not exist")
        return 0

def delete_node(id): #delete node by id. if readOnly=0
'''
This function gets ID of the node that should be deleted. If ID exists, the node
will be deleted. If ID does not exist the function will print error message. Function also 
checks if selected node can be deleted, i.e. read_only = 0.
'''
    if id in listOfIds:
        for i in range(len(gJsonList)):
            if gJsonList[i]['id']==id:
                if not gJsonList[i]['read_only']:
                    print("Unable to delete the node. Read only node")
                    return 0
                del gJsonList[i]
                return 1
            else:
                childs=gJsonList[i]['children']
                for j in range(len(childs)):
                    if childs[j]['id']==id:
                        if childs[j]['read_only']:
                            print("Unable to delete the node. Read only node")
                            return 0
                        del gJsonList[i]['children'][j]
                        return 1
                    else:
                        innerchild=childs[j]["children"]
                        for k in range(len(innerchild)):
                            if innerchild[k]["id"]==id:
                                if innerchild[k]['read_only']:
                                    print("Unable to delete the node. Read only node")
                                    return 0
                                del gJsonList[i]['children'][j]['children'][k]
                                return 1
                            else:
                                innerchild2=innerchild[k]['children']
                                for l in range(len(innerchild2)):
                                    if innerchild2[l]['id']==id:
                                        if innerchild2[l]['read_only']:
                                            print("Unable to delete the node. Read only node")
                                            return 0
                                        del gJsonList[i]['children'][j]["children"][k]['children'][l]
                                        return 1
    else:
        print("Unable to delete the node. Id does not exist")
        return 0

def create_node(parent, node): #node is JSON object
'''
This function checks if parent exists and it can be modified (read_only=0).
If check passes new child will be added (or inserted) in to the table.
'''
    for i in range(len(gJsonList)):
        if gJsonList[i]['id']==parent:
            gJsonList[i]['children'].append(node)
            return 1
        else:
            child=gJsonList[i]['children']
            for j in range(len(child)):
                if child[j]['id']==parent:
                    gJsonList[i]['children'][j]['children'].append(node)
                    return 1
                else:
                    innerchild=child[j]['children']
                    for k in range(len(innerchild)):
                        if innerchild[k]['id']==parent:
                            gJsonList[i]['children'][j]['children'][k]['children'].append(node)
                            return 1
                        else:
                            innerchild2=innerchild[k]['children']
                            for l in range(len(innerchild2)):
                                if innerchild2[l]['id']==parent:
                                    gJsonList[i]['children'][j]['children'][k]['children'][l]['children'].append(node)
                                    return 1
    return 0


def export_csv():
'''
export_csv passes all nodes and subnodes in the tree and generates *.csv file
'''
    elementList=['id\tname\tdescription\tparent\tread_only\n']
    file2write=open("newCsvFile.csv",'w')
    for i in range(len(gJsonList)):
        line=(str(gJsonList[i]['id'])
        +'\t'+str(gJsonList[i]['name'])
        +'\t'+str(gJsonList[i]['description'])
        +'\t'+str(gJsonList[i]['parent'])
        +'\t'+str(gJsonList[i]['read_only']))+'\n'
        elementList.append(line)
        if not len(gJsonList[i]['children'])==0:
            child=gJsonList[i]['children']
            for j in range(len(child)):
                line=(str(child[j]['id'])
                +'\t'+str(child[j]['name'])
                +'\t'+str(child[j]['description'])
                +'\t'+str(child[j]['parent'])
                +'\t'+str(child[j]['read_only']))+'\n'
                elementList.append(line)
                if not len(gJsonList[i]["children"][j]['children'])==0:
                    innerchild=gJsonList[i]['children'][j]['children']
                    for k in range(len(gJsonList[i]['children'][j]['children'])):
                        line=(str(innerchild[k]['id'])
                        +'\t'+str(innerchild[k]['name'])
                        +'\t'+str(innerchild[k]['description'])
                        +'\t'+str(innerchild[k]['parent'])
                        +'\t'+str(innerchild[k]['read_only']))+'\n'
                        elementList.append(line)
                        if not len(gJsonList[i]["children"][j]['children'][k]['children'])==0:
                            innerchild=gJsonList[i]['children'][j]['children'][k]['children']
                            for l in range(len(gJsonList[i]['children'][j]['children'][k]['children'])):
                                line=(str(innerchild[l]['id'])
                                +'\t'+str(innerchild[l]['name'])
                                +'\t'+str(innerchild[l]['description'])
                                +'\t'+str(innerchild[l]['parent'])
                                +'\t'+str(innerchild[l]['read_only']))+'\n'
                                elementList.append(line)
    file2write.writelines(elementList)
    file2write.close()