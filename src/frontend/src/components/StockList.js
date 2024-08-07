import React from 'react';

function StockList({ stocks }) {
  return (
    <div className="card">
      <div className="card-body">
        <h5 className="card-title">Current Stock</h5>
        <ul className="list-group">
          {stocks.map(stock => (
            <li key={stock.id} className="list-group-item d-flex justify-content-between align-items-center my-2">
              {stock.title}
              <span className="badge bg-primary rounded-pill">{stock.units}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default StockList;