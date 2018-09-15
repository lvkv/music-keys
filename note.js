const getFrequency = require('./getFrequency')

// Initialize the note class

const Note = function() {
	// Frequency of the A4 note (middle A) 
	this.a4 = 440	
	// Controls the number of sample frames to be processed each call
	this.bufferSize = 2048
	this.noteList = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
}

// Init method

Note.prototype.init = function() {
	this.audioContext = new AudioContext()
	
	this.analyser = this.audioContext.createAnalyser()
	this.record()
}

// Add the record method to the Note class

Note.prototype.record = function () {
	// Start recording audio
	navigator.mediaDevices.getUserMedia({ audio: true}).then(stream => {
		this.frequencies = new Float32Array(this.analyser.frequencyBinCount)

		this.microphone = this.audioContext.createMediaStreamSource(stream)
		this.microphone.connect(this.analyser)

		this.analyser.getFloatFrequencyData(this.frequencies)
		
		console.log(getFrequency(this.frequencies))
	})
}
