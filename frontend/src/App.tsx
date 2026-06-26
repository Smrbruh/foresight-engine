import React, { useState, useEffect } from 'react';
import { api } from './api/client';
import './index.css';

interface Prediction {
  id: number;
  agent_id: number;
  model_type: string;
  horizon_hours: number;
  status: string;
  result: any;
  created_at: string;
  completed_at: string | null;
}

interface Agent {
  id: number;
  name: string;
  type: string;
  status: string;
  created_at: string;
}

function App() {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [predsRes, agentsRes] = await Promise.all([
        api.get('/predictions'),
        api.get('/agents')
      ]);
      setPredictions(predsRes.data);
      setAgents(agentsRes.data);
      setError(null);
    } catch (err: any) {
      console.error('Fetch error:', err);
      setError(err.message || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const createPrediction = async () => {
    if (agents.length === 0) {
      setError('No agents available. Please create an agent first.');
      return;
    }

    try {
      setIsCreating(true);
      await api.post('/predictions', {
        agent_id: agents[0].id,
        model_type: 'risk_assessment',
        horizon_hours: 24,
        parameters: {
          risk_level: 0.5,
          time_horizon: 30,
          scenario: 'financial_crisis'
        }
      });
      await fetchData();
    } catch (err: any) {
      console.error('Create error:', err);
      setError(err.message || 'Failed to create prediction');
    } finally {
      setIsCreating(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-500';
      case 'pending': return 'bg-yellow-500';
      case 'processing': return 'bg-blue-500';
      case 'failed': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 mb-8 text-white">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-4xl font-bold mb-2">🔮 Foresight Engine</h1>
              <p className="text-white/80">Predictive analytics and monitoring platform</p>
            </div>
            <div className="bg-white/20 px-4 py-2 rounded-full">
              <span className="inline-block w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></span>
              <span className="text-sm">API: Online</span>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Stats & Actions */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white/95 backdrop-blur-sm rounded-xl p-6 shadow-xl">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">📊 Overview</h2>
              <div className="space-y-3">
                <div className="flex justify-between items-center border-b border-gray-100 pb-2">
                  <span className="text-gray-600">Total Predictions</span>
                  <span className="font-bold text-indigo-600">{predictions.length}</span>
                </div>
                <div className="flex justify-between items-center border-b border-gray-100 pb-2">
                  <span className="text-gray-600">Active Agents</span>
                  <span className="font-bold text-indigo-600">{agents.length}</span>
                </div>
                <button
                  onClick={createPrediction}
                  disabled={isCreating || agents.length === 0}
                  className="w-full mt-4 bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-semibold py-3 px-4 rounded-xl hover:from-indigo-600 hover:to-purple-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isCreating ? '⏳ Creating...' : '✨ Create Prediction'}
                </button>
                {agents.length === 0 && (
                  <p className="text-xs text-yellow-600 text-center mt-2">
                    ⚠️ No agents found. Create an agent via API first.
                  </p>
                )}
              </div>
            </div>

            <div className="bg-white/95 backdrop-blur-sm rounded-xl p-6 shadow-xl">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">🔗 Quick Links</h2>
              <div className="space-y-2">
                <a href="/docs" target="_blank" className="block text-indigo-600 hover:text-indigo-800 hover:underline">
                  📚 API Documentation
                </a>
                <a href="/api/health" target="_blank" className="block text-indigo-600 hover:text-indigo-800 hover:underline">
                  💚 Health Check
                </a>
              </div>
            </div>
          </div>

          {/* Right Column - Predictions List */}
          <div className="lg:col-span-2">
            <div className="bg-white/95 backdrop-blur-sm rounded-xl p-6 shadow-xl">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">📈 Recent Predictions</h2>
              
              {loading ? (
                <div className="flex justify-center items-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
                </div>
              ) : error ? (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
                  ❌ {error}
                </div>
              ) : predictions.length === 0 ? (
                <div className="text-center py-12 text-gray-500">
                  <p className="text-4xl mb-4">📭</p>
                  <p>No predictions yet</p>
                  <p className="text-sm mt-2">Click "Create Prediction" to get started</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {predictions.map((pred) => (
                    <div key={pred.id} className="bg-gray-50 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <span className="font-mono text-sm font-bold text-gray-700">
                              #{pred.id}
                            </span>
                            <span className={`px-2 py-1 rounded-full text-xs font-semibold text-white ${getStatusColor(pred.status)}`}>
                              {pred.status.toUpperCase()}
                            </span>
                            <span className="text-xs text-gray-500">
                              {new Date(pred.created_at).toLocaleString()}
                            </span>
                          </div>
                          <div className="grid grid-cols-2 gap-2 text-sm">
                            <div>
                              <span className="text-gray-500">Model:</span>
                              <span className="ml-1 font-medium">{pred.model_type}</span>
                            </div>
                            <div>
                              <span className="text-gray-500">Agent:</span>
                              <span className="ml-1 font-medium">#{pred.agent_id}</span>
                            </div>
                            <div>
                              <span className="text-gray-500">Horizon:</span>
                              <span className="ml-1 font-medium">{pred.horizon_hours}h</span>
                            </div>
                            {pred.result && (
                              <div className="col-span-2 mt-2">
                                <details className="text-xs">
                                  <summary className="cursor-pointer text-indigo-600 hover:text-indigo-800">
                                    View Result
                                  </summary>
                                  <pre className="mt-2 bg-gray-100 p-2 rounded overflow-x-auto">
                                    {JSON.stringify(pred.result, null, 2)}
                                  </pre>
                                </details>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-8 text-center text-white/60 text-sm">
          <p>Foresight Engine v1.0.0 • Built with FastAPI + React</p>
        </footer>
      </div>
    </div>
  );
}

export default App;