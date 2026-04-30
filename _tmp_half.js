
// ===== FIREBASE INIT (dynamic loading) =====
const firebaseConfig = {
  apiKey: "AIzaSyAvsb1AAF5RffIycA82ai5yWj-Qdzu2Bfo",
  authDomain: "fc26-league-47ef8.firebaseapp.com",
  databaseURL: "https://fc26-league-47ef8-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "fc26-league-47ef8",
  storageBucket: "fc26-league-47ef8.firebasestorage.app",
  messagingSenderId: "1054047306704",
  appId: "1:1054047306704:web:b74c29a7459b96ca7cefd5"
};
let dbRef = null;
let _fbRef = null; // modular ref helper

// Firebase read/write helpers using modular API
function _fbSave(path, data) {
  if(!_fbRef) return;
  _fbRef(dbRef, path).set(data).then(function() {
    console.log('FB saved:', path);
  }).catch(function(e) { console.error('FB write error:', e); });
}
function _fbListen(path, cb) {
  if(!_fbRef) return;
  _fbRef(dbRef, path).on('value', function(snap) { cb(snap.val()); });
}

// Firebase SDK is loaded via <script> tags in <head>
try {
