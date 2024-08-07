import React from 'react';

function InventoryStats({ stats }) {
  return (
    <div className="row mt-4">
      <div className="col-md-6">
        <div className="card">
          <div className="card-body">
            <h5 className="card-title">Total Stock Items</h5>
            <p className="card-text display-4">{stats.totalItems}</p>
          </div>
        </div>
      </div>
      <div className="col-md-6">
        <div className="card">
          <div className="card-body">
            <h5 className="card-title">Finished Stocks</h5>
            <p className="card-text display-4">{stats.finishedStocks}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default InventoryStats;