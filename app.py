from flask import Flask, request, render_template
app = Flask(__name__)
app.static_folder='static'

equality = {'Ab':'B#', 'B#':'C', 'C#':'Db', 'D#':'Eb', 'E#':'F', 'F#':'Gb', 'G#':'Ab'}
chords = ['Ab','A','Bb','B','C','Db','D','Eb','E','F','Gb','G']
posn = {}
for i in range(len(chords)):
	posn[chords[i]]=i
for chord in list(equality):
	equality[equality[chord]] = chord

@app.route("/")
def converter():
	return render_template("converter.html", value="Input chords here.")

@app.route('/transpose', methods=["POST"])
def transpose():
	half_steps = request.form['submit_button']
	print(half_steps)
	text = request.form['text']
	return render_template("converter.html", value=text)