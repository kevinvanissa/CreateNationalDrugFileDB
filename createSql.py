fo = open("missing.txt","r")
#fw = open("createSql.sql","w")

for l in fo:
    #print s[0]
    #print  l[11:]
    #print  l[:11]
    print "insert into Drug values(\"%s\",\"%s\");" % (l[:11],l[11:].lstrip())
    #fw.write(l,)

fo.close()
#fw.close()

