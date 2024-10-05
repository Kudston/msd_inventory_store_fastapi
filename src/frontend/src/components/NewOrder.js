import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { API_URLS } from '../config/apiConfig';


function CartCreate() {
    const [id, setId] = useState();
    const navigate = useNavigate();
    const { accessToken } = useAuth();
  
    useEffect(() => {
      if (accessToken) {
        fetch(`${API_URLS.CREATE_CART}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
          }
        })
          .then(response => response.json())
          .then(data => {
            setId(data['id']);  // Set the id state
            console.log(data['id']);  // Log the id from data
            // Use a callback or useEffect to navigate after id is set
          })
          .catch(error => console.error('Error creating cart:', error));
      }
    }, [accessToken]);
  
    useEffect(() => {
      if (id) {
        navigate(`/cart-edit/${id}`);  // Navigate only when id has been updated
      }
    }, [id, navigate]);
  
    return (
      <div>
        Creating Cart...
      </div>
    );
  }
  
  export default CartCreate;