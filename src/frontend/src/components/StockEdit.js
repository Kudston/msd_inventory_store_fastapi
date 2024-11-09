import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { API_URLS } from '../config/apiConfig';

function StockEdit() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { accessToken } = useAuth();
  const [stock, setStock] = useState({ name: '', units: 0 });

  useEffect(() => {
    if (accessToken) {
      fetch(`${API_URLS.GET_STOCK}?id=${id}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        }
      })
        .then(response => response.json())
        .then(data => setStock(data))
        .catch(error => console.error('Error fetching stock:', error));
    }
  }, [accessToken, id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_URLS.EDIT_STOCKS}?id=${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(stock)
      });
      if (response.ok) {
        navigate('/products');
      } else {
        throw new Error('Failed to Add stock');
      }
    } catch (error) {
      console.error('Error updating stock:', error);
      alert('Failed to update stock. Please try again.');
    }
  };

  return (
    <div className="container mt-4 col-5">
      <h2>Edit Stock: {stock.title}</h2>
      <h2>Current in stock:<span className='text-info'>{stock.units}</span></h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="title" className="form-label">Title</label>
          <input
            type="text"
            className="form-control"
            id="title"
            value={stock.title}
            onChange={(e) => setStock({...stock, title: e.target.value})}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="quantity" className="form-label">Quantity to add:</label>
          <input
            type="number"
            className="form-control"
            id="units"
            value={0}
            onChange={(e) => setStock({...stock, units: parseInt(e.target.value)})}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">Update Stock</button>
        <button type="button" className="btn btn-secondary ms-2" onClick={() => navigate('/products')}>Cancel</button>
      </form>
    </div>
  );
}

export default StockEdit;
