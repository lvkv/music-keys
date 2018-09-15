const Application = function() {
	this.note = new Note()
}

Application.prototype.start = function() {
	this.note.init()
}

const app = new Application()
app.start()
