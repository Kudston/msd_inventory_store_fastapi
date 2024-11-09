import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { API_URLS } from '../config/apiConfig';
import InventoryStats from './InventoryStats';
import StockList from './StockList';
import RecentOrders from './RecentOrders';
import { Link } from 'react-router-dom';
import Button from './Button';

function HomePage() {
  const [stocks, setStocks] = useState([]);
  const [orders, setOrders] = useState([]);
  const [stats, setStats] = useState({ totalItems: 0, finishedStocks: 0 });
  const [unclearedOrdersCount, setUnclearedOrdersCount] = useState(0);
  const { accessToken } = useAuth();

  const stocksRef = useRef(null);
  const ordersRef = useRef(null);

  useEffect(() => {
    if (accessToken) {
      // Fetch stocks
      alert(process.env.REACT_APP_WEBSITE_NAME);
      fetch(`${API_URLS.STOCKS}?skip=0&limit=1000`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        }
      })
        .then(response => response.json())
        .then(data => {
          data = data['products'];
          setStocks(data);
          const totalItems = data.reduce((sum, item) => sum + item.units, 0);
          const finishedStocks = data.filter(item => item.units === 0).length;
          setStats({ totalItems, finishedStocks });
        });

      // Fetch orders
      fetch(`${API_URLS.GET_CARTS}?skip=0&limit=1000&order_direction=desc&order_by=date_modified`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        }
      })
        .then(response => response.json())
        .then(data => {
          data = data['carts'];
          setOrders(data);
          const unclearedOrders = data.filter(order => !order.cleared).length;
          setUnclearedOrdersCount(unclearedOrders);
        });
    }
  }, [accessToken]);

  const scroll = (ref, direction) => {
    const scrollAmount = 200;
    if (ref.current) {
      ref.current.scrollTop += direction * scrollAmount;
    }
  };

  if (!accessToken) {
    return <div className="container mt-4">Please sign in to view the dashboard.</div>;
  }

  return (
    <div className="container-fluid mt-4">
      <h1 className="mb-4 text-center">Inventory Dashboard</h1>
      
      <div className="row mb-4">
        <div className="col-md-6">
          <InventoryStats stats={stats} />
        </div>
        <div className="col-md-6">
          <div className="d-flex justify-content-between align-items-center">
            <Link to={'/cart-create'} className='btn btn-primary'>Create New Order</Link>
            <Link to={'/statistics'} className='btn btn-primary'>statistics</Link>
            <Link to={'/carts/true'} className='btn btn-warning'>
              Uncleared Orders <span className="badge bg-secondary">{unclearedOrdersCount}</span>
            </Link>
          </div>
        </div>
      </div>

      <div className="row">
        <div className="col-md-6 mb-4">
          <div className="card">
            <div className="card-header d-flex justify-content-between align-items-center">
              <h2 className="mb-0">Current Stocks</h2>
              <div>
                <Button onClick={() => scroll(stocksRef, -1)} variant="outline-secondary" size="sm" className="me-2">↑</Button>
                <Button onClick={() => scroll(stocksRef, 1)} variant="outline-secondary" size="sm">↓</Button>
              </div>
            </div>
            <div className="card-body" ref={stocksRef} style={{ height: '400px', overflowY: 'auto' }}>
              <StockList stocks={stocks} />
            </div>
          </div>
        </div>

        <div className="col-md-6 mb-4">
          <div className="card">
            <div className="card-header d-flex justify-content-between align-items-center">
              <h2 className="mb-0">Recent Orders</h2>
              <div>
                <Button onClick={() => scroll(ordersRef, -1)} variant="outline-secondary" size="sm" className="me-2">↑</Button>
                <Button onClick={() => scroll(ordersRef, 1)} variant="outline-secondary" size="sm">↓</Button>
              </div>
            </div>
            <div className="card-body" ref={ordersRef} style={{ height: '400px', overflowY: 'auto' }}>
              <RecentOrders orders={orders} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;

