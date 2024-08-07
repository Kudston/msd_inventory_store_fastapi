import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { API_URLS } from '../config/apiConfig';
import Button from './Button';  // Import the custom Button component

function Products() {
  const [stocks, setStocks] = useState([]);
  const [filteredStocks, setFilteredStocks] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(5);
  const [sortKey, setSortKey] = useState('title');
  const [sortOrder, setSortOrder] = useState('asc');
  const { accessToken } = useAuth();

  useEffect(() => {
    if (accessToken) {
      fetch(API_URLS.STOCKS, {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      })
        .then(response => response.json())
        .then(data => {
          setStocks(data['products']);
          setFilteredStocks(data['products']);
        })
        .catch(error => console.error('Error fetching stocks:', error));
    }
  }, [accessToken]);

  useEffect(() => {
    const results = stocks.filter(stock =>
      stock.title.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredStocks(results);
    setCurrentPage(1);
  }, [searchTerm, stocks]);

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSort = (key) => {
    const isAsc = sortKey === key && sortOrder === 'asc';
    setSortKey(key);
    setSortOrder(isAsc ? 'desc' : 'asc');
    
    const sortedStocks = [...filteredStocks].sort((a, b) => {
      if (a[key] < b[key]) return isAsc ? 1 : -1;
      if (a[key] > b[key]) return isAsc ? -1 : 1;
      return 0;
    });
    
    setFilteredStocks(sortedStocks);
  };

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredStocks.slice(indexOfFirstItem, indexOfLastItem);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <div className="container mt-4">
      <h2>Products</h2>
      <div className="row">
        <div className="col-md-8">
          <p>Product information and management tools can go here.</p>
        </div>
        <div className="col-md-8">
          <h3>Inventory Stocks</h3>
          <div className="mb-3">
            <input
              type="text"
              placeholder="Search products..."
              value={searchTerm}
              onChange={handleSearch}
              className="form-control"
            />
          </div>
          <div className="mb-3">
            <Button onClick={() => handleSort('title')} className="mr-2">
              Sort by Name {sortKey === 'title' && (sortOrder === 'asc' ? '↑' : '↓')}
            </Button>
            <Button onClick={() => handleSort('createdAt')} className="mr-2">
              Sort by Date {sortKey === 'createdAt' && (sortOrder === 'asc' ? '↑' : '↓')}
            </Button>
          </div>
          <ul className="list-group overflow-auto" style={{ maxHeight: '400px' }}>
            <li className="list-group-item d-flex justify-content-between align-items-center my-2">
              <h2 className="col-3">Name</h2>
              <div className="col-3">Quantity</div>
              <div className="col-3">Created At</div>
              <div className="col-3">Update</div>
            </li>
            {currentItems.map(stock => (
              <li key={stock.id} className="list-group-item d-flex justify-content-between align-items-center my-2">
                <h2 className="col-3 text-truncate">{stock.title}</h2>
                <div className="col-3">{stock.units}</div>
                <div className="col-3">{new Date(stock.date_created).toLocaleDateString()}</div>
                <Link to={`/stock-edit/${stock.id}`} className="btn btn-primary btn-sm col-3">Edit</Link>
              </li>
            ))}
          </ul>
          <div className="d-flex justify-content-between mt-3">
            <Button 
              onClick={() => paginate(currentPage - 1)} 
              disabled={currentPage === 1}
            >
              Previous
            </Button>
            <Button 
              onClick={() => paginate(currentPage + 1)} 
              disabled={indexOfLastItem >= filteredStocks.length}
            >
              Next
            </Button>
          </div>
          <Link to={`/add-product`} className="btn btn-primary mt-3">Add New Products</Link>
        </div>
      </div>
    </div>
  );
}

export default Products;
