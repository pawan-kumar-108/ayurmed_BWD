// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBpJBg4RVCm4R7ZlsAIJzzrovJhAhrLc4w",
  authDomain: "login--with-firebase-dfa89.firebaseapp.com",
  projectId: "login--with-firebase-dfa89",
  storageBucket: "login--with-firebase-dfa89.appspot.com",
  messagingSenderId: "12252723045",
  appId: "1:12252723045:web:b7a39f8a291e11a630938c",
  measurementId: "G-NS8NKLQ1CD"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth();
// const full_name = document.getElementById('full_name').value;

//REGISTER BUTTON 
const submit = document.getElementById('submit');
submit.addEventListener("click", function (event) {

  event.preventDefault()
  const email = document.getElementById('reg_email').value;
  const password = document.getElementById('reg_password').value;

  createUserWithEmailAndPassword(auth, email, password)

    .then((userCredential) => {
      // Signed up 
      const user = userCredential.user;
      window.location.assign("index.html");
      // ...
    })


    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      alert(errorMessage)
      // ..
    });
})