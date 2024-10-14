import React,{ useState } from 'react'
import { Link,useNavigate } from 'react-router-dom'
import { useLogin } from '../LoginContext';

const LoginPage = () => {

	const { user,setUser} = useLogin()
	const navigate = useNavigate()
	const [form, setForm] = useState({})

	const handleChange = (e) => {
		setForm({
			...form,
			[e.target.name]: e.target.value,
		});
	};


	const handleLogin = (e) => {
		e.preventDefault();
		const apiUrl = import.meta.env.VITE_API_URL;

		const login = async () => {
			const response = await fetch(`${apiUrl}/validateLogin`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(form),
			});
			const data = await response.json();
			if(response.ok){
				setUser(data);
				navigate('/');
			}
			else{
				alert('Invalid credentials');
			}
		};
		login();
	}
	

  return (
    <div className="login_css">
        <h1>Login/SignUp</h1>
        <form className='form'>
			<div className="input-field">
				<label htmlFor="email">Email:</label>
				<input type="email" name="email" id="email" placeholder="Enter your email" value={form.email || ''} onChange={handleChange} /> 
			</div>

			<div className="input-field">
				<label htmlFor="pswd">Password:</label>
				<input type="password" name="pswd" id="pswd" placeholder="Enter your password" value={form.pswd || ''} onChange={handleChange} /> 
			</div>

			<div className="extras">
				{/* <Link to="/forgotPassword">forgot password?</Link> */}
				<Link to="/signup">New User?</Link>
			</div>

			<input type="submit" value="Login" onClick={handleLogin} />
		</form>
    </div>
  )
}

export default LoginPage
