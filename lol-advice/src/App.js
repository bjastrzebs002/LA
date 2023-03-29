import React, { useState } from 'react';
import { ClipLoader } from 'react-spinners';
import axios from 'axios';
import './App.css';

function App() {
  const [summonerName, setSummonerName] = useState('');
  const [advice, setAdvice] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const getAdvice = async (event) => {
      event.preventDefault();
      setError('');
      setAdvice('');
      setLoading(true);

      try {
        const response = await axios.post('/api/get_advice', { summoner_name: summonerName });

        if (response.data.error) {
          setError(response.data.error);
        } else {
          setAdvice(response.data.advice);
        }
      } catch (err) {
        if (err.response && err.response.data && err.response.data.error) {
          setError(err.response.data.error);
        } else {
          setError('An error occurred while processing your request. Please try again later.');
        }
      } finally {
        setLoading(false);
      }
    };

  return (
      <div className="App" key={loading ? 'loading' : 'idle'}>
        <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
          <div className="relative py-3 sm:max-w-xl sm:mx-auto">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-blue-600 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
            <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
              <div className="max-w-md mx-auto">
                <form onSubmit={getAdvice}>
                  <div>
                    <label htmlFor="summonerName" className="block text-sm font-medium text-gray-700">
                      Summoner Name
                    </label>
                    <input
                      type="text"
                      name="summonerName"
                      id="summonerName"
                      className="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                      value={summonerName}
                      onChange={(event) => setSummonerName(event.target.value)}
                    />
                  </div>
                  <div className="mt-6">
                    <button
                      type="submit"
                      className="w-full py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                      Get Advice
                    </button>
                  </div>
                </form>
                {error && (
                  <div className="text-red-500 text-center whitespace-pre-wrap">{error}</div>
                )}
                {loading && (
                  <div className="flex justify-center items-center mt-4">
                    <ClipLoader color="#4A5568" loading={loading} size={50} />
                  </div>
                )}
                {advice && (
                  <div className="text-center text-gray-800 font-medium mt-4">
                    <p>{advice}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
}

export default App;
