import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useLogin } from '../LoginContext';

const CompanyHome = () => {
	const apiUrl = import.meta.env.VITE_API_URL
	const [donations, setDonations] = useState([])
	const { user } = useLogin();
	
	useEffect(() => {
		const fetchDonations = async () => {
			const response = await fetch(`${apiUrl}/getDonationsbyParty/${user.partyId}`);
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			const data = await response.json();
			// console.log(data);
			
			setDonations(data);
		}

		fetchDonations();
	}, [])


	return (
		<>
		<div className='companyHome'>
			<h1>CompanyHome</h1>
			<h2>{user.party_name}</h2>
			<table>
				<thead>
					<tr>
						<th>Item Name</th>
						<th>Quantity Donated</th>
					</tr>
				</thead>
				<tbody>
					{
						// sample doantions = [[abc,abc,abc,abc],[xyz,xyz,xyz,xyz]]
						donations.map((donation, index) => (
							<tr key={index}>
								<td>{donation.Item_Name}</td>
								<td>{donation.Quantity_Donated}</td>
							</tr>
						))
					}
				</tbody>
			</table>

			<Link to="/companyDonate">Donate</Link>
		</div>
		</>
	)
}

export default CompanyHome