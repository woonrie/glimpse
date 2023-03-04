import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import 'firebase/compat/firestore';

const firebaseConfig = {
    "config" : "config"
  };

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

export const addLinkToDB = (link) => {
  db.collection("links").add({
    link: link,
    timestamp: firebase.firestore.FieldValue.serverTimestamp()
  })
    .then(function (docRef) {
      console.log("Document written with ID: ", docRef.id);
    })
    .catch(function (error) {
      console.error("Error adding document: ", error);
    });
};