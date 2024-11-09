import React, { useState, useEffect, useRef } from 'react';

const AddStockComponent = ({ onAddStock, availableProducts, existingProducts }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortOrder, setSortOrder] = useState('asc');
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [quantities, setQuantities] = useState({});
  const [hiddenProducts, setHiddenProducts] = useState({});
  const searchInputRef = useRef(null);

  useEffect(() => {

    if (!Array.isArray(availableProducts)) return;

    const initialHiddenProducts = existingProducts.reduce((acc, product) => {
      acc[product.product_id] = true;
      return acc;
    }, {});

    setHiddenProducts(initialHiddenProducts);
    const filtered = availableProducts.filter(product =>
      product.title.toLowerCase().includes(searchTerm.toLowerCase())
    );
    
    const sorted = filtered.sort((a, b) => {
      if (sortOrder === 'asc') {
        return a.title.localeCompare(b.title);
      } else {
        return b.title.localeCompare(a.title);
      }
    });

    setFilteredProducts(sorted);
  }, [searchTerm, sortOrder, availableProducts, existingProducts]);

  if (!Array.isArray(availableProducts)) {
    return (
      <div>
        <p>Loading...</p>
      </div>
    );
  }

  const handleAddClick = (product) => {
    const quantity = quantities[product.id] || 1;
    onAddStock({
      product_id: product.id,
      order_counts: quantity
    });
    setHiddenProducts(prevHiddenProducts => ({
      ...prevHiddenProducts,
      [product.id]: true
    }));
  };

  const handleQuantityChange = (productId, value) => {
    setQuantities(prevQuantities => ({
      ...prevQuantities,
      [productId]: value
    }));
  };

  return (
    <div className="container mt-4">
      <div className="row mb-3">
        <div className="col-md-6">
          <input
            ref={searchInputRef}
            type="text"
            className="form-control"
            placeholder="Search products..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="col-md-6">
          <select
            className="form-select"
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value)}
          >
            <option value="asc">Sort A-Z</option>
            <option value="desc">Sort Z-A</option>
          </select>
        </div>
      </div>
      <div className="row">
        <div className="col-12">
          <ul className="list-group">
            {filteredProducts.map((product) => (
              !hiddenProducts[product.id] && (
                <li
                  key={product.id}
                  className="list-group-item d-flex justify-content-between align-items-center my-2"
                >
                  <span>{product.title}</span>
                  <div className="d-flex align-items-center">
                    <input
                      type="number"
                      className="form-control me-2"
                      placeholder="Quantity"
                      min={1}
                      max={product.units}
                      value={quantities[product.id] || ''}
                      onChange={(e) => handleQuantityChange(product.id, parseInt(e.target.value))}
                    />
                    <button
                      className="btn btn-primary btn-sm"
                      onClick={() => handleAddClick(product)}
                    >
                      Add
                    </button>
                  </div>
                </li>
              )
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default AddStockComponent;
