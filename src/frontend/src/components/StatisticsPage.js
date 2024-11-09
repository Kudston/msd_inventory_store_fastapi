import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { API_URLS } from '../config/apiConfig';

const StatisticsDashboard = () => {
  const [totalAmount, setTotalAmount] = useState(0);
  const [unclearedAmount, setUnclearedAmt] = useState(0);
  const [clearedAmount, setClearedAmt] = useState(0);
  const [productsData, setProductsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const productsRef = useRef(null);
  const { accessToken } = useAuth();

  // Filter states
  const [endDate, setEndDate] = useState(new Date().toISOString().split('T')[0]);
  const [dateRangeType, setDateRangeType] = useState('days');
  const [rangeCounts, setRangeCounts] = useState(7);
  const [orderDirection, setOrderDirection] = useState('desc');
  const [orderBy, setOrderBy] = useState('amount');

  const fetchData = async () => {
    if (!accessToken) return;

    setLoading(true);
    try {
      const queryParams = new URLSearchParams({
        end_date: endDate,
        date_range_type: dateRangeType,
        range_counts: rangeCounts,
        order_direction: orderDirection,
        order_by: orderBy
      });

      const response = await fetch(
        `${API_URLS.PRODUCTS_STATISTICS}?${queryParams}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
          },
        }
      );

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setTotalAmount(data.total_amount);
      setClearedAmt(data.total_cleared_amount);
      setUnclearedAmt(data.total_uncleared_amount);
      setProductsData(data.products_list);
    } catch (error) {
      console.error("Error fetching statistics data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [accessToken, endDate, dateRangeType, rangeCounts, orderDirection, orderBy]);

  if (!accessToken) {
    return <div className="text-center mt-4">Please sign in to view the dashboard.</div>;
  }

  return (
    <div className="container mt-4">
      <h1 className="mb-4 text-center">Statistics Dashboard</h1>
      
      {/* Filter Controls */}
      <div className="card mb-4">
        <div className="card-header">
          <h5 className="card-title mb-0">Filters</h5>
        </div>
        <div className="card-body">
          <div className="row g-3">
            <div className="col-md">
              <label className="form-label">End Date</label>
              <input
                type="date"
                className="form-control"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
            
            <div className="col-md">
              <label className="form-label">Range Type</label>
              <select
                className="form-select"
                value={dateRangeType}
                onChange={(e) => setDateRangeType(e.target.value)}
              >
                <option value="days">Days</option>
                <option value="weeks">Weeks</option>
                <option value="months">Months</option>
              </select>
            </div>
            
            <div className="col-md">
              <label className="form-label">Range Count</label>
              <input
                type="number"
                className="form-control"
                value={rangeCounts}
                onChange={(e) => setRangeCounts(e.target.value)}
                min="1"
                max="100"
              />
            </div>
            
            <div className="col-md">
              <label className="form-label">Order By</label>
              <select
                className="form-select"
                value={orderBy}
                onChange={(e) => setOrderBy(e.target.value)}
              >
                <option value="amount">Amount</option>
                <option value="counts">Quantities</option>
              </select>
            </div>
            
            <div className="col-md">
              <label className="form-label">Direction</label>
              <select
                className="form-select"
                value={orderDirection}
                onChange={(e) => setOrderDirection(e.target.value)}
              >
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="row mb-4">
        <div className="col-md-4 mb-3">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title">Total Amount</h5>
              <p className="display-6">${totalAmount.toFixed(2)}</p>
            </div>
          </div>
        </div>
        
        <div className="col-md-4 mb-3">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title">Cleared Amount</h5>
              <p className="display-6">${clearedAmount.toFixed(2)}</p>
            </div>
          </div>
        </div>

        <div className="col-md-4 mb-3">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title">Uncleared Amount</h5>
              <p className="display-6">${unclearedAmount.toFixed(2)}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Products Table */}
      <div className="card">
        <div className="card-header d-flex justify-content-between align-items-center">
          <h5 className="mb-0">Products Statistics</h5>
          <div>
            <button 
              onClick={() => productsRef.current?.scrollBy(0, -200)} 
              className="btn btn-outline-secondary btn-sm me-2"
            >
              ↑
            </button>
            <button 
              onClick={() => productsRef.current?.scrollBy(0, 200)} 
              className="btn btn-outline-secondary btn-sm"
            >
              ↓
            </button>
          </div>
        </div>
        
        <div className="card-body p-0">
          <div 
            ref={productsRef} 
            style={{ height: '400px', overflowY: 'auto' }}
          >
            {loading ? (
              <div className="text-center py-4">
                <div className="spinner-border text-primary" role="status">
                  <span className="visually-hidden">Loading...</span>
                </div>
              </div>
            ) : (
              <table className="table table-hover mb-0">
                <thead className="table-light">
                  <tr>
                    <th className="px-3">Product</th>
                    <th className="px-3">Quantity</th>
                    <th className="px-3">Total Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {productsData.map((product) => (
                    <tr key={product.id}>
                      <td className="px-3">{product.title}</td>
                      <td className="px-3">{product.total_counts}</td>
                      <td className="px-3">${(product.total_amount).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatisticsDashboard;