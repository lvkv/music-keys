function getFrequency (frequencies) {
	const rate = 22050 / 1024

	let maxI, max = frequencies[0]

	for (var i=0; frequencies.length > i; i++) {
    	let oldmax = parseFloat(max)
    	let newmax = Math.max(max, frequencies[i])
    	
    	if (oldmax != newmax) {
      		max = newmax
      		maxI = i
    	} 
  }
  return maxI * rate
}

module.exports = getFrequency
