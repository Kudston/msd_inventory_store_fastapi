import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { API_URLS } from '../config/apiConfig';

function Carts() {
  const { uncleared } = useParams();
  const [carts, setCarts] = useState([]);
  const { accessToken } = useAuth();
  const [statusFilter, setStatusFilter] = useState('');
  const [amountFilter, setAmountFilter] = useState('');
  const [amountComparison, setAmountComparison] = useState('greater');
  const [sortOrder, setSortOrder] = useState('desc');
  const [showModal, setShowModal] = useState(false);
  const [currentCartId, setCurrentCartId] = useState(null);

  useEffect(() => {
    if (accessToken) {
      const unclearedParam = uncleared === 'true';
      if (unclearedParam) {
        setStatusFilter('uncleared');
      }
      fetch(`${API_URLS.GET_CARTS}?uncleared_only=${unclearedParam}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        }
      })
        .then(response => response.json())
        .then(data => setCarts(data['carts']))
        .catch(error => console.error('Error fetching carts:', error));
    }
  }, [accessToken, uncleared]);

  const handleCheckout = (cartId) => {
    setCurrentCartId(cartId);
    setShowModal(true);
  };

  const confirmCheckout = () => {
    fetch(`${API_URLS.CHECKOUT_CART}?cart_id=${currentCartId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      }
    })
      .then(response => response.json())
      .then(data => {
        // Handle successful checkout, e.g., update the cart status
        setCarts(prevCarts =>
          prevCarts.map(cart =>
            cart.id === currentCartId ? { ...cart, status: true } : cart
          )
        );
        setShowModal(false);
      })
      .catch(error => {
        console.error('Error during checkout:', error);
        setShowModal(false);
      });
  };

  const filteredCarts = carts
    .filter(cart => {
      if (statusFilter && cart.status !== (statusFilter === 'cleared')) {
        return false;
      }
      if (amountFilter) {
        const amountCondition = parseFloat(amountFilter);
        if (amountComparison === 'greater' && cart.total_amount <= amountCondition) {
          return false;
        }
        if (amountComparison === 'less' && cart.total_amount >= amountCondition) {
          return false;
        }
      }
      return true;
    })
    .sort((a, b) => {
      if (sortOrder === 'asc') {
        return a.total_amount - b.total_amount;
      } else {
        return b.total_amount - a.total_amount;
      }
    });

  return (
    <div className="container mt-4">
      <h2 className="text-center mb-4">Carts</h2>
      <div className="mb-4">
        <div className="row">
          <div className="col-md-4">
            <select 
              className="form-select"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              disabled={uncleared === 'true'}
            >
              <option value="">All</option>
              <option value="cleared">Cleared</option>
              <option value="uncleared">Uncleared</option>
            </select>
          </div>
          <div className="col-md-4">
            <input 
              type="number"
              className="form-control"
              placeholder="Total amount"
              value={amountFilter}
              onChange={(e) => setAmountFilter(e.target.value)}
            />
          </div>
          <div className="col-md-4">
            <select 
              className="form-select"
              value={amountComparison}
              onChange={(e) => setAmountComparison(e.target.value)}
            >
              <option value="greater">Greater than</option>
              <option value="less">Less than</option>
            </select>
          </div>
          <div className="col-md-4 mt-2">
            <select 
              className="form-select"
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value)}
            >
              <option value="asc">Sort by amount: Low to High</option>
              <option value="desc">Sort by amount: High to Low</option>
            </select>
          </div>
        </div>
      </div>
      <div className="row" style={{ maxHeight: '500px', overflowY: 'scroll' }}>
        <div className="col-md-12">
          <ul className="list-group">
            {filteredCarts.map(cart => (
              <li key={cart.id} className="list-group-item my-3 position-relative">
                <div className="d-flex justify-content-between align-items-center">
                  <h3 className="mb-0">Cart ID: {cart.id}</h3>
                  <span className={`badge ${cart.status ? 'bg-success' : 'bg-danger'}`}>
                    {cart.status ? 'Cleared' : 'Uncleared'}
                  </span>
                </div>
                <div className="mt-2">
                  <strong>Total Amount:</strong> ${cart.total_amount > 0 ? cart.total_amount.toFixed(2) : '0.00'}
                </div>
                {!cart.status && (
                  <div className="mt-2 d-flex">
                    <Link to={`/cart-edit/${cart.id}`} className="btn btn-primary btn-sm me-3">Update</Link>
                    <button
                      onClick={() => handleCheckout(cart.id)}
                      className="btn btn-success btn-sm me-3"
                    >
                      Checkout
                    </button>
                    <Link 
                      to={`/delete-cart/${cart.id}`} 
                      className="btn btn-danger btn-sm position-absolute"
                      style={{ bottom: '10px', right: '10px' }}
                    >
                      Delete
                    </Link>
                  </div>
                )}
                {cart.status && (
                  <div className="mt-2">
                    <span className="text-muted">Cart is pending clearance</span>
                  </div>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Confirmation Modal */}
      {showModal && (
        <div className="modal show" aria-hidden="true" tabIndex="-1" style={{ display: 'block' }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Confirm Checkout</h5>
                <button type="button" className="btn-close" onClick={() => setShowModal(false)}></button>
              </div>
              <div className="modal-body">
                <p>Are you sure you want to checkout this cart?</p>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="button" className="btn btn-primary" onClick={confirmCheckout}>Confirm</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Carts;
