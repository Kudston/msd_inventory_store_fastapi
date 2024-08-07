const API_BASE_URL = "http://172.19.0.3:8500"; // Replace with your actual API base URL

export const API_URLS = {
  STOCKS: `${API_BASE_URL}/products`,
  RECENT_ORDERS: `${API_BASE_URL}/orders/get-carts`,
  SIGN_IN: `${API_BASE_URL}/users/token`,
  EDIT_STOCKS: `${API_BASE_URL}/products/product-update`,
  GET_STOCK: `${API_BASE_URL}/products/product`,
  GET_CART: `${API_BASE_URL}/orders/get-cart`,
  GET_CARTS: `${API_BASE_URL}/orders/get-carts`,
  ADD_PRODUCT: `${API_BASE_URL}/products/product-create`,
  CREATE_CART: `${API_BASE_URL}/orders/cart-initiate`,
  DELETE_CART: `${API_BASE_URL}/orders/delete-cart`,
  UPDATE_ORDER: `${API_BASE_URL}/orders/update-units`,
  CREATE_ORDER: `${API_BASE_URL}/orders`,
  CHECKOUT_CART: `${API_BASE_URL}/orders/checkout`,
  // Add more endpoints as needed
};