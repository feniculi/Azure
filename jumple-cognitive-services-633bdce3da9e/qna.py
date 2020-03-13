#python
import http.client, urllib.request, urllib.parse, urllib.error, base64
import re, json

# NOTE: Replace this with a valid host name.
host_qna = "testqnamakercesare.azurewebsites.net"
# To get your endpoint keys, call the GET /endpointkeys method.
endpoint_key_qna = " c28396c7-391f-4df8-b26d-fe47aaee13a3"
# POST /knowledgebases/{knowledge base ID} method.
kb_qna = "6e623c34-c942-40db-b222-ec8eb37ff244"

class qna:
    def get_answers (content, n_ans):
        path = "/qnamaker/knowledgebases/" + kb_qna + "/generateAnswer"
        question = {
            'question': content,
            'top': n_ans
        }
        content=json.dumps(question)
        headers = {
            'Authorization': 'EndpointKey ' + endpoint_key_qna,
            'Content-Type': 'application/json',
            'Content-Length': len (content)
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection(host_qna)
            conn.request("POST", "/qnamaker/knowledgebases/" + kb_qna + "/generateAnswer?%s" % params, content, headers)
            response = conn.getresponse()
            str_response = response.read().decode('utf-8')
            obj = json.loads(str_response)
            conn.close()
            return obj

        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
