import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { API_URLS } from '../config/apiConfig';
import CartItems from './CartItemsList';
import AddStockComponent from './AddStocksToCart';

function CartEdit() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { accessToken } = useAuth();
  const [items, setItems] = useState([]);
  const [cart_total, setTotal] = useState(0);
  const [cart_status, setCartStatus] = useState();
  const [availableProducts, setAvailableProducts] = useState([]);
  const [ loading, setLoading ] = useState(true);

  useEffect(() => {
    if (accessToken) {
      fetch(`${API_URLS.GET_CART}?cart_id=${id}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        }
      })
        .then(response => response.json())
        .then(data => {
          setTotal(data['total_amount']);
          setItems(data['orders']);
          setCartStatus(data['status']);
        })
        .catch(error => console.error('Error fetching stock:', error));
        fetchAvailableProducts();
        setLoading(false);
    }
  }, [accessToken, id]);
  
  const fetchCartDetails = async () => {
    await fetch(`${API_URLS.GET_CART}?cart_id=${id}`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      }
    })
      .then(response => response.json())
      .then(data => {
        setTotal(data['total_amount']);
        setItems(data['orders']);
        setCartStatus(data['status']);
      })
      .catch(error => console.error('Error fetching stock:', error));
  };

  const fetchAvailableProducts = async () => {
    try {
      const response = await fetch(`${API_URLS.STOCKS}?skip=0&limit=100`);
      const data = await response.json();
      setAvailableProducts(data['products']);
    } catch (error) {
      console.error('Error fetching available products:', error);
    }
  };

  const handleAddStock = async (new_product_detail) => {
    try {
      console.log("new stock "+new_product_detail.order_counts);
      await fetch(`${API_URLS.CREATE_ORDER}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
          'cart_id': id,
          'product_id': new_product_detail.product_id,
          'counts': new_product_detail.order_counts
        })
      });

      await fetchCartDetails();
    } catch (error) {
      console.error('Error adding stock:', error);
    }
  };

  const updateItemQuantity = async (itemId, newQuantity) => {
    try {
      console.log("quantities");
      console.log(newQuantity);
      const response = await fetch(`${API_URLS.UPDATE_ORDER}?order_id=${itemId}&order_counts=${newQuantity}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        }
      });
  
      const data = await response.json();
  
      setItems(prevItems => {
        const updatedItems = prevItems.map(item =>
          item.id === itemId ? { ...item, counts: newQuantity, total_amount: item.product.price * newQuantity } : item
        );
        setTotal(updatedItems.reduce((sum, item) => sum + item.total_amount, 0));
        return updatedItems;
      });
      
    } catch (error) {
      console.error('Error updating quantity:', error);
    }
  };
  
  if (!accessToken || !id) {
    return <div className="text-center mt-4">Please sign in to view the dashboard.</div>;
  }

  return (
    <div className="row mt-4">
      <div className="col-md-7">
        <h2 className="mb-4">Cart Detail: {id}</h2>
        <CartItems 
          items={items}
          onUpdateQuantity={updateItemQuantity}
          cart_status={ cart_status }
        />
        <div className="mt-4">
          {!cart_status && (
            <Link to={`/delete-cart/${id}`} className="btn btn-danger me-2">
              Delete Cart 
            </Link>
          )}
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate('/carts/false')}
          >
            Back
          </button>
        </div>
      </div>

      
      <div className="col-md-5">
        <h2 className="mb-4">Cart Summary</h2>
        <p className="lead">Total Amount: #{cart_total}</p>
        {!cart_status &&(
          <>
        <div className="col-md-5">
            <Link to={`/checkout/${id}`}> Checkout Cart </Link>
        </div>
        
        <h2 className='my-5 text-center text-primary'>Add New Stock</h2>
        <div className='col-12'>
          <AddStockComponent
            onAddStock={handleAddStock}
            availableProducts={availableProducts}
            existingProducts={ items }
          />
        </div>

      </>
        )}
      </div>
    </div>
  );
}

export default CartEdit;
