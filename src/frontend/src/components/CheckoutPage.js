import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { API_URLS } from '../config/apiConfig';

function CheckoutPage() {
  const { cartId } = useParams();
  const [cart, setCart] = useState(null);
  const { accessToken } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (accessToken && cartId) {
      fetch(`${API_URLS.GET_CART}/${cartId}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        }
      })
        .then(response => response.json())
        .then(data => setCart(data))
        .catch(error => console.error('Error fetching cart:', error));
    }
  }, [accessToken, cartId]);

  const handleConfirmCheckout = () => {
    fetch(`${API_URLS.CHECKOUT_CART}/${cartId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      }
    })
      .then(response => response.json())
      .then(data => {
        console.log('Checkout successful:', data);
        navigate('/carts');
      })
      .catch(error => console.error('Error during checkout:', error));
  };

  if (!cart) {
    return <div className="container mt-4">Loading...</div>;
  }

  return (
    <div className="container mt-4">
      <h2 className="text-center mb-4">Checkout Confirmation</h2>
      <div className="card">
        <div className="card-body">
          <h3 className="card-title">Cart ID: {cart.id}</h3>
          <p className="card-text"><strong>Total Amount:</strong> ${cart.total_amount.toFixed(2)}</p>
          <p className="card-text">Are you sure you want to checkout this cart?</p>
          <div className="d-flex justify-content-between">
            <button onClick={() => navigate('/carts')} className="btn btn-secondary">Cancel</button>
            <button onClick={handleConfirmCheckout} className="btn btn-success">Confirm Checkout</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CheckoutPage;