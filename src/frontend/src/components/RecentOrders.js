import React from 'react';
import { Link } from 'react-router-dom';

function RecentOrders({ orders }) {
  return (
    <div className="card">
      <div className="card-body">
        <h5 className="card-title">Recent Orders</h5>
        <ul className="list-group">
          {orders.map(order => (
            <li key={order.id} className="list-group-item my-2">
              <div>Order #{order.id}</div>
              <small>Date: {new Date(order.date_created).toLocaleDateString()}</small>
              <div>Total #{(order.total_amount>0)?order.total_amount:0}</div>
              <Link to={`/cart-edit/${order.id}`} className="btn btn-primary btn-sm">Details</Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default RecentOrders;