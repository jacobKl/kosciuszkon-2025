import React from 'react'
import logo from '../../../public/logo.png';

const Header = () => {
    return (
        <nav className="py-4 bg-white shadow">
        <a href="/" className="container mx-auto flex items-center">
            <img src={logo} alt={""} className={"h-10"}/>
            <div>Green<b>House</b></div>
        </a>
    </nav>
    )
}

export default Header;