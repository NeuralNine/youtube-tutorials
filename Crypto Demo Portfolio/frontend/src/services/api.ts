import axios from 'axios';

const API_URL = 'http://localhost:8000';

// Types
export interface UserCreate {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface AddMoney {
  amount: number;
}

export interface TradeAsset {
  symbol: string;
  quantity: number;
}

export interface Asset {
  symbol: string;
  quantity: number;
  current_price: number;
  total_value: number;
  performance_abs: number;
  performance_rel: number;
}

export interface Portfolio {
  total_added_money: number;
  available_money: number;
  total_value: number;
  performance_abs: number;
  performance_rel: number;
  assets: Asset[];
}

// API client setup
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Set auth token for requests
export const setAuthToken = (token: string) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

// API functions
export const register = async (userData: UserCreate) => {
  return api.post('/register', userData);
};

export const login = async (username: string, password: string) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  
  const response = await api.post<LoginResponse>('/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  
  if (response.data.access_token) {
    setAuthToken(response.data.access_token);
    localStorage.setItem('token', response.data.access_token);
  }
  
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('token');
  setAuthToken('');
};

export const checkAuth = () => {
  const token = localStorage.getItem('token');
  if (token) {
    setAuthToken(token);
    return true;
  }
  return false;
};

export const addMoney = async (amount: number) => {
  return api.post('/add-money', { amount });
};

export const buyAsset = async (symbol: string, quantity: number) => {
  return api.post('/buy', { symbol, quantity });
};

export const sellAsset = async (symbol: string, quantity: number) => {
  return api.post('/sell', { symbol, quantity });
};

export const getPortfolio = async () => {
  return api.get<Portfolio>('/portfolio');
};

export default {
  register,
  login,
  logout,
  checkAuth,
  addMoney,
  buyAsset,
  sellAsset,
  getPortfolio,
};
