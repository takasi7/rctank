#! /usr/bin/python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from tank import Tank
from urllib.parse import urlparse

rctank = Tank()

htmltemplate = '''<html>
<head>
<title>RC TANK TA7291P</title>
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<script>
function btnact(id) {
	var obj = document.getElementById("cmd");
	var objfm = document.getElementById("tankaction");
	obj.value = id;
	objfm.submit();
}

function tankspeed(speed) {
	var obj = document.getElementById("speed");
	var objfm = document.getElementById("tankaction");
	obj.value = speed;
	objfm.submit();
}

</script>
</head>
<body>
<table>
<tr>
	<td></td>
	<td><input type="button" value="forward" id="forward" onclick="btnact(this.id)"></td>
	<td></td>
</tr>
<tr>
	<td><input type="button" value="left" id="leftturn" onclick="btnact(this.id)"></td>
	<td><input type="button" value="stop" id="brake" onclick="btnact(this.id)"></td>
	<td><input type="button" value="right" id="rightturn" onclick="btnact(this.id)"></td>
</tr>

<tr>
	<td></td>
	<td><input type="button" value="back" id="back" onclick="btnact(this.id)"></td>
	<td></td>
</tr>
</table>
<div>
<input type="radio" name="speed" onclick="tankspeed(50)" __50__ /><label>1  </label>
<input type="radio" name="speed" onclick="tankspeed(60)" __60__ /><label>2  </label>
<input type="radio" name="speed" onclick="tankspeed(70)" __70__ /><label>3  </label>
<input type="radio" name="speed" onclick="tankspeed(80)" __80__ /><label>4  </label>
<input type="radio" name="speed" onclick="tankspeed(90)" __90__ /><label>5  </label>
<input type="radio" name="speed" onclick="tankspeed(100)" __100__  /><label>MAX</label>
</div>
<form id="tankaction" action="index.html" method="get" enctype="application/x-www-form-urlencoded">
<input type="hidden" name="cmd" value="None" id="cmd">
<input type="hidden" name="speed" value="__SPEED__" id="speed">
</form>
</body>
</html>'''

class HelloHandler(BaseHTTPRequestHandler):
	def parse_query(self):
		query = urlparse(self.path).query
		querylist = query.split("&")
		query_components = {}
		
		for item in querylist:
			q = item.split("=")
			if len(q) == 2:
				query_components[q[0]] = q[1]
		
		return query_components

	def action_tank(self,qc):
		global rctank
		if 'cmd' in qc:
			cmd = qc['cmd']
			if cmd == 'forward':
				rctank.forward()
			elif cmd == 'back':
				rctank.back()
			elif cmd == 'leftturn':
				rctank.leftturn()
			elif cmd == 'rightturn':
				rctank.rightturn()
			elif cmd == 'brake':
				rctank.brake()
			elif cmd == 'acceloff':
				rctank.acceloff()

		if 'speed' in qc:
			try:
				sp = int(qc['speed'])
			except:
				return -1
			if sp >= 50 and sp <= 100 and sp != rctank.speed:
				rctank.setspeed(sp)
				
		return 0

	def gen_html(self,qc):
		global htmltemplate
		global rctank
		html = htmltemplate
		html = html.replace('__SPEED__',str(rctank.speed))
		chtag = "__"+str(rctank.speed)+"__"
		html = html.replace(chtag, "checked")
		for s in range(50,110,10):
			s = '__'+str(s)+'__'
			html = html.replace(s,'')
		return html
	
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html; charset=utf-8')
		self.end_headers()
		
		qc = self.parse_query()
		self.action_tank(qc)
		html = self.gen_html(qc)
		self.wfile.write(html.encode())



if __name__ == '__main__':
	server_address = ('', 8000)
	httpd = HTTPServer(server_address, HelloHandler)
	httpd.serve_forever()

