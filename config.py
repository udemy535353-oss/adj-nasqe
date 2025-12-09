import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyChR0fgAC4xrgDf9FRpqjfWn6l4gQ_HQSU",
  'authDomain': "nasqeprevoisly.firebaseapp.com",
  'projectId': "nasqeprevoisly",
  'storageBucket': "nasqeprevoisly.firebasestorage.app",
  'messagingSenderId': "820508877235",
  'appId': "1:820508877235:web:909023e58f364e7bfbebc6",
  'measurementId': "G-NZ5VM53HM1",
  'databaseURL': ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()