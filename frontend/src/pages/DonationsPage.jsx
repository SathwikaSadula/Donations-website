import React,{useState} from 'react'
import { useNavigate } from 'react-router-dom'
import { useLogin } from '../LoginContext'


const DonationsPage = () => {
  const { user } = useLogin()
  const [form, setForm] = useState({})
  const navigate = useNavigate()

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  }
 
  const donate = async (e) => {
    e.preventDefault();
    const apiUrl = import.meta.env.VITE_API_URL;
    const response = await fetch(`${apiUrl}/createNewDonation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...form,
        partyId: user.partyId
      }),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    alert('Donation created successfully');
    navigate('/dashboard');
  }
  return (
    <>
    <div className='DonationsPage'>
      <div>DonationsPage</div>
      <form>
        <div className="input-field">
          <label htmlFor="itemType">Type:</label>
          <select name="itemType" id="itemType" value={form.itemType || ''} onChange={handleChange}>
            <option value="">Select Item</option>
            <option value="laptops">Laptops</option>
            <option value="monitors">monitors</option>
            <option value="tablets">tablets</option>
            <option value="chairs">chairs</option>
            <option value="desks">desks</option>
            <option value="projectors">projectors</option>
          </select>
        </div>
        <div className="input-field">
          <label htmlFor="quantity">Quantity:</label>
          <input type="number" name="quantity" id="quantity" value={form.quantity || ''} onChange={handleChange} />
        </div>

        <button type="submit" onClick={donate}>Donate</button>
      </form>
    </div>
    </>
  )
}

export default DonationsPage