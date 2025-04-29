let i = 0;
let playlist = [];
let songlist = []
async function moody(val) {
	let songs = await eel.get_songs(val)();
	playlist = [];
	songlist = [];
	for (let i = 0; i < songs.length; i++) {
		playlist.push("Songs\\" + val + "\\" + songs[i] + ".mp3");
		songlist.push(songs[i]);
	}
	return playlist;
}

async function getTime() {
	let value = await eel.get_emotion()();
	playlist = moody(value);
	return playlist;
}

function playsong(path, num) {
	document.getElementById("song_name").innerHTML = songlist[num];
	document.getElementById("sel").src = path;
	document.getElementById("main_slider").load();
	document.getElementById("main_slider").play();
}
async function get_emotion() {
	playlist = await getTime();
	i = 0;
	playsong(playlist[i], i);
}
async function random_play() {
	let view = await eel.random_play()();
	songlist = view.songlist;
	playlist = view.playlist;
	i = 0;
	playsong(playlist[i],i);
}

function song_over() {
	i++;
	if (i == playlist.length) {
		get_emotion();
	} else {
		playsong(playlist[i], i);
	}
}
function previous() {
	if (i == 0) {
		playsong(playlist[i], i);
	} else {
		i--;
		playsong(playlist[i], i);
	}
}
function play_pause() {
	let mus = document.getElementById("main_slider");
	if (mus.paused) {
		mus.play();
	} else {
		mus.pause();
	}
}
