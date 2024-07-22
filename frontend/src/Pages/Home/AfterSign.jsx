
import Features from "../../components/CustomComponents/Features/Features";
import Hero1 from "../../components/CustomComponents/Hero1/Hero1";
import React from "react";
import Navbar from "../../components/CustomComponents/Navbar/Navbar";
import { Waitlist } from "../../components/CustomComponents/Waitlist/Waitlist";
import Footer from "../../components/CustomComponents/Footer/Footer";
import Testimonial from "../../components/CustomComponents/Testomonials/Testimonial";
import Showcase from "../../components/CustomComponents/Showcase/Showcase";
import { Signup } from "../../components/CustomComponents/Forms/Signup";
import AfterSignNav from "../../components/CustomComponents/Navbar/AfterSignNav";

const Home = () => {
  return (
    <div>
      <AfterSignNav/>
      <Hero1 />
      <Features/>
      <Testimonial/>
      {/* <Price/> */}
      <Showcase/>
      <Waitlist/>
      <Footer/>
    </div>
  );
};

export default Home;
