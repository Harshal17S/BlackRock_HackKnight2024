import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { BrowserRouter } from 'react-router-dom';
import { ClerkProvider } from '@clerk/clerk-react';
import { UserEmailProvider } from './components/Context/UserEmail.jsx';

const PUBLISHABLE_KEY = "pk_test_Y3VkZGx5LWNoZWV0YWgtNjMuY2xlcmsuYWNjb3VudHMuZGV2JA";

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
      <UserEmailProvider>
      <BrowserRouter>
        <App />
      </BrowserRouter>
      </UserEmailProvider>
    </ClerkProvider>
  </React.StrictMode>,
)
