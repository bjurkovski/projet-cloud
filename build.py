import os
import shutil
#from subprocess import call
import commands

GAE_DIR = "../../google_appengine/"
BUILD_DIR = ".build"
BUILD_FOLDERS = ["pages", "static", "gdata", "atom"]
BUILD_FILES = ["app.yaml", "facebook.yaml", "projet-cloud.py", "managers.py", "deezerExtractor.py",
				"facebookExtractor.py", "youtubeExtractor.py", "dataMapper.py", "models.py", "facebook.py", "yuicompressor-2.4.2.jar"]

if __name__ == "__main__":
	if GAE_DIR[-1] != "/": GAE_DIR += "/"
	if BUILD_DIR[-1] != "/": BUILD_DIR += "/"

	try: shutil.rmtree(BUILD_DIR)
	except OSError: pass
	os.mkdir(BUILD_DIR)

	for f in BUILD_FILES:
		if f.endswith(".yaml"):	 shutil.copyfile(f + ".build", BUILD_DIR + f)
		else: shutil.copyfile(f, BUILD_DIR + f)

	for f in BUILD_FOLDERS:
		shutil.copytree(f, BUILD_DIR + f)

	shutil.copyfile("static/js/facebook.js.build", BUILD_DIR + "static/js/facebook.js")
	commands.getoutput("rm " + BUILD_DIR + "static/js/facebook.js.build")
	commands.getoutput("java -jar yuicompressor-2.4.2.jar --type js static/js/script.js > " + BUILD_DIR + "static/js/script.js")
	commands.getoutput("java -jar yuicompressor-2.4.2.jar --type css static/css/style.css > " + BUILD_DIR + "static/css/style.css")
	#print commands.getoutput(GAE_DIR + "appcfg.py update " + BUILD_DIR)
