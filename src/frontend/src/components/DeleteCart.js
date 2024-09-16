import React, { useState,  } from 'react';
import { useAuth } from '../context/AuthContext';
import { useParams, useNavigate } from 'react-router-dom';
import { API_URLS } from '../config/apiConfig';

const DeleteCartComponent = () => {
    const { id } = useParams();
    const { accessToken } = useAuth();
    const navigate = useNavigate();
    const [isModalOpen, setIsModalOpen] = useState(false);  
    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);
  
    const handleDelete = () => {
      fetch(`${API_URLS.DELETE_CART}/?cart_id=${id}`,{
        method: "DELETE",
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
      })
      navigate('/carts/false');
      closeModal();
    };

  return (
    <div className="p-3 d-flex flex-column justify-content-center align-items-center">
     <h2 className='text-primary mb-4'>You are about to delete cart with id: {id}</h2>
     <h2 className='text-danger mb-5'>Click the delete icon below to confirm operation</h2>
      <button className="btn btn-danger d-flex col-4 align-items-center" onClick={openModal}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="me-2"
        >
          <path d="M3 6h18"></path>
          <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
          <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
          <line x1="10" y1="11" x2="10" y2="17"></line>
          <line x1="14" y1="11" x2="14" y2="17"></line>
        </svg>
        Delete Cart
      </button>

      {isModalOpen && (
        <div className="modal d-block" tabIndex="-1" role="dialog">
          <div className="modal-dialog" role="document">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Confirm Deletion</h5>
                <button type="button" className="btn-close" onClick={closeModal} aria-label="Close"></button>
              </div>
              <div className="modal-body">
                <p>Are you sure you want to delete your cart? This action cannot be undone. This will permanently delete the cart and remove the data from our servers.</p>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={closeModal}>Cancel</button>
                <button type="button" className="btn btn-danger" onClick={handleDelete}>Delete</button>
              </div>
            </div>
          </div>
        </div>
      )}
      {isModalOpen && <div className="modal-backdrop fade show"></div>}
    </div>
  );
};

export default DeleteCartComponent;