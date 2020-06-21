
class CommandLineSwitches:

	def parse(self, args):
		self.minMode=False
		self.develMode=False
		self.noSend=False
		
		if len(args)>1:
			for arg in args[1:]:
				if arg.lower()=="-devel":
					self.develMode=True
					print("Development mode enabled.")
				if arg.lower()=="-min":
					self.minMode=True
					print("Minimum display size mode enabled.")
				if arg.lower()=="-nosend":
					self.noSend=True
					print("Will not send any GET requests for this session.")