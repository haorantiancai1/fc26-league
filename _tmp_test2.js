var firebase = {initializeApp: function(){}, database: function(){return {ref: function(){return {set:function(){},on:function(){}};}};}};
function _test(){

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
firebase.initializeApp(firebaseConfig);
dbRef = firebase.database();

// Compat SDK: firebase.database() returns a Database instance with .ref(path) method
// .ref(path) returns a Reference, which has .child(), .set(), .on('value', ...) etc.
try {
  console.log('dbRef type:', typeof dbRef, '| dbRef.ref type:', typeof dbRef.ref);
  if(typeof dbRef.ref === 'function') {
    _fbRef = function(db, path) { return db.ref(path); };
    console.log('Firebase initialized successfully (compat .ref mode)');
  } else if(typeof dbRef.child === 'function') {
    _fbRef = function(db, path) { return db.child(path); };
    console.log('Firebase initialized successfully (compat .child mode)');
  } else {
    console.error('FATAL: dbRef has no .ref or .child method. Keys:', Object.getOwnPropertyNames(dbRef));
  }
} catch(e) {
  console.error('Firebase init failed:', e);
}

// ===== SOUND EFFECTS =====
let _audioCtx = null;
}
