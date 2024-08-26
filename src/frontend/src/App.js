import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import HomePage from './components/HomePage';
import Carts from './components/Carts';
import Products from './components/Products';
import SignIn from './components/SignIn';
import StockEdit from './components/StockEdit';
import CartEdit from './components/CartEdit';
import AddProductForm from './components/AddProduct';
import CartCreate from './components/NewOrder';
import DeleteCartComponent from './components/DeleteCart';
import AddStockModal from './components/AddStocksToCart';
import CheckoutPage from './components/CheckoutPage.js';
import RegisterPage from './components/SignUp.js';

function NavBar() {
  const { accessToken, setAccessToken } = useAuth();
  const handleSignOut = () => {
    setAccessToken(null);
  };

  return (
    <header className='bg-primary text-white'>
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container">
          <Link className="navbar-brand text-primary fs-4" to="/">DominionInventory</Link>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse justify-content-end" id="navbarNav">
            <ul className="navbar-nav">
              <li className="nav-item">
                <Link className="nav-link text-primary fs-5" to="/carts/false">Carts</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link text-primary fs-5" to="/products">Products</Link>
              </li>
              {accessToken ? (
                <li className="nav-item">
                  <button className="nav-link btn btn-link text-primary fs-5" onClick={handleSignOut}>Sign Out</button>
                </li>
              ) : (
                <li className="nav-item">
                  <Link className="nav-link text-primary fs-5" to="/signin">Sign In</Link>
                </li>
              )}
            </ul>
          </div>
        </div>
      </nav>
      <div className='container d-flex flex-column mb-3 text-white display-5 text-center'>
        <span>Welcome to MSD STORE</span>
        <span>Store of Quality</span>
      </div>
    </header>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <NavBar />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/carts/:uncleared" element={<Carts />} />
            <Route path="/products" element={<Products />} />
            <Route path="/signin" element={<SignIn />} />
            <Route path="/stock-edit/:id" element={<StockEdit />} />
            <Route path="/cart-edit/:id" element={<CartEdit />} />
            <Route path="/add-product" element={<AddProductForm />} />
            <Route path="/cart-create" element={<CartCreate />} />
            <Route path="/delete-cart/:id" element={<DeleteCartComponent />} />
            <Route path="/add-cart-stock/:id" element={<AddStockModal />} />
            <Route path="/checkout/:id" element={<CheckoutPage />} />
            <Route path='/signup' element={<RegisterPage />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
