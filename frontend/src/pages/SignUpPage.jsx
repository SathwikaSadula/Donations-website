import React from 'react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const SignUpPage = () => {
  const [form, setForm] = useState({})
	const handleChange = (e) => {
		setForm({
			...form,
			[e.target.name]: e.target.value,
		});
	};

  const handleSignup = async (e)=>{
    e.preventDefault();
    const apiUrl = import.meta.env.VITE_API_URL;

    const response = await fetch(`${apiUrl}/createParty`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...form,
      }),
    });

    const data = await response.json();
    console.log(data);
    if(response.ok){
      alert('Party created successfully');
      navigate('/login');
    }
    else{
      alert('Error creating party');
    }
  }

  
  return (
    <div className='signup'>
        <h1>SignUp</h1>
        <div className='form'>
          <div className="input-field">
            <label htmlFor="contactEmail">User Email:</label>
            <input type="email" name="contactEmail" id="contactEmail" placeholder="Enter your email" value={form.contactEmail || ''} onChange={handleChange} /> 
          </div>

          <div className="input-field">
            <label htmlFor="password">Password:</label>
            <input type="password" name="password" id="password" placeholder="Enter your password" value={form.password || ''} onChange={handleChange} /> 
          </div>

          <div className="input-field">
            <label htmlFor="addLine1">Address Line1:</label>
            <input type="text" name="addLine1" id="addLine1" value={form.addLine1 || ''} onChange={handleChange} /> 
          </div>
          <div className="input-field">
            <label htmlFor="addLine2">Address Line2:</label>
            <input type="text" name="addLine2" id="addLine2" value={form.addLine2 || ''} onChange={handleChange} /> 
          </div>
					<div className="input-field">
						<label htmlFor="city">City:</label>
						<input type="text" name="city" id="city" value={form.city || ''} onChange={handleChange} /> 
					</div>
					<div className="input-field">
						<label htmlFor="state">State:</label>
						<input type="text" name="state" id="state" value={form.state || ''} onChange={handleChange} /> 
					</div>
					<div className="input-field">
						<label htmlFor="zip">Zip:</label>
						<input type="text" name="zip" id="zip" value={form.zip || ''} onChange={handleChange} /> 
					</div>

					<div className="input-field">
            <label htmlFor="contactName">Contact Name:</label>
            <input type="text" name="contactName" id="contactName"  value={form.contactName || ''} onChange={handleChange} /> 
          </div>
					
					<div className="input-field">
            <label htmlFor="phone">Contact Phone:</label>
            <input type="tel" name="phone" id="phone"  value={form.phone || ''} onChange={handleChange} /> 
          </div>

					<div className="input-field">
            <label htmlFor="partyType">Type:</label>
						<select name="partyType" id="partyType" value={form.partyType || ''} onChange={handleChange}>
							<option value="">Select Type</option>
							<option value="company">Company</option>
							<option value="school">School</option>
						</select>
          </div>
					<div className="input-field">
            <label htmlFor="imageName">Image Name:</label>
            <input type="text" name="imageName" id="imageName"  value={form.imageName || ''} onChange={handleChange} /> 
          </div>
				</div>

        <input type="button" value="Sign Up" onClick={handleSignup} />
    </div>
  )
}

export default SignUpPage