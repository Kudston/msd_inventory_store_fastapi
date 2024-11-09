import React from 'react';

function CartItems({ items, onUpdateQuantity, cart_status }) {
  const handleIncrease = (item) => {
    const newQuantity = item.counts + 1;
    item.counts = newQuantity;
    onUpdateQuantity(item.id, newQuantity);
  };

  const handleDecrease = (item) => {
    if (item.counts > 0) {
      const newQuantity = item.counts - 1;
      item.counts = newQuantity;
      onUpdateQuantity(item.id, newQuantity);
    }
  };

  const handleInputChange = (item, event) => {
    const newQuantity = parseInt(event.target.value, 10);
    if (!isNaN(newQuantity) && newQuantity >= 0) {
      onUpdateQuantity(item.id, newQuantity);
    }
  };

  return (
    <div className="card">
      <div className="card-body">
        <h5 className="card-title">Cart Items</h5>
        <ul className="list-group">
          {items.map(item => (
            <li key={item.id} className="list-group-item">
              <div>Title <span className='m-2'>#{item.product.title}</span></div>
              <div>Total <span className='m-2'>#{item.total_amount}</span></div>
              <div className="d-flex align-items-center mb-3">
               {!cart_status && (<> <button 
                  className="btn btn-secondary me-2" 
                  onClick={() => handleDecrease(item)}
                >
                  -
                </button>
                </>
              )}
                <input
                  type="number"
                  className="form-control w-auto"
                  value={item.counts}
                  onChange={(e) => handleInputChange(item, e)}
                />
                {!cart_status && (
                  <>
                <button 
                  className="btn btn-secondary ms-2" 
                  onClick={() => handleIncrease(item)}
                >
                  +
                </button>
                </>
                )}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default CartItems;
