#! /usr/bin/python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from tank import Tank
from urllib.parse import urlparse

rctank = Tank()

htmltemplate = '<html><head></head><body>Hello,World</body></html>'

def load_template():
	global htmltemplate
	try:
		f = open('/home/pi/TA7291P/template.html')
	except:
		return
	htmltemplate = f.read()
	f.close()
	return


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
	def state2cmd(self,state):
		command = 'None'
		if state == 0:
			command = 'brake'
		elif state == 1:
			command = 'acceloff'
		elif state == 2:
			command = 'forward'
		elif state == 3:
			command = 'rightturn'
		elif state == 4:
			command = 'back'
		elif state == 5:
			command = 'leftturn'
		return command
	def gen_html(self,qc):
		global htmltemplate
		global rctank
		html = htmltemplate
		html = html.replace('__SPEED__',str(rctank.speed))
		html = html.replace('__COMMAND__', self.state2cmd(rctank.state))
		#chtag = "__"+str(rctank.speed)+"__"
		#html = html.replace(chtag, "checked")
		#for s in range(50,110,10):
		#	s = '__'+str(s)+'__'
		#	html = html.replace(s,'')
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
	load_template()
	server_address = ('', 8000)
	httpd = HTTPServer(server_address, HelloHandler)
	httpd.serve_forever()

