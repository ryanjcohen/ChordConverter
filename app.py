from flask import Flask, request, render_template

app = Flask(__name__)
app.static_folder='static'

equality = {'A#':'Bb', 'B#':'C', 'C#':'Db', 'D#':'Eb', 'E#':'F', 'F#':'Gb', 'G#':'Ab'}
chord_letters = {'A', 'B', 'C', 'D', 'E', 'F', 'G'}
chords = ['Ab','A','Bb','B','C','Db','D','Eb','E','F','Gb','G']
posn = {}
for i in range(len(chords)):
	posn[chords[i]]=i
for chord in list(equality):
	equality[equality[chord]] = chord

@app.route("/")
def converter():
	return render_template("converter.html", value="Input chords here.",
		output="Transposed chords will appear here.")

@app.route('/transpose', methods=["POST"])
def transpose():
	half_steps = request.form['submit_button']
	text = request.form['text']
	transposed_text = process_text(half_steps,text)
	return render_template("converter.html", value=text, output=transposed_text)

def process_text(half_steps, text):
	''' 
	Takes text, a string containing song chords with lines containing chords preceded
	by asterisks and chord names capitalized, and outputs a string, transposed_text, 
	which is equivalent to the string text with the chords in lines preceded by 
	asterisks transposed a number of half steps equal to half_steps.

	Args:
		text: a string containing song chords to be transposed, where lines containing
			chords are preceded by asterisks and chord names are capitalized
		half_steps: the number of half steps to transpose chords in text by

	Returns:
		transposed_text: a string containing song chords where chords in lines preceded
			by asterisks have been transposed from the string text a number of half steps
			equal to half_steps

	'''
	transposed_text = text
	half_steps = int(half_steps)

	for i in range(len(transposed_text)):

		# Check if current character is the beginning of a line containing chords to be transposed.
		if i+1 < len(transposed_text) and transposed_text[i]=='*':

			# Remove asterisk from transposed_text
			transposed_text = transposed_text[:i] + transposed_text[i+1:]
			character = transposed_text[i]

			# Loop through line containing chords to be transposed.
			while i < len(transposed_text) and character != '\n':
				character = transposed_text[i]

				# Check that character is the name of a chord.
				if character in chord_letters:
					sharp = False
					original_chord = ''

					# Check if character is the name of a sharp chord.
					if i+1 < len(transposed_text) and transposed_text[i+1] == '#':
						sharp = True
						original_chord = original_chord + transposed_text[i:i+2]
					# Check if character is the name of a flat chord.
					elif i+1 < len(transposed_text) and transposed_text[i+1] == 'b':
						original_chord = original_chord + transposed_text[i:i+2]
					else:
						original_chord = original_chord + transposed_text[i:i+1]

					# Convert sharp chord to a non-sharp chord so the array chords can be used
					# for transposition.
					chord = original_chord

					if sharp:
						chord = equality[chord]

					idx = posn[chord]

					transposed_idx = (idx + half_steps) % len(chords)
					transposed_chord = chords[transposed_idx]

					# If previously sharp chord was transposed to a flat chord, convert it
					# to the equivalent non-flat chord.
					if sharp and transposed_chord in equality:
						transposed_chord = equality[transposed_chord]

					original_chord_len = len(original_chord)
					transposed_chord_len = len(transposed_chord)

					if i+transposed_chord_len < len(transposed_text):
						next_char = transposed_text[i+transposed_chord_len]

						if transposed_chord_len == original_chord_len or (transposed_chord_len > original_chord_len 
							and next_char != ' '):
							transposed_text = transposed_text[:i] + transposed_chord + transposed_text[i+len(chord):]
						elif transposed_chord_len < original_chord_len:
							transposed_text = transposed_text[:i] + transposed_chord + ' ' + transposed_text[i+len(chord):]
						elif transposed_chord_len > original_chord_len and next_char == ' ':
							transposed_text = transposed_text[:i] + transposed_chord + transposed_text[i+1+len(chord):]

					
					else:
						transposed_text = transposed_text[:i] + transposed_chord
					
					i += len(transposed_chord)
				
				else:
					i += 1

	return transposed_text