import React, { useState } from 'react';
import { API_URLS } from '../config/apiConfig';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const AddProductForm = () => {
  const navigate = useNavigate();
  const { accessToken } = useAuth();
  const [form, setForm] = useState({
    title: '',
    category: '',
    units: '',
    price: '',
  });
  const categories = [
    'Electronics',
    'Fashion',
    'Home Goods',
    'Sports',
    'Toys',
  ];
  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch(API_URLS.ADD_PRODUCT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(form),
      });
      const data = await response.json();
      console.log(data);
      navigate('/products');
      // Handle success response
    } catch (error) {
      console.error(error);
      // Handle error response
    }
  };
  
  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value,
    });
  };

  return (
    <form onSubmit={handleSubmit} className='container col-5'>
      <div className="mb-3">
        <label className="form-label">Title</label>
        <input
          type="text"
          name="title"
          value={form.title}
          onChange={handleChange}
          className="form-control"
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Category</label>
        <select
          name="category"
          value={form.category}
          onChange={handleChange}
          className="form-select"
        >
          <option value="">Select a category</option>
          {categories.map((category) => (
            <option key={category} value={category}>
              {category}
            </option>
          ))}
        </select>
      </div>
      <div className="mb-3">
        <label className="form-label">Units</label>
        <input
          type="number"
          name="units"
          value={form.units}
          onChange={handleChange}
          className="form-control"
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Price</label>
        <input
          type="number"
          name="price"
          value={form.price}
          onChange={handleChange}
          className="form-control"
        />
      </div>
      <button type="submit" className="btn btn-primary">
        Add Product
      </button>
    </form>
  );
};

export default AddProductForm;