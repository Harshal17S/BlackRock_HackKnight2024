const mongoose=require('mongoose');

const userschema=new mongoose.Schema({
    name:String,
    currentsaving:String,
    AnnualSaving:String,
    Goal:String,
    month:String,
    lastmonthsave:Number
})
// userschema.pre('save',async function(next){
//     const user =this;
//     if(!user.isModified("passsword")){
//         next();
//     }
//     try{
//         const salt =await  bcrypt.genSaltSync(10);
//         const hash = await bcrypt.hashSync(user.password, salt);
//         console.log("hashed pass is "+hash)
//         user.password=hash;
//         console.log("hashed pass is "+user.password)
//     }
//     catch(error){
// next(error)
//     }
// })

module.exports=mongoose.model("user",userschema);