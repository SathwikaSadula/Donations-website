import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom';
import { useLogin } from '../LoginContext';


const SchoolHome = () => {
  const apiUrl = import.meta.env.VITE_API_URL
	const [pending, setPending] = useState([])
	const [processed, setProcessed] = useState([])
	const { user } = useLogin();

  useEffect(() => {
		const fetchPending = async () => {

			const response = await fetch(`${apiUrl}/getPendingRequests/${user.partyId}`);
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			const data = await response.json();
      // console.log(data);
			setPending(data);
		}

		const fetchProcessed = async () => {

			const response = await fetch(`${apiUrl}/getProcessedRequests/${user.partyId}`);
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			const data = await response.json();
      // console.log(data);
			setProcessed(data);
		}

		fetchPending();
		fetchProcessed();

	}, [])

  return (
    <>
      <div className='SchoolHome'>
			<h1>SchoolHome</h1>
      <h2>{user.party_name}</h2>
			<table>
          <thead>
            <tr>
              <th>Item</th>
              <th>Quantity Requested</th>
              <th>Quantity Pending</th>
              <th>Status</th>
            </tr>
          </thead>
        <tbody>
          {
            // sample doantions = [[abc,abc,abc,abc],[xyz,xyz,xyz,xyz]]
            pending.map((item, index) => (
              <tr key={index}>
                <td>{item.Item_Name}</td>
                <td>{item.Pending_Quantity}</td>
                <td>{item.Requested_Quantity}</td>
                <td>{item.Status}</td>
              </tr>
            ))
          }
        </tbody>
			</table>


			<table>
        <thead>
          <tr>
            <th>Item</th>
            <th>Company Name</th>
            <th>Quantity Donated</th>
          </tr>
        </thead>
        <tbody>
          {
            // sample doantions = [[abc,abc,abc],[xyz,xyz,xyz]]
            processed.map((item, index) => (
              <tr key={index}>
                <td>{item.Company_Name}</td>
                <td>{item.Item_Name}</td>
                <td>{item.Quantity}</td>
              </tr>
            ))
          }
        </tbody>
			</table>


      <Link to="/schoolRequest">New Request</Link>
    </div>
    </>
  )
}

export default SchoolHome