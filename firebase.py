import firebase_admin
from firebase_admin import credentials,firestore
from firebase_admin import db
import pickle


# Fetch the service account key JSON file contents
cred = credentials.Certificate('sham-a9d95-firebase-adminsdk-aj0h6-fdddc99699.json')

# Initialize the app with a None auth variable, limiting the server's access
firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sham-a9d95.firebaseio.com/',
        'databaseAuthVariableOverride': None
    })


def addstudent(name,rollno):

    try:
        open("data.pickle",'rb')

    except:
        fileObj = open("data.pickle", 'wb')
        pickle.dump({}, fileObj)
        fileObj.close()

    fileObj = open("data.pickle", 'rb')
    names_existing = pickle.load(fileObj)
    names_existing[rollno] = name
    fileObj.close()

    fileObj = open("data.pickle", 'wb')
    pickle.dump(names_existing,fileObj)

    root = db.reference()
    new_user = root.child('Students').update({
        rollno: name,
    })
    print(names_existing)





def Firebase_Read():
    root = db.reference('attendance')

    snapshot = root.get()
    #print(snapshot)
    return snapshot

def Total_held(h):

    root = db.reference()
    try:
        fb_attdb = root.order_by_child('attendance').get()['attendance']['Total Held']
    except:
        fb_attdb = {}
    for key in h:
        if h[key] in fb_attdb:
            print(key)
            fb_attdb[key] = fb_attdb[key] + h[key]
        else:
            fb_attdb[key] = h[key]
    #print(fb_attdb)
    #print(h)
    att = root.child('attendance').child('Total Held').set(fb_attdb)


#attendance updation
def Firebase_attendance(a):

    root = db.reference()
    try:
        fb_attdb=root.order_by_child('attendance').get()['attendance']
    except:
        fb_attdb={}

    #print(fb_attdb)

#adding new attendance to attendance in firebase
    for name in a:
        if name in fb_attdb:
            for date in a[name]:
                label : date
                if date in fb_attdb[name]:
                    for hh in a[name][date]:
                        fb_attdb[name][date].update({hh:a[name][date][hh]})
                else:
                    fb_attdb[name][date] = {}
                    for hh in a[name][date]:
                        fb_attdb[name][date].update({hh:a[name][date][hh]})
        else:
            fb_attdb[name]={}
            for date in a[name]:
                label : date
                if date in fb_attdb[name]:
                    for hh in a[name][date]:
                        fb_attdb[name][date].update({hh:a[name][date][hh]})
                else:
                    fb_attdb[name][date] = {}
                    for hh in a[name][date]:
                        fb_attdb[name][date].update({hh:a[name][date][hh]})



    #print(fb_attdb)
    print("sucessfully uploaded to database")
    att = root.child('attendance').set(fb_attdb)
    #att = root.child('attendance').update(a)