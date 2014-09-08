#!/usr/bin/env python
import pickle
import os.path
from flask import Flask
from flask import request


app = Flask(__name__)

'''domainDict, key is the name, value is the (url, tags)'''
domainDict = {}

@app.route('/add')
def add():
    return """
    <form name="myform" onsubmit="return save_url();">
    <div id="keydiv">
	<label style="width:40px">    	  key:    	</label>
	<input type="text" id = "key" style="width:1024px;height:40px;"> 	</input> <p>
    </div>
    <div>
    	<label  style="width:40px">url&nbsp :    	</label>
    	<input type="text" id = "url" style="width:1024px;height:40px;"> 	</input> <p>
        
    	<label  style="width:40px">tags:    	</label>
    	<input type="text" id = "tags" style="width:1024px;height:40px;"> 	</input>
    
    	<label>
    	  <button id="save">Save</button>
    	</label>
    </div>
    <script language = "javaScript" >
        function attach_params(form, params){
            for(var key in params) {
                    if(params.hasOwnProperty(key)) {
                        var hiddenField = document.createElement("input");
                        hiddenField.setAttribute("type", "hidden");
                        hiddenField.setAttribute("name", key);
                        hiddenField.setAttribute("value", params[key]);

                        form.appendChild(hiddenField);
                     }
                }
        }
        function save_url(){
            key   = document.getElementById('key').value;
            url   = document.getElementById('url').value;
            tags   = document.getElementById('tags').value;
            alert(key);
            document.myform.action ="/save";
            attach_params(document.myform, {key: key,url:url,tags:tags});
        }
        
        //document.getElementById('save').addEventListener('click',save_url);
    </script>
    </form>
    """

def save(key,url,tags):
    global domainDict
    if(not domainDict and os.path.isfile('./dict')):
        init()
    domainDict[key] = (url,tags)
    with open('./dict','w') as fi:
        pickle.dump(domainDict,fi)

def init():
    global domainDict
    with open('./dict','r') as fi:
        domainDict = pickle.load(fi)
    print('pickled')

@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    global domainDict
    message = ''
    if(path=='save'):
        key = request.args.get("key")
        url = request.args.get("url")
        tags = request.args.get("tags")
        save(key,url,tags)
    elif (not domainDict and os.path.isfile('./dict')):
        init()
    for key,valuetags in domainDict.items():
        message = ('%s <font size="10px"> <a href="%s" target="_blank">%s</a>, tags:%s </font><p>' % (message, valuetags[0], key, valuetags[1])  );
        
    message = '%s <hr><p> add new website to the list: <a href="/add">new website</a>' % message
    return message
    
if __name__ == '__main__':
    app.run(debug = True)
