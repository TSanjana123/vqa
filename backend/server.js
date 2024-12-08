const express = require('express');

const cors = require('cors');

const mongoose = require('mongoose');

const jwt = require('jsonwebtoken');

const cookieParser = require('cookie-parser');

require('dotenv').config();

const app = express();

app.use(cors({ credentials: true, origin: 'http://localhost:3000' }));
// app.use(cors({ credentials: true, origin: 'http://192.168.0.141:3000' }));
// app.use(cors({ credentials: true, origin: 'http://192.168.187.187:3000' }));

app.use(express.json());

app.use(cookieParser());

const dotenv = require('dotenv');

const path = require('path');
const envPath = path.resolve(__dirname,"./.env")
console.log("envpath : ",envPath)


dotenv.config({ path: envPath });

console.log(process.env.MY_VARIABLE);

mongoose
  .connect(process.env.REACT_APP_MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log('Connected to MongoDB');
  })
  .catch((err) => {
    console.error('Failed to connect to MongoDB:', err);
  });


const userSchema = new mongoose.Schema({
    username  : {type: String,required:true},
    email : {type:String,required:true,unique:true},
    password : {type:String,required:true}
});

// const signupitem = mongoose.model('signup',userSchema);
const SignupItem = mongoose.model('SignupItem', userSchema);
console.log("SignupItem : ",SignupItem)
app.post('/api/signin',(req,res) => {
    console.log("req body : ",req.body)
    console.log("enter into app.post of signin")
    const newsignupitem = new SignupItem({username:req.body.username,email:req.body.email,password:req.body.password})

    newsignupitem
        .save()
        .then((result) => {
            // console.log("result signup")
            // console.log("username,email,password",result);
            res.sendStatus(200);
        })
});


app.post('/api/login', async(req,res) => {
  const { email , password } = req.body;
  try {
    const user = await SignupItem.findOne({ email});
    if(!user){
      return res.status(401).json({error: 'Invalid email or password'});
    }
    if(user.password!==password){
      return res.status(401).json({error:'wrong password'});
    }
    if(user.password===password){
      res.status(200).json({Message:"Login success"});
    }
  }
  catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'An error occurred during login' });
  }
});


const port = 5001;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});


