import myconnection
mydb = myconnection.DBconnection()
globalcursor = mydb.getCursor()
globaldb  = mydb.getConnection()


def createStrings(cursor,db,tablename,column1,column2):
    query="select %s,%s from %s" % (column2, column1, tablename)
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print "\"%s--%s\"," % (row[0],row[1])

    except mydb.getErrorHandler(), e:
        db.rollback()
        print "ERROR:Could Not query %s " % tablename
        print "Error %d: %s" % (e.args[0], e.args[1])

#createStrings(globalcursor,globaldb,"MechanismAction","mechanism_code","mechanism_type_name")
#createStrings(globalcursor,globaldb,"PharmacoKinetics","pharmaco_code","pharmaco_type_name")
#createStrings(globalcursor,globaldb,"PhysiologicEffect","physiologic_code","physiologic_type_name")
#createStrings(globalcursor,globaldb,"TherapeuticCategory","therapeutic_code","therapeutic_type_name")

