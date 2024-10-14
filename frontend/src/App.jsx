import './App.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { Navigate } from 'react-router-dom';

import { useLogin } from './LoginContext';
import LoginPage from './pages/LoginPage';
import DashBoard from './pages/DashBoard';
import SignUpPage from './pages/SignUpPage';
import DonationsPage from './pages/DonationsPage';
import RequestPage from './pages/RequestPage';


function App() {
  const { user } = useLogin()
  const router = createBrowserRouter([
    {
      path: '/',
      element: user.partyId!="" ? <Navigate to="/dashboard" /> : <Navigate to="/login" />
    },
    {
      path: '/dashboard',
      element:  user.partyId!="" ? <DashBoard/> : <Navigate to="/login" />
    },
    {
      path: '/login',
      element: <LoginPage />
    },
    {
      path: '/signup',
      element: <SignUpPage />
    },
    {
      path: '/companyDonate',
      element: <DonationsPage />
    },
    {
      path: '/schoolRequest',
      element: <RequestPage />
    },
  ]);

  return (
    <RouterProvider router={router} />
  )
}

export default App
