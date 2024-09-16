import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { API_URLS } from '../config/apiConfig';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: '',
    is_admin: false,
    super_admin_token: '',
  });
  const navigate = useNavigate();

  const [passwordError, setPasswordError] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: type === 'checkbox' ? checked : value
    }));

    if (name === 'password') {
      if (value !== formData.confirmPassword) {
        setPasswordError("Passwords don't match");
      } else {
        setPasswordError('');
      }
    }
  };

  const handle_password_check = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));

    if (name === 'confirmPassword') {
      if (value !== formData.password) {
        setPasswordError("Passwords don't match");
      } else {
        setPasswordError('');
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (passwordError) {
      return;  // Prevent form submission if passwords don't match
    }
    console.log('Form submitted:', formData);
    try {
      const response = await fetch(API_URLS.SIGN_UP, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });
      
      if (response.status === 200) {
        alert('User created successfully!');
        navigate('/signin');  // Redirect to signin page
      } else {
        const data = await response.json();
        alert(`Error: ${data.message || 'Failed to create user'}`);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while creating the user');
    }
  };

  return (
    <div className="container mt-5">
      <h2>Register</h2>
      <form onSubmit={handleSubmit} className="col-5">
        <div className="mb-3">
          <label htmlFor="username" className="form-label">Username</label>
          <input
            type="text"
            className="form-control"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
          <input
            type="password"
            className={`form-control ${passwordError ? 'is-invalid' : ''}`}
            id="confirmPassword"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handle_password_check}
            required
          />
          {passwordError && <div className="invalid-feedback">{passwordError}</div>}
        </div>
        <div className="mb-3 form-check">
          <input
            type="checkbox"
            className="form-check-input"
            id="is_admin"
            name="is_admin"
            checked={formData.is_admin}
            onChange={handleChange}
          />
          <label className="form-check-label" htmlFor="is_admin">Register as admin</label>
        </div>
        {formData.is_admin && (
          <div className="mb-3">
            <label htmlFor="super_admin_token" className="form-label">Admin Token</label>
            <input
              type="text"
              className="form-control"
              id="super_admin_token"
              name="super_admin_token"
              value={formData.super_admin_token}
              onChange={handleChange}
              required
            />
          </div>
        )}
        <button type="submit" className="btn btn-primary" disabled={passwordError}>Register</button>
      </form>
      <div className="mt-3">
        <p>Already have an account? <Link to="/signin">Sign in here</Link></p>
      </div>
    </div>
  );
};

export default RegisterPage;