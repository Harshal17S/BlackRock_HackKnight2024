const express = require("express");
require("./db/connection");
const user = require("./models/user");
const app = express();
const cors = require("cors");
// const bcrypt = require("bcrypt");
// const bodyParser = require("body-parser");


app.use(express.json());
app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.post("/register", async (req, resp) => {
  let a = new user(req.body);
//   let b = await a.save();
//   const salt = await bcrypt.genSaltSync(10);
//   const hash = await bcrypt.hashSync(req.body.password, salt);
//   const NewUser = {
//     name: req.body.name,
//     email: req.body.email,
//     password: hash,
//   };
//   let USer = new user(NewUser);
  let result = await a.save();
  resp.send(result);
  // resp.send(req.body)
});

app.post("/login", async (req, resp) => {
  if (req.body.password && req.body.email) {
    let User = await sample.findOne(req.body).select("-password");
    if (User) {
      resp.send(User);
    } else {
      resp.send({ result: "No user Found" });
    }
  } else {
    resp.send({ result: "No user Found" });
  }
});
app.get("/", function (req, resp) {
  resp.send("App running");
});

app.post("/add-product", async (req, resp) => {
  let product = new products(req.body);
  let result = await product.save();
  resp.send(result);
}),
  app.get("/product", async (req, resp) => {
    const product = await products.find();
    if (product.length > 0) {
      resp.send(product);
    } else {
      resp.send({ result: "NO Product Found" });
    }
  }),
  app.delete("/product/:id", async (req, res) => {
    let result = await products.deleteOne({ _id: req.params.id });
    res.send(result);
  }),
  app.get("/product/:id", async (req, res) => {
    let result = await products.findOne({ _id: req.params.id });
    if (result) {
      res.send(result);
    } else {
      res.send({ result: "No record" });
    }
  }),
  app.put("/product/:id", async (req, res) => {
    let result = await products.updateOne(
      { _id: req.params.id },
      {$set: req.body}
      
    );
    res.send(result);
  }),
  app.listen(5001);