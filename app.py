from flask import Flask, request, render_template
import re

app = Flask(__name__)
app.static_folder='static'

equality = {'A#':'Bb', 'B#':'C', 'C#':'Db', 'D#':'Eb', 'E#':'F', 'F#':'Gb', 'G#':'Ab'}
chords = ['Ab','A','Bb','B','C','Db','D','Eb','E','F','Gb','G']
posn = {}
for i in range(len(chords)):
	posn[chords[i]]=i
for chord in list(equality):
	equality[equality[chord]] = chord

notes = "[ABCDEFG]"
accidentals = "(b|bb|#)?"
chord_type = "(m|maj7|maj|min7|min|sus)?"
suspensions = "(1|2|3|4|5|6|7|8|9)?"
chord_regex = notes + accidentals + chord_type + suspensions

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


def is_chord_line(line):
	''' 
	Takes the string line and determines if line only contains the names of chords.

	Args:
		line: a string of text

	Returns:
		chord_line: a boolean indicating whether or not line contains only chord names.

	'''

	line = line.split()
	chord_line = True
	
	for word in line:
		if '/' in word:
			# If word contains the character '/', word potentially contains multiple 
			# chords. Therefore, word must be split using the character '/', and the
			# resulting strings must all be tested to see if they are chord names.
			chords = word.split('/')
			for chord in chords:
				print(chord)
				if (re.fullmatch(chord_regex, chord) == None):
					chord_line = False
				break
		elif (re.fullmatch(chord_regex, word) == None):
			chord_line = False
			break

	return chord_line


def process_text(half_steps, text):
	''' 
	Takes text, a string where each line contains either only chords with chord names
	capitalized or lyrics, and outputs a string, transposed_text, which is equivalent to 
	the string text with the chords in lines containg only chord names transposed a number 
	of half steps equal to half_steps.

	Args:
		text: a string containing song chords to be transposed and possibly lyrics where
			each line contains either only chords with chord names capitalized or lyrics
		half_steps: a string representing the number of half steps to transpose chords in 
			text by

	Returns:
		transposed_text: a string containing song chords where chords in lines contiaing
			only song chords have been transposed from the string text a number of half 
			steps equal to half_steps

	'''
	text_lines = text.split('\n')
	half_steps = int(half_steps)

	for line in range(len(text_lines)):
		# Determine if text_lines[line] is a line containing only chords.
		chord_line = is_chord_line(text_lines[line])
		if chord_line:
			# Transpose text_lines[line] a number of half steps equal to half_steps.
			transposed_line = transpose(text_lines[line], half_steps)
			text_lines[line] = transposed_line

	transposed_text = ''
	for line in text_lines:
		transposed_text = transposed_text + line + '\n'

	return transposed_text


def transpose(line, half_steps):
	''' 
	Takes line, a string containing a sequence of chords and outputs a string equivalent 
	to line with the chords transposed a number of half steps equal to half_steps.

	Args:
		line: a string containing song chords to be transposed, where lines containing
			chords are preceded by asterisks and chord names are capitalized
		half_steps: a string representing the number of half steps to transpose chords in 
			text by

	Returns:
		line: a string updated from the input string line where song chords have been 
			transposed from the original string a number of half steps equal to half_steps

	'''

	# Loop through line containing chords to be transposed.
	i = 0
	while(i < len(line)):
		character = line[i]

		# Check that character is the name of a chord.
		if re.match(notes, character) != None:
			sharp = False
			original_chord = ''

			# Check if character is the name of a sharp chord.
			if i+1 < len(line) and line[i+1] == '#':
				sharp = True
				original_chord = original_chord + line[i:i+2]
			# Check if character is the name of a flat chord.
			elif i+1 < len(line) and line[i+1] == 'b':
				original_chord = original_chord + line[i:i+2]
			else:
				original_chord = original_chord + line[i:i+1]

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

			if i + transposed_chord_len < len(line):
				next_char = line[i+transposed_chord_len]

				if transposed_chord_len == original_chord_len or (transposed_chord_len > original_chord_len 
					and next_char != ' ') or (transposed_chord_len < original_chord_len and 
					next_char != 'm' and re.match(suspensions,next_char) != None):
					line = line[:i] + transposed_chord + line[i+len(chord):]
				elif transposed_chord_len < original_chord_len:
					line = line[:i] + transposed_chord + ' ' + line[i+len(chord):]
				elif transposed_chord_len > original_chord_len and next_char == ' ':
					line = line[:i] + transposed_chord + line[i+1+len(chord):]

			else:
				line = line[:i] + transposed_chord
			
			i += len(transposed_chord)
		
		else:
			i += 1

	return line