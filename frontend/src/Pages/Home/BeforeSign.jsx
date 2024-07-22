import React from 'react'
import { SignedOut, SignedIn } from "@clerk/clerk-react";
import Home from './Home';
import AfterSign from './AfterSign'

function BeforeSign() {
  return (
    <div>
        <SignedOut>
            <Home/>
        </SignedOut>

        <SignedIn>
            <AfterSign/>
        </SignedIn>
    </div>
  )
}

export default BeforeSign