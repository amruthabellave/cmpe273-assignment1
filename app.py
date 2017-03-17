from github import Github
import sys
import base64
import yaml
import json
from flask import Flask
from flask import jsonify


app = Flask(__name__)

@app.route('/v1/<filename>')
def isConfig(filename):
    g= Github()
    url = sys.argv[1].split("/")
    try:
        user = g.get_user(url[3])
    except:
        return "Github user not found"
    else:
        try:
            repo = user.get_repo(url[4])
       
        except:
            return "Repository not found"
        else:
            files = repo.get_contents('/')
            for i in files:
                gitfile = str(i.name)
                if(gitfile==filename):
                    temp = gitfile.split('.')
                    file_type = temp[1]
                    if(file_type == 'yml'):
                        file_contents = yaml.load(i.content.decode('base64'))
                        return yaml.dump(file_contents,default_flow_style=False)
                    elif(file_type == 'json'):
                        file_contents = json.loads(i.content.decode('base64'))
                        response = app.response_class(response=json.dumps(file_contents),status=200,mimetype='application/json')
                        return response 
                    else :
                        return i.content.decode('base64')

            return "File not found"


    
    

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')



