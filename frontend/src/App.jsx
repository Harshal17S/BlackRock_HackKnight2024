import "./App.css";
import "./index.css";
import { ThemeProvider } from "./components/theme-provider";
import { ReactLenis, useLenis } from "lenis/react";
import BeforeSign from "./Pages/Home/BeforeSign";
import { Route, Routes } from "react-router-dom";
import Dashboard from "./Pages/Dashboard";
import DashSignForm from "./components/CustomComponents/Forms/DashSignForm";
import Request from "./components/CustomComponents/Forms/Request";


function App() {
  const lenis = useLenis(({ scroll }) => {});

  return (
    <ReactLenis root>
      <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
        <Routes>
          <Route path="/" Component={BeforeSign}/>
          <Route path="/dashboard" Component={Dashboard}/>
          <Route path="/dashform" Component={DashSignForm}/>
          <Route path="/request" Component={Request}/>
        </Routes> 
      </ThemeProvider>
    </ReactLenis>

    

  );
}

export default App;
