import re
import pymongo
import bson
from tqdm import tqdm
from bson.json_util import dumps

uri = "env.URI"

client = pymongo.MongoClient(uri, connectTimeoutMS=200, retryWrites=True)
print(client)
print(client.list_database_names())
pa3 = client.pa3
apidb = pa3['apidb']
mashupdb = pa3['mashupdb']
# print(pa3.list_collection_names())


def data_loading():
    files = input("enter data file")
    files = 'data\\' + files
    # print(files)

    with open(files) as f:
        line = []
        for lines in tqdm(f):
            # print(lines.split('$#$'))
            temp = lines.split('$#$')
            tags = temp[17].split('###')
            # print(len(temp))
    #         print(tags)
            updatedYear = temp[45][:4]
            # print(updatedYear)
            document = {"id":temp[0],"title":temp[1],"summary":temp[2],"rating":temp[3],"name":temp[4],"label":temp[5],
             "author":temp[6],"description":temp[7],"type":temp[8],"downloads":temp[9],"useCounts":temp[10],
             "sampleUrl":temp[11],"downloadUrl":temp[12],"dateModified":temp[13],"remoteFeed":temp[14],
             "numComments":temp[15],"commentsUrl":temp[16],"tags":tags,"category":temp[18],"protocols":temp[19],
            "serviceEndpoint":temp[20],"version":temp[21],"wsdl":temp[22],"dataFormats":temp[23],"apigroups":temp[24],
             "example":temp[25],"clientInstall":temp[26],"authentication":temp[27],"ssl":temp[28],"readonly":temp[29],
             "VendorApiKits":temp[30],"CommunityApiKits":temp[31],"blog":temp[32],"forum":temp[33],"support":temp[34],
             "accountReq":temp[35],"commercial":temp[36],"provider":temp[37],"managedBy":temp[38],"nonCommercial":temp[39],
            "dataLicensing":temp[40],"fees":temp[41],"limits":temp[42],"terms":temp[43],"company":temp[44],
            "updated":updatedYear}
            # print(document)
            pa3.apidb.insert_one(document)
        print()
        print("Finished loading API.txt")

    #
    files2 = input("enter mashup data file")
    files2 = 'data\\' + files2



    with open(files2) as f:
        line = []
        for lines in tqdm(f):
            # print(lines.split('$#$'))
            temp = lines.split('$#$')
            tags = temp[15].split('###')
            updatedYear2 = temp[17][:4]
            # print(len(temp))
            # print(tags)
            urldict={}
            if len(temp[16])<1:
                urls=''
            elif "###" in temp[16]:
                urls = temp[16].split("###")
                for i in urls:
                    api_url = i.split("$$$")
                    urldict[api_url[0]] = api_url[1]
            else:
                urls = temp[16].split("$$$")
                urldict[urls[0]] = urls[1]

            document = {"id":temp[0],"title":temp[1],"summary":temp[2],"rating":temp[3],"name":temp[4],"label":temp[5],
                      "author":temp[6],"description":temp[7],"type":temp[8],"downloads":temp[9],"useCount":temp[10],
                      "sampleUrl":temp[11],"dateModified":temp[12],"numComments":temp[13],"commentsUrl":temp[14],
                      "tags":tags,"API":bson.BSON.encode(urldict),"updated":updatedYear2}

            pa3.mashupdb.insert_one(document,bypass_document_validation=True)
        print("Finished loading mashup.txt")
        print(pa3.list_collection_names())
#
# # data = bson.BSON.encode({'a': 1})
# # decoded_doc = bson.BSON(data).decode()
#
# # options = CodecOptions(document_class=collections.OrderedDict)
# # decoded_doc = bson.BSON(data).decode(codec_options=options)
# # type(decoded_doc)

data_loading()


apidb.create_index([("title",1)])
apidb.create_index([("summary",1)])
apidb.create_index([("description",1)])

mashupdb.create_index([("title",1)])
mashupdb.create_index([("summary",1)])
mashupdb.create_index([("description",1)])

# apidb.create_index([("title",1),("summary",1),("description",1)])
# mashupdb.create_index([("title",1),("summary",1),("description",1)])
