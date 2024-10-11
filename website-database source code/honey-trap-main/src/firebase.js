// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getDatabase } from 'firebase/database';
//import firebaseConfig from './firebaseConfig'
//import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAH9FVxG2Fc0DtocVyI_bG3o28HcGHeS4k",
  authDomain: "honeypot-891e9.firebaseapp.com",
  databaseURL: "https://honeypot-891e9-default-rtdb.firebaseio.com",
  projectId: "honeypot-891e9",
  storageBucket: "honeypot-891e9.appspot.com",
  messagingSenderId: "1026455785849",
  appId: "1:1026455785849:web:d5e622fd181fd28c25dfa8",
  measurementId: "G-RP883D1G0T"
};


// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app)

export default app;

//const analytics = getAnalytics(app);
