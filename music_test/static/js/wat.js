/* WEB AUDIO TUNER */
/* Adapted from Web Audio Tuner by Joaquin Bonet */
/* https://developer.microsoft.com/en-us/microsoft-edge/testdrive/demos/webaudiotuner/ */

$(document).ready(function () {
	'use strict';

	//var baseFreq = 440;
	//var currentNoteIndex = 57; // A4
	//var isRefSoundPlaying = false;
    var lowNote = "G2";
    var highNote = "C5";
    var pitchArray = [];
    var averages = [];
	var isMicrophoneInUse = false;
	var frameId,
		freqTable,
		//gauge,
		micStream,
		notesArray,
		audioContext,
		sourceAudioNode,
		analyserAudioNode;

	var isAudioContextSupported = function () {
		// This feature is still prefixed in Safari
		window.AudioContext = window.AudioContext || window.webkitAudioContext;
		if (window.AudioContext) {
			return true;
		}
		else {
			return false;
		}
	};

	var reportError = function (message) {
		$('p#messages').fadeIn();
        $('p#messages').html(message);
	};

	var init = function () {
		$.getJSON('/static/json/notes.json', function (data) {
            //console.log(data);
			freqTable = data;
		});

		if (isAudioContextSupported()) {
			audioContext = new window.AudioContext();
		}
		else {
			reportError('<span style="color:red">AudioContext is not supported in this browser.<br>Please use updated version of Chrome or Firefox</span>');
		}
	};

	var isGetUserMediaSupported = function () {
		navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
		if ((navigator.mediaDevices && navigator.mediaDevices.getUserMedia) || navigator.getUserMedia) {
			return true;
		}
		return false;
	};

	var findFundamentalFreq = function (buffer, sampleRate) {
		// We use Autocorrelation to find the fundamental frequency.

		// In order to correlate the signal with itself (hence the name of the algorithm), we will check two points 'k' frames away.
		// The autocorrelation index will be the average of these products. At the same time, we normalize the values.
		// Source: http://www.phy.mty.edu/~suits/autocorrelation.html
		// Assuming the sample rate is 48000Hz, a 'k' equal to 1000 would correspond to a 48Hz signal (48000/1000 = 48),
		// while a 'k' equal to 8 would correspond to a 6000Hz one, which is enough to cover most (if not all)
		// the notes we have in the notes.json?_ts=1470327772251 file.
		var n = 1024;
		var bestK = -1;
		var bestR = 0;
		for (var k = 78; k <= 500; k++) {
			var sum = 0;

			for (var i = 0; i < n; i++) {
				sum += ((buffer[i] - 128) / 128) * ((buffer[i + k] - 128) / 128);
			}

			var r = sum / (n + k);

			if (r > bestR) {
				bestR = r;
				bestK = k;
			}

			if (r > 0.9) {
				// Let's assume that this is good enough and stop right here
				break;
			}
		}

		if (bestR > 0.0025) {
			// The period (in frames) of the fundamental frequency is 'bestK'. Getting the frequency from there is trivial.
			var fundamentalFreq = sampleRate / bestK;
			return fundamentalFreq;
		}
		else {
			// We haven't found a good correlation
			return -1;
		}
	};

	var findClosestNote = function (freq, notes) {
		// Use binary search to find the closest note
		var low = 0;
		var high = notes.length - 1;
		while (high - low > 1) {
			var pivot = Math.round((low + high) / 2);
			if (notes[pivot].frequency <= freq) {
				low = pivot;
			} else {
				high = pivot;
			}
		}

		if (Math.abs(notes[high].frequency - freq) <= Math.abs(notes[low].frequency - freq)) {
			// notes[high] is closer to the frequency we found
			return notes[high];
		}

		return notes[low];
	};

	var findCentsOffPitch = function (freq, refFreq) {
		// We need to find how far freq is from baseFreq in cents
		var log2 = 0.6931471805599453; // Math.log(2)
		var multiplicativeFactor = freq / refFreq;

		// We use Math.floor to get the integer part and ignore decimals
		var cents = Math.floor(1200 * (Math.log(multiplicativeFactor) / log2));
		return cents;
	};

	var detectPitch = function () {
		var buffer = new Uint8Array(analyserAudioNode.fftSize);
		analyserAudioNode.getByteTimeDomainData(buffer);

		var fundamentalFreq = findFundamentalFreq(buffer, audioContext.sampleRate);

		if (fundamentalFreq !== -1) {
			var note = findClosestNote(fundamentalFreq, notesArray);
			var cents = findCentsOffPitch(fundamentalFreq, note.frequency);
			console.log(note.note, cents, fundamentalFreq);
            pitchArray.push([note.note,cents,fundamentalFreq]);
            $("#record").css("background-color","red");
		}
		else {
            console.log('--');
            $("#record").css("background-color","black");
		}

		frameId = window.requestAnimationFrame(detectPitch);
	};

	var streamReceived = function (stream) {
		micStream = stream;

		analyserAudioNode = audioContext.createAnalyser();
		analyserAudioNode.fftSize = 2048;

		sourceAudioNode = audioContext.createMediaStreamSource(micStream);
		sourceAudioNode.connect(analyserAudioNode);

		detectPitch();
	};
    
    var averagePitches = function (pitchArray) {
        var tempArray = [];
        var noteArray = [];
        var length = pitchArray.length;
        
        if (length > 1) {
            var note = pitchArray[0][0];
            var cents = pitchArray[0][1];
            var freq = pitchArray[0][2];
            var count = 1;
            
            for ( var i = 1; i < length; i++ ) {
                if ( pitchArray[i][0] == note ){
                    cents = cents + pitchArray[i][1];
                    freq = freq + pitchArray[i][2];
                    count++;
                    
                    if ( i == length - 1) {
                        if (count > 10){
                            cents = cents/count;
                            freq = freq/count;
                            tempArray.push([note, cents, freq, count]);
                            break;
                        }
                    }
                }
                else {
                    if (count > 7){
                        cents = cents/count;
                        freq = freq/count;
                        tempArray.push([note, cents, freq, count]);
                    }
                    note = pitchArray[i][0];
                    cents = pitchArray[i][1];
                    freq = pitchArray[i][2];
                    count = 1;
                }
            }
            console.log(tempArray);
            // Cleaning loop. Combines adjacent notes of the same pitch
            length = tempArray.length;
            if (length > 2){
                var currNote = tempArray[0];
                note = currNote[0];
                cents = currNote[1];
                freq = currNote[2];
                count = currNote[3];
                
                for (var j = 1; j < length; j++){
                    var nextNote = tempArray[j];
                    
                    if (note == nextNote[0] ){
                        cents = (note*count + nextNote[1]*nextNote[3]) / (count + nextNote[3]);
                        freq = (freq*count + nextNote[2]*nextNote[3]) / (count + nextNote[3]);
                        count = (count + nextNote[3]);
                    }
                    else {
                        noteArray.push( [note, cents, freq, count] );
                        currNote = nextNote;
                        
                        note = currNote[0];
                        cents = currNote[1];
                        freq = currNote[2];
                        count = currNote[3];
                    }
                }
                // For Loop is done
                noteArray.push( [note, cents, freq, count] );
            }
            //TempArray.length <= 2
            else{
                return tempArray;
            }
        }
        return noteArray;
    };

	var turnOffMicrophone = function () {
		if (sourceAudioNode && sourceAudioNode.mediaStream && sourceAudioNode.mediaStream.stop) {
			sourceAudioNode.mediaStream.stop();
		}
		sourceAudioNode = null;
		analyserAudioNode = null;
		window.cancelAnimationFrame(frameId);
		isMicrophoneInUse = false;
        console.log(pitchArray);
        averages = averagePitches(pitchArray);
        console.log(averages);
        pitchArray = [];
        $("#record").css("background-color","black");
	};

	var toggleMicrophone = function () {

		if (!isMicrophoneInUse) {
			if (isGetUserMediaSupported()) {
                notesArray = freqTable.notes;
				var getUserMedia = navigator.mediaDevices && navigator.mediaDevices.getUserMedia ?
					navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices) :
					function (constraints) {
						return new Promise(function (resolve, reject) {
							navigator.getUserMedia(constraints, resolve, reject);
						});
					};

				getUserMedia({audio: true}).then(streamReceived).catch(reportError);
				isMicrophoneInUse = true;
                $("#record").html('Stop');
                $("#messages").fadeOut();
			}
			else {
				reportError('<span style="color:red">It looks like this browser does not support getUserMedia.<br>Please use updated version of Chrome or Firefox</span>');
			}
		}
		else {
			turnOffMicrophone();
            $("#record").html('Record');
            $("#submit").removeAttr('disabled');
		}
	};
   
    function note(pitch, cents, freq, length){
        this.pitch = pitch;
        this.cents = cents;
        this.freq = freq;
        this.length = length;
    };
     
    var submit = function () {
        var avlen = averages.length;
        var thisNote;
        var notes = [];
        for ( var i = 0; i < avlen ; i++){
             thisNote = new note( averages[i][0], averages[i][1], averages[i][2], averages[i][3]);
             notes.push(thisNote);
        }
        var jsonData = JSON.stringify(notes);
        console.log(jsonData);
        
        var csrftoken = $.cookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        
        $.ajax({
            url: '/submit/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(notes),
            success: function(response) {
                //var res = JSON.parse(response);
                //console.log(res);
                $('p#messages').fadeIn();
                $('p#messages').html(response.message);
                $("#submit").attr('disabled','disabled');
                
                if (response.playnote == "True"){
                        $("#second_button").removeAttr('disabled');
                }
            }
        });
        
    };
    
	init();
    
    $('#record').click(toggleMicrophone);
    $('#submit').click(submit);
});