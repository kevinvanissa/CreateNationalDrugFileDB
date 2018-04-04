import urllib2
import xml.etree.ElementTree as et

import myconnection
mydb = myconnection.DBconnection()
globalcursor = mydb.getCursor()
globaldb  = mydb.getConnection()

#===========================Function Definitions==============

def getConceptNUI(conceptname):
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/search?conceptName=%s&kindName=DRUG_KIND' % conceptname
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    groupconcepts = raw_data.find("groupConcepts")
    concepts = groupconcepts.findall("concept")
    for c in concepts:
            print c.find("conceptNui").text

def populateDrugInteraction(cursor,db,tablename):
    query =  "select * from Interaction"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print row[1].split("/")

    except mydb.getErrorHandler(), e:
        db.rollback()
        print "ERROR:Could Not Enter %s " % tablename
        print "Error %d: %s" % (e.args[0], e.args[1])


def getInteractionsPopulate(cursor,db):
    query = "select * from Drug where drug_code > 'N0000178420' "
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            url='http://rxnav.nlm.nih.gov/REST/Ndfrt/interaction/nui=%s&scope=2' %  row[0]
            response = urllib2.urlopen(url)
            raw_data = et.fromstring(response.read().decode('utf8'))
            groupconcepts = raw_data.find("groupInteractions")
            concepts = groupconcepts.find("interactions")
            if not concepts:
                continue
            idrugs  = concepts.find("groupInteractingDrugs")
            alldrugs = idrugs.findall("interactingDrug")

            for c in alldrugs:
                query2 = "insert into DrugInteraction values(\"%s\",\"%s\",\"%s\")" % (row[0],c.find("concept").find("conceptNui").text,c.find("severity").text)
                #print c.find("concept").find("conceptName").text
                #print c.find("concept").find("conceptNui").text
                #print c.find("severity").text
                try:
                    cursor.execute(query2)
                    db.commit()
                    print "Successfully Entered"
                except mydb.getErrorHandler(), e:
                    db.rollback()
                    print "ERROR:Could Not Enter in DrugInteraction"
                    print "Error %d: %s" % (e.args[0], e.args[1])
    except mydb.getErrorHandler(), e:
        db.rollback()
        print "ERROR:Could Not fetch from Interaction"
        print "Error %d: %s" % (e.args[0], e.args[1])


def generalPopulate(cursor,db,tablename,conceptnui,conceptname):
    query="insert into %s values(\"%s\",\"%s\")" % (tablename, conceptnui,conceptname)
    try:
        cursor.execute(query)
        db.commit()
        print "Successfully Entered"
    except mydb.getErrorHandler(), e:
        db.rollback()
        print "ERROR:Could Not Enter %s ===> %s , %s" % (tablename,conceptnui, conceptname)
        print "Error %d: %s" % (e.args[0], e.args[1])


def populateDrug(cursor,db,conceptnui,conceptname):
    query="insert into Drug values(\"%s\",\"%s\")" % (conceptnui,conceptname)
    try:
        cursor.execute(query)
        db.commit()
        print "Successfully Entered"
    except mydb.getErrorHandler(), e:
        db.rollback()
        print "ERROR:Could Not Enter Drug ===> %s , %s" % (conceptnui, conceptname)
        print "Error %d: %s" % (e.args[0], e.args[1])

def populateDiagnosis(cursor,db,conceptnui,conceptname):
    query="insert into Diagnosis values(\"%s\",\"%s\")" % (conceptnui,conceptname)
    try:
        cursor.execute(query)
        db.commit()
        print "Successfully Entered"
    except mydb.getErrorHandler(), e:
        db.rollback()
        print "ERROR:Could Not Enter Diagnosis ===> %s , %s" % (conceptnui, conceptname)
        print "Error %d: %s" % (e.args[0], e.args[1])

def drugsWhichMayTreat(conceptnui):
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/reverse/nui=%s&roleName=may_treat&transitive=false' % conceptnui
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    groupconcepts = raw_data.find("groupConcepts")
    concepts = groupconcepts.findall("concept")
    for c in concepts:
            print c.find("conceptName").text
            print c.find("conceptNui").text

def drugsWhichMayTreatPopulate(cursor,db):
    query = "select * from Diagnosis"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            url='http://rxnav.nlm.nih.gov/REST/Ndfrt/reverse/nui=%s&roleName=may_treat&transitive=false' % row[0]
            response = urllib2.urlopen(url)
            raw_data = et.fromstring(response.read().decode('utf8'))
            groupconcepts = raw_data.find("groupConcepts")
            if not groupconcepts:
                continue
            concepts = groupconcepts.findall("concept")
            for c in concepts:
                query2 = "insert into IndicationUsage values(\"%s\",\"%s\")" % (row[0],c.find("conceptNui").text)
                try:
                    cursor.execute(query2)
                    db.commit()
                    print "Successfully Entered"
                except mydb.getErrorHandler(), e:
                    db.rollback()
                    print "ERROR:Could Not Enter in IndicationUsage"
                    print "Error %d: %s" % (e.args[0], e.args[1])
    except mydb.getErrorHandler(), e:
        db.rollback()
        print "ERROR:Could Not fetch from Diagnosis"
        print "Error %d: %s" % (e.args[0], e.args[1])


def drugCI_withDiseasePopulate(cursor,db):
    query = "select * from Diagnosis"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            url='http://rxnav.nlm.nih.gov/REST/Ndfrt/reverse/nui=%s&roleName=CI_with&transitive=false' % row[0]
            response = urllib2.urlopen(url)
            raw_data = et.fromstring(response.read().decode('utf8'))
            groupconcepts = raw_data.find("groupConcepts")
            if not groupconcepts:
                continue
            concepts = groupconcepts.findall("concept")
            for c in concepts:
                query2 = "insert into ContraIndication values(\"%s\",\"%s\")" % (row[0],c.find("conceptNui").text)
                try:
                    cursor.execute(query2)
                    db.commit()
                    print "Successfully Entered"
                except mydb.getErrorHandler(), e:
                    db.rollback()
                    print "ERROR:Could Not Enter in ContraIndication"
                    print "Error %d: %s" % (e.args[0], e.args[1])
    except mydb.getErrorHandler(), e:
        db.rollback()
        print "ERROR:Could Not fetch from Diagnosis"
        print "Error %d: %s" % (e.args[0], e.args[1])



def ingredientInDrugPopulate(cursor,db):
    query = "select * from Ingredient"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            url='http://rxnav.nlm.nih.gov/REST/Ndfrt/reverse/nui=%s&roleName=has_ingredient&transitive=false' % row[0]
            response = urllib2.urlopen(url)
            raw_data = et.fromstring(response.read().decode('utf8'))
            groupconcepts = raw_data.find("groupConcepts")
            if not groupconcepts:
                continue
            concepts = groupconcepts.findall("concept")
            for c in concepts:
                query2 = "insert into IngredientInDrugs values(\"%s\",\"%s\")" % (row[0],c.find("conceptNui").text)
                try:
                    cursor.execute(query2)
                    db.commit()
                    print "Successfully Entered"
                except mydb.getErrorHandler(), e:
                    db.rollback()
                    print "ERROR:Could Not Enter in IngredientInDrugs"
                    print "Error %d: %s" % (e.args[0], e.args[1])
    except mydb.getErrorHandler(), e:
        db.rollback()
        print "ERROR:Could Not fetch from Ingredient"
        print "Error %d: %s" % (e.args[0], e.args[1])

#===============================GENERAL DRUG POPULATE======================
def GeneralDrugPopulate(cursor,db,table1,table2,role):
    query = "select * from %s" % table1
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            url='http://rxnav.nlm.nih.gov/REST/Ndfrt/reverse/nui=%s&roleName=%s&transitive=false' % (row[0],role)
            response = urllib2.urlopen(url)
            raw_data = et.fromstring(response.read().decode('utf8'))
            groupconcepts = raw_data.find("groupConcepts")
            if not groupconcepts:
                continue
            concepts = groupconcepts.findall("concept")
            for c in concepts:
                query2 = "insert into %s values(\"%s\",\"%s\")" % (table2,row[0],c.find("conceptNui").text)
                try:
                    cursor.execute(query2)
                    db.commit()
                    print "Successfully Entered"
                except mydb.getErrorHandler(), e:
                    db.rollback()
                    print "ERROR:Could Not Enter in %s" % table2
                    print "Error %d: %s" % (e.args[0], e.args[1])
    except mydb.getErrorHandler(), e:
        db.rollback()
        print "ERROR:Could Not fetch from %s" % table1
        print "Error %d: %s" % (e.args[0], e.args[1])

#===============================END GENERAL DRUG POPULATE======================


def diseasesTreatedByDrug(conceptnui):
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/nui=%s&roleName=may_treat&transitive=false' % conceptnui
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    groupconcepts = raw_data.find("groupConcepts")
    concepts = groupconcepts.findall("concept")
    for c in concepts:
            print c.find("conceptName").text
            print c.find("conceptNui").text


def diseasesCI_withDrug(conceptnui):
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/nui=%s&roleName=CI_with&transitive=false' % conceptnui
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    groupconcepts = raw_data.find("groupConcepts")
    concepts = groupconcepts.findall("concept")
    for c in concepts:
            print c.find("conceptName").text
            print c.find("conceptNui").text


def ingredientDrugContains(conceptnui):
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/nui=%s&roleName=has_ingredient&transitive=false' % conceptnui
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    groupconcepts = raw_data.find("groupConcepts")
    concepts = groupconcepts.findall("concept")
    for c in concepts:
            print c.find("conceptName").text
            print c.find("conceptNui").text

#=====================End Function Definitions=====================

if False:
    #============================================================
    #url = 'http://api.decibel.net/v1/Albums/?artist=miles%20davis&format=xml'
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/kindList'
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    #namespace = '{http://rxnav.nlm.nih.gov/ndfrtrest.xsd}'
    kindlist = raw_data.find("kindList")
    kindnames = kindlist.findall("kindName")
    for k in kindnames:
        print k.text
    #==========================================================

if False:
    #============================================================
    #url = 'http://api.decibel.net/v1/Albums/?artist=miles%20davis&format=xml'
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/roleList'
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    #namespace = '{http://rxnav.nlm.nih.gov/ndfrtrest.xsd}'
    rolelist = raw_data.find("roleList")
    rolenames = rolelist.findall("roleName")
    for r in rolenames:
        print r.text
    #==========================================================


if False:
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/allconcepts?kind=disease_kind'
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    #namespace = '{http://rxnav.nlm.nih.gov/ndfrtrest.xsd}'
    grouplist = raw_data.find("groupConcepts")
    concepts = grouplist.findall("concept")
    for c in concepts:
        #print c.find("conceptName").text
        #print c.find("conceptNui").text
        populateDiagnosis(globalcursor,globaldb,c.find("conceptNui").text,c.find("conceptName").text)



if False:
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/allconcepts?kind=drug_kind'
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    #namespace = '{http://rxnav.nlm.nih.gov/ndfrtrest.xsd}'
    grouplist = raw_data.find("groupConcepts")
    concepts = grouplist.findall("concept")
    for c in concepts:
        #print c.find("conceptName").text
        conceptN = c.find("conceptName").text
        conceptI =  c.find("conceptNui").text
        if "'" in conceptN:
            print "%s  %s" % (conceptI,conceptN)
        #print c.find("conceptNui").text
        #populateDrug(globalcursor,globaldb,c.find("conceptNui").text,c.find("conceptName").text)



if False:
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/allconcepts?kind=dose_form_kind'
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    #namespace = '{http://rxnav.nlm.nih.gov/ndfrtrest.xsd}'
    grouplist = raw_data.find("groupConcepts")
    concepts = grouplist.findall("concept")
    for c in concepts:
        #print c.find("conceptName").text
        #print c.find("conceptName").text
        generalPopulate(globalcursor,globaldb,'DrugForm',c.find("conceptNui").text,c.find("conceptName").text)


#retunrs string separted by / in concept name
if False:
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/allconcepts?kind=drug_interaction_kind'
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    #namespace = '{http://rxnav.nlm.nih.gov/ndfrtrest.xsd}'
    grouplist = raw_data.find("groupConcepts")
    concepts = grouplist.findall("concept")
    for c in concepts:
        #print c.find("conceptName").text
        #print c.find("conceptNui").text
        generalPopulate(globalcursor,globaldb,'DrugInteraction',c.find("conceptNui").text,c.find("conceptName").text)


if False:
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/allconcepts?kind=ingredient_kind'
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    #namespace = '{http://rxnav.nlm.nih.gov/ndfrtrest.xsd}'
    grouplist = raw_data.find("groupConcepts")
    concepts = grouplist.findall("concept")
    for c in concepts:
        #print c.find("conceptName").text
        #print c.find("conceptNui").text
        generalPopulate(globalcursor,globaldb,'Ingredient',c.find("conceptNui").text,c.find("conceptName").text)


if False:
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/allconcepts?kind=mechanism_of_action_kind'
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    #namespace = '{http://rxnav.nlm.nih.gov/ndfrtrest.xsd}'
    grouplist = raw_data.find("groupConcepts")
    concepts = grouplist.findall("concept")
    for c in concepts:
        #print c.find("conceptName").text
        #print c.find("conceptNui").text
        generalPopulate(globalcursor,globaldb,'MechanismAction',c.find("conceptNui").text,c.find("conceptName").text)


if False:
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/allconcepts?kind=pharmacokinetics_kind'
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    #namespace = '{http://rxnav.nlm.nih.gov/ndfrtrest.xsd}'
    grouplist = raw_data.find("groupConcepts")
    concepts = grouplist.findall("concept")
    for c in concepts:
        #print c.find("conceptName").text
        #print c.find("conceptNui").text
        generalPopulate(globalcursor,globaldb,'PharmacoKinetics',c.find("conceptNui").text,c.find("conceptName").text)


if False:
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/allconcepts?kind=physiologic_effect_kind'
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    #namespace = '{http://rxnav.nlm.nih.gov/ndfrtrest.xsd}'
    grouplist = raw_data.find("groupConcepts")
    concepts = grouplist.findall("concept")
    for c in concepts:
        #print c.find("conceptName").text
        #print c.find("conceptNui").text
        generalPopulate(globalcursor,globaldb,'PhysiologicEffect',c.find("conceptNui").text,c.find("conceptName").text)


if False:
    url='http://rxnav.nlm.nih.gov/REST/Ndfrt/allconcepts?kind=therapeutic_category_kind'
    response = urllib2.urlopen(url)
    raw_data = et.fromstring(response.read().decode('utf8'))
    #namespace = '{http://rxnav.nlm.nih.gov/ndfrtrest.xsd}'
    grouplist = raw_data.find("groupConcepts")
    concepts = grouplist.findall("concept")
    for c in concepts:
        #print c.find("conceptName").text
        #print c.find("conceptNui").text
        generalPopulate(globalcursor,globaldb,'TherapeuticCategory',c.find("conceptNui").text,c.find("conceptName").text)

#====================Examples of function usage=====================
#drugsWhichMayTreat('N0000000478')
#diseasesTreatedByDrug('N0000145914')
#diseasesCI_withDrug('N0000148590')
#ingredientDrugContains('N0000145914')
#getConceptNUI('morphine')
#getInteractionsPopulate(globalcursor,globaldb)
#drugsWhichMayTreatPopulate(globalcursor,globaldb)
#drugCI_withDiseasePopulate(globalcursor,globaldb)
#ingredientInDrugPopulate(globalcursor,globaldb)
#GeneralDrugPopulate(globalcursor,globaldb,'MechanismAction','MechanismActionInDrugs','has_MoA')
#GeneralDrugPopulate(globalcursor,globaldb,'PharmacoKinetics','PharmacoKineticsInDrugs','has_PK')
#GeneralDrugPopulate(globalcursor,globaldb,'PhysiologicEffect','PhysiologicEffectInDrugs','has_PE')
#GeneralDrugPopulate(globalcursor,globaldb,'TherapeuticCategory','TherapeuticCategoryInDrugs','has_TC')



