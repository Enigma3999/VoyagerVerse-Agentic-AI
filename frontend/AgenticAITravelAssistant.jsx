import React, { useState, useEffect } from 'react';
import axios from 'axios';

const mockWeather = {
  temperature: 44,
  condition: 'Sunny',
  heatIndex: 'Very High',
  forecast: 'Extreme heat expected throughout the day'
};

const mockVenues = [
  { name: 'Dubai Museum', type: 'Cultural', indoorActivity: true, price: 35, rating: 4.5, crowdLevel: 'Medium' },
  { name: 'Dubai Mall', type: 'Shopping', indoorActivity: true, price: 0, rating: 4.7, crowdLevel: 'High' },
  { name: 'Burj Khalifa Observation Deck', type: 'Attraction', indoorActivity: true, price: 149, rating: 4.6, crowdLevel: 'Medium' },
  { name: 'IMG World of Adventures', type: 'Entertainment', indoorActivity: true, price: 249, rating: 4.4, crowdLevel: 'Medium' }
];

const mockReasoning = {
  unsafeActivity: 'Desert Safari',
  reason: 'Outdoor temperature exceeds safety threshold (44°C)',
  alternatives: mockVenues
};

const mockAction = {
  updatedItinerary: [
    { time: '09:00 AM', activity: 'Hotel Breakfast', type: 'Food', location: 'Hotel Restaurant', indoor: true },
    { time: '11:00 AM', activity: 'Dubai Museum Visit', type: 'Cultural', location: 'Al Fahidi Fort', indoor: true, updated: true },
    { time: '02:00 PM', activity: 'Lunch at Arabian Tea House', type: 'Food', location: 'Al Fahidi District', indoor: true, updated: true },
    { time: '04:00 PM', activity: 'Dubai Mall & Fountain Show', type: 'Shopping & Entertainment', location: 'Downtown Dubai', indoor: true, updated: true },
    { time: '07:00 PM', activity: 'Dinner Cruise', type: 'Food & Entertainment', location: 'Dubai Marina', indoor: true }
  ],
  message: 'Itinerary updated due to extreme heat.'
};

const mockLearning = {
  updates: [
    'Added "Indoor activities preferred during heat warnings"',
    'Updated cultural venue preference ranking',
    'Reinforced budget compliance pattern'
  ],
  impact: {
    weatherAdaptability: 85,
    culturalPreferenceAccuracy: 92,
    satisfactionPrediction: 90
  }
};

const AgenticAITravelAssistant = () => {
  const [stage, setStage] = useState(0);
  const [userInput, setUserInput] = useState({ name: '', preferences: '' });
  const [weather, setWeather] = useState(null);
  const [venues, setVenues] = useState([]);
  const [reasoning, setReasoning] = useState(null);
  const [action, setAction] = useState(null);
  const [learning, setLearning] = useState(null);
  const [loading, setLoading] = useState(false);

  // Step 1: Perception (Weather + Venue APIs)
  useEffect(() => {
    if (stage === 1) {
      setLoading(true);
      Promise.all([
        axios.get('/api/tools/weather', { params: { location: 'Dubai' } }).catch(() => ({ data: mockWeather })),
        axios.get('/api/tools/venues', { params: { location: 'Dubai', preferences: userInput.preferences } }).catch(() => ({ data: mockVenues }))
      ])
      .then(([weatherRes, venuesRes]) => {
        setWeather(weatherRes.data);
        setVenues(venuesRes.data);
        setLoading(false);
        setStage(2);
      });
    }
  }, [stage, userInput]);

  // Step 2: Reasoning (Agentic Core)
  useEffect(() => {
    if (stage === 2 && weather && venues.length > 0) {
      setLoading(true);
      axios.post('/api/agent/reason', { weather, venues, user: userInput })
        .then(res => {
          setReasoning(res.data);
          setLoading(false);
          setStage(3);
        })
        .catch(() => {
          setReasoning(mockReasoning);
          setLoading(false);
          setStage(3);
        });
    }
  }, [stage, weather, venues, userInput]);

  // Step 3: Action (Booking/Itinerary Update)
  useEffect(() => {
    if (stage === 3 && reasoning) {
      setLoading(true);
      axios.post('/api/agent/action', { reasoning, user: userInput })
        .then(res => {
          setAction(res.data);
          setLoading(false);
          setStage(4);
        })
        .catch(() => {
          setAction(mockAction);
          setLoading(false);
          setStage(4);
        });
    }
  }, [stage, reasoning, userInput]);

  // Step 4: Learning (Preference Update)
  useEffect(() => {
    if (stage === 4 && action) {
      setLoading(true);
      axios.post('/api/agent/learn', { action, user: userInput })
        .then(res => {
          setLearning(res.data);
          setLoading(false);
        })
        .catch(() => {
          setLearning(mockLearning);
          setLoading(false);
        });
    }
  }, [stage, action, userInput]);

  const handleStart = () => setStage(1);

  return (
    <div className="max-w-4xl mx-auto p-4">
      {stage === 0 && (
        <form onSubmit={e => { e.preventDefault(); handleStart(); }} className="bg-white rounded-lg shadow p-6 flex flex-col gap-4">
          <h2 className="text-lg font-semibold mb-2">Start Your Agentic AI Travel Demo</h2>
          <input className="border p-2 rounded" placeholder="Your Name" value={userInput.name} onChange={e => setUserInput({ ...userInput, name: e.target.value })} required />
          <input className="border p-2 rounded" placeholder="Preferences (e.g. indoor, cultural)" value={userInput.preferences} onChange={e => setUserInput({ ...userInput, preferences: e.target.value })} required />
          <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Start Demo</button>
        </form>
      )}

      {stage >= 1 && (
        <div className="my-4">
          <h2 className="font-semibold text-blue-700 mb-2">Perception</h2>
          {loading ? <div>Loading weather and venues...</div> : (
            <>
              <div className="mb-2">Weather: {weather && `${weather.temperature}°C, ${weather.condition}`}</div>
              <div>Venues: {venues.map(v => v.name).join(', ')}</div>
            </>
          )}
        </div>
      )}

      {stage >= 2 && (
        <div className="my-4">
          <h2 className="font-semibold text-blue-700 mb-2">Reasoning</h2>
          {loading ? <div>Reasoning...</div> : (
            <pre className="bg-slate-100 p-2 rounded text-xs overflow-x-auto">{JSON.stringify(reasoning, null, 2)}</pre>
          )}
        </div>
      )}

      {stage >= 3 && (
        <div className="my-4">
          <h2 className="font-semibold text-blue-700 mb-2">Action</h2>
          {loading ? <div>Taking action...</div> : (
            <pre className="bg-slate-100 p-2 rounded text-xs overflow-x-auto">{JSON.stringify(action, null, 2)}</pre>
          )}
        </div>
      )}

      {stage >= 4 && (
        <div className="my-4">
          <h2 className="font-semibold text-blue-700 mb-2">Learning</h2>
          {loading ? <div>Learning from preferences...</div> : (
            <pre className="bg-slate-100 p-2 rounded text-xs overflow-x-auto">{JSON.stringify(learning, null, 2)}</pre>
          )}
        </div>
      )}
    </div>
  );
};

export default AgenticAITravelAssistant;
