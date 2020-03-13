import httplib, urllib,json
import re

# NOTE: Replace this with a valid host name.
host = "testqnamakercesare.azurewebsites.net"

# To get your endpoint keys, call the GET /endpointkeys method.
endpoint_key = " c28396c7-391f-4df8-b26d-fe47aaee13a3"

# POST /knowledgebases/{knowledge base ID} method.
kb = "6e623c34-c942-40db-b222-ec8eb37ff244"

class qna:
    def get_answers (content, n_ans):
        path = "/qnamaker/knowledgebases/" + kb + "/generateAnswer"
        question = {
            'question': content,
            'top': n_ans
        }
        content=json.dumps(question)
        print ('Calling ' + host + path + '.')
        headers = {
            'Authorization': 'EndpointKey ' + endpoint_key,
            'Content-Type': 'application/json',
            'Content-Length': len (content)
        }
        conn = httplib.HTTPSConnection(host)#conn = http.client.HTTPSConnection(host)
        conn.request ("POST", path, content, headers)
        response = conn.getresponse ()
        str_response = response.read().decode('utf-8')
        obj = json.loads(str_response)
        return obj
