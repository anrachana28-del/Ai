const express=require("express");
const multer=require("multer");
const axios=require("axios");
const fs=require("fs");
const path=require("path");

const app=express();
const upload=multer({dest:"/tmp"});

// upload video → python AI
app.post("/upload-video",upload.single("file"),async(req,res)=>{

    const file=fs.readFileSync(req.file.path);

    try{
        const result=await axios.post(
            "https://https://ai-ouub.onrender.com/video-dub",
            file,
            {
                headers:{
                    "Content-Type":"application/octet-stream"
                }
            }
        );

        res.json(result.data);

    }catch(err){
        res.status(500).json({error:err.message});
    }
});

// serve generated videos
app.use("/files",express.static("/tmp"));

app.listen(3000,()=>{
    console.log("Node running on 3000");
});
