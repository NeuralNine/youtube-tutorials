import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getPortfolio, buyAsset, sellAsset, addMoney } from '../services/api';
import type { Portfolio, Asset } from '../services/api';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const navigate = useNavigate();
  const { logout: authLogout } = useAuth();
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Transaction states
  const [buySymbol, setBuySymbol] = useState('');
  const [buyQuantity, setBuyQuantity] = useState('');
  const [sellSymbol, setSellSymbol] = useState('');
  const [sellQuantity, setSellQuantity] = useState('');
  const [addMoneyAmount, setAddMoneyAmount] = useState('');
  
  // Modal states
  const [showBuyModal, setShowBuyModal] = useState(false);
  const [showSellModal, setShowSellModal] = useState(false);
  const [showAddMoneyModal, setShowAddMoneyModal] = useState(false);
  const [transactionLoading, setTransactionLoading] = useState(false);

  useEffect(() => {
    fetchPortfolio();
  }, []);

  const fetchPortfolio = async () => {
    try {
      setLoading(true);
      const response = await getPortfolio();
      setPortfolio(response.data);
      setError('');
    } catch (err: any) {
      setError('Failed to load portfolio data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleBuy = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!buySymbol || !buyQuantity) return;
    
    try {
      setTransactionLoading(true);
      await buyAsset(buySymbol.toUpperCase(), Number(buyQuantity));
      await fetchPortfolio();
      setShowBuyModal(false);
      setBuySymbol('');
      setBuyQuantity('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to buy asset');
    } finally {
      setTransactionLoading(false);
    }
  };

  const handleSell = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!sellSymbol || !sellQuantity) return;
    
    try {
      setTransactionLoading(true);
      await sellAsset(sellSymbol.toUpperCase(), Number(sellQuantity));
      await fetchPortfolio();
      setShowSellModal(false);
      setSellSymbol('');
      setSellQuantity('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to sell asset');
    } finally {
      setTransactionLoading(false);
    }
  };

  const handleAddMoney = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!addMoneyAmount) return;
    
    try {
      setTransactionLoading(true);
      await addMoney(Number(addMoneyAmount));
      await fetchPortfolio();
      setShowAddMoneyModal(false);
      setAddMoneyAmount('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to add money');
    } finally {
      setTransactionLoading(false);
    }
  };

  const handleLogout = () => {
    authLogout();
    navigate('/login');
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const formatPercentage = (value: number) => {
    return `${value > 0 ? '+' : ''}${value.toFixed(2)}%`;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Trading Dashboard</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-700">{error}</div>
          </div>
        )}

        {portfolio && (
          <>
            {/* Portfolio Overview */}
            <div className="bg-white rounded-lg shadow p-6 mb-6">
              <h2 className="text-xl font-semibold mb-4">Portfolio Overview</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-500">Total Value</p>
                  <p className="text-2xl font-bold">{formatCurrency(portfolio.total_value)}</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-500">Available Cash</p>
                  <p className="text-2xl font-bold">{formatCurrency(portfolio.available_money)}</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-500">Total Added</p>
                  <p className="text-2xl font-bold">{formatCurrency(portfolio.total_added_money)}</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-500">Performance</p>
                  <p className={portfolio.performance_abs >= 0 ? "text-2xl font-bold text-green-600" : "text-2xl font-bold text-red-600"}>
                    {formatCurrency(portfolio.performance_abs)} ({formatPercentage(portfolio.performance_rel)})
                  </p>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-wrap gap-4 mb-6">
              <button
                onClick={() => setShowBuyModal(true)}
                className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Buy Asset
              </button>
              <button
                onClick={() => setShowSellModal(true)}
                className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Sell Asset
              </button>
              <button
                onClick={() => setShowAddMoneyModal(true)}
                className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
              >
                Add Money
              </button>
            </div>

            {/* Assets Table */}
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <h2 className="text-xl font-semibold p-6 pb-0">Your Assets</h2>
              {portfolio.assets.length === 0 ? (
                <div className="p-6 text-center text-gray-500">
                  You don't have any assets yet. Start buying some!
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Symbol</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantity</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Current Price</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Value</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Performance ($)</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Performance (%)</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {portfolio.assets.map((asset: Asset) => (
                        <tr key={asset.symbol}>
                          <td className="px-6 py-4 whitespace-nowrap font-medium">{asset.symbol}</td>
                          <td className="px-6 py-4 whitespace-nowrap">{asset.quantity}</td>
                          <td className="px-6 py-4 whitespace-nowrap">{formatCurrency(asset.current_price)}</td>
                          <td className="px-6 py-4 whitespace-nowrap">{formatCurrency(asset.total_value)}</td>
                          <td className={asset.performance_abs >= 0 ? "px-6 py-4 whitespace-nowrap text-green-600" : "px-6 py-4 whitespace-nowrap text-red-600"}>
                            {formatCurrency(asset.performance_abs)}
                          </td>
                          <td className={asset.performance_rel >= 0 ? "px-6 py-4 whitespace-nowrap text-green-600" : "px-6 py-4 whitespace-nowrap text-red-600"}>
                            {formatPercentage(asset.performance_rel)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </>
        )}
      </main>

      {/* Buy Modal */}
      {showBuyModal && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Buy Asset</h3>
            <form onSubmit={handleBuy}>
              <div className="mb-4">
                <label htmlFor="buySymbol" className="block text-sm font-medium text-gray-700">Symbol</label>
                <input
                  type="text"
                  id="buySymbol"
                  value={buySymbol}
                  onChange={(e) => setBuySymbol(e.target.value)}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="e.g. AAPL"
                  required
                />
              </div>
              <div className="mb-4">
                <label htmlFor="buyQuantity" className="block text-sm font-medium text-gray-700">Quantity</label>
                <input
                  type="number"
                  id="buyQuantity"
                  value={buyQuantity}
                  onChange={(e) => setBuyQuantity(e.target.value)}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  min="0.01"
                  step="0.01"
                  placeholder="0.00"
                  required
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowBuyModal(false)}
                  className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={transactionLoading}
                  className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-300"
                >
                  {transactionLoading ? 'Processing...' : 'Buy'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Sell Modal */}
      {showSellModal && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Sell Asset</h3>
            <form onSubmit={handleSell}>
              <div className="mb-4">
                <label htmlFor="sellSymbol" className="block text-sm font-medium text-gray-700">Symbol</label>
                <input
                  type="text"
                  id="sellSymbol"
                  value={sellSymbol}
                  onChange={(e) => setSellSymbol(e.target.value)}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="e.g. AAPL"
                  required
                />
              </div>
              <div className="mb-4">
                <label htmlFor="sellQuantity" className="block text-sm font-medium text-gray-700">Quantity</label>
                <input
                  type="number"
                  id="sellQuantity"
                  value={sellQuantity}
                  onChange={(e) => setSellQuantity(e.target.value)}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  min="0.01"
                  step="0.01"
                  placeholder="0.00"
                  required
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowSellModal(false)}
                  className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={transactionLoading}
                  className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-300"
                >
                  {transactionLoading ? 'Processing...' : 'Sell'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Money Modal */}
      {showAddMoneyModal && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Add Money</h3>
            <form onSubmit={handleAddMoney}>
              <div className="mb-4">
                <label htmlFor="addMoneyAmount" className="block text-sm font-medium text-gray-700">Amount</label>
                <div className="mt-1 relative rounded-md shadow-sm">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <span className="text-gray-500 sm:text-sm">$</span>
                  </div>
                  <input
                    type="number"
                    id="addMoneyAmount"
                    value={addMoneyAmount}
                    onChange={(e) => setAddMoneyAmount(e.target.value)}
                    className="block w-full pl-7 pr-12 border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="0.00"
                    min="1"
                    step="1"
                    required
                  />
                </div>
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowAddMoneyModal(false)}
                  className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={transactionLoading}
                  className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:bg-green-300"
                >
                  {transactionLoading ? 'Processing...' : 'Add Money'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
