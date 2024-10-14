import React from 'react'
import { useLogin } from '../LoginContext'
import CompanyHome from './CompanyHome'
import SchoolHome from './SchoolHome'

const DashBoard = () => {
    const { user, setUser } = useLogin()
    if (user.userType == 'Company') {
        return <CompanyHome />;
    } else {
        return <SchoolHome />;
    }
}

export default DashBoard
