
import requests
import webbrowser
import os

IP = '127.0.0.1'
PORT = '8000'
SIZE = 'leaderboard'
KEY = 'P53ZD2pSaQdg43oWK1Fuop2VIysPO9p0'
KEY = 'fqXKaCiNoSksZE8ZqoZpvsMiPLMfwWWM'
FILENAME = 'ad_adv.html'
"""
url link: https://<domain-name>/adv-api/
"""

data = {
    'key': KEY
}

r = requests.post(f"http://{IP}:{PORT}/adv-api/", data=data)
r = r.json()
print(r)

html = \
"""
<div id="ad-holder"></div>
<button onclick="foo()">Click Me</button>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
<script type="text/javascript">
function foo() {
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/adv-api/',
        dataType:'jsonp',
        crossDomain: true,
        data: {
                 temp_key: '""" + str(r['temporary-key']) + """',
                 size: 'leaderboard'
        },
        success: function( data ) 
        {
            alert('working');
            console.log(data);
            $('#ad-holder').innerhtml = data;
        },
    });
}
</script>"""

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILENAME)
with open(path, "w") as f:
    f.write(html)
webbrowser.open(path, new=2)
