import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { API_URLS } from '../config/apiConfig';

function SignIn() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { setAccessToken } = useAuth();
  const navigate = useNavigate();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);
      
      const response = await fetch(API_URLS.SIGN_IN, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Sign in failed');
      }
      
      const data = await response.json();
      if (data.access_token) {
        setAccessToken(data.access_token);
        navigate('/');
      } else {
        alert('Sign in failed. Please try again.');
      }
    } catch (error) {
      console.error('Sign in error:', error);
      alert('An error occurred. Please try again.');
    }
  };
  
  return (
    <div className="container mt-5">
      <h2>Sign In</h2>
      <form onSubmit={handleSubmit} className='col-5'>
        <div className="mb-3">
          <label htmlFor="username" className="form-label">Username</label>
          <input
            type="text"
            className="form-control"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">Sign In</button>
      </form>
      <div className="mt-3">
        <p>Don't have an account? <Link to="/signup">Sign up here</Link></p>
      </div>
    </div>
  );
}

export default SignIn;