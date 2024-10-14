import React,{useState} from 'react'
import { useNavigate } from 'react-router-dom'
import { useLogin } from '../LoginContext'

const RequestPage = () => {
  const { user } = useLogin()
  const [form, setForm] = useState({})
  const navigate = useNavigate()

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  }

  const request = async (e) => {
    e.preventDefault();
    const apiUrl = import.meta.env.VITE_API_URL;
    const response = await fetch(`${apiUrl}/newItemRequest`, {
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
    alert('Request created successfully');
    navigate('/dashboard');
  }

  return (
    <>
    <div className='RequestPage'>
      <div>RequestPage</div>
      <form>
        <div className="input-field">
          <label htmlFor="itemType">Type:</label>
          <select name="itemType" id="itemType" value={form.itemType || ''} onChange={handleChange}>
            <option value="">Select Item</option>
            <option value="laptops">Laptops</option>
            <option value="monitors">Monitors</option>
            <option value="tablets">Tablets</option>
            <option value="printers">Printers</option>
            <option value="scanners">Scanners</option>
            <option value="storage_devices">Storage Devices</option>
            <option value="projectors">Projectors</option>
          </select>
        </div>
        <div className="input-field">
          <label htmlFor="quantity">Quantity:</label>
          <input type="number" name="quantity" id="quantity" value={form.quantity || ''} onChange={handleChange} />
        </div>

        <button type="submit" onClick={request}>request</button>
      </form>
    </div>
    </>
  )
}

export default RequestPage