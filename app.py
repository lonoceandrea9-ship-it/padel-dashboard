import React, { useState } from 'react';
import PlayerListTab from './PlayerListTab';
import PlayerDetailView from './PlayerDetailView';

export default function PlayerArea({ players }) {
  // Gestisce il tab attivo ('overview' o 'directory')
  const [activeTab, setActiveTab] = useState('overview');
  // Memorizza l'ID o l'oggetto del giocatore selezionato per la scheda dettaglio
  const [selectedPlayer, setSelectedPlayer] = useState(null);

  return (
    <div className="player-area-container">
      {/* --- BARRA DEI SUBTAB --- */}
      <div className="flex border-b border-gray-200 mb-4">
        <button
          className={`py-2 px-4 font-medium text-sm border-b-2 ${
            activeTab === 'overview'
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => {
            setActiveTab('overview');
            setSelectedPlayer(null); // Torna alla vista generale se si cambia tab
          }}
        >
          Panoramica
        </button>
        
        <button
          className={`py-2 px-4 font-medium text-sm border-b-2 ${
            activeTab === 'directory' || selectedPlayer
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => {
            setActiveTab('directory');
            setSelectedPlayer(null);
          }}
        >
          Lista Giocatori
        </button>
      </div>

      {/* --- CONTENUTO DEI TAB --- */}
      {activeTab === 'overview' && !selectedPlayer && (
        <div className="p-4">
          <h2 className="text-xl font-bold">Panoramica Area Giocatore</h2>
          <p className="text-gray-600">Contenuti generali dell'area...</p>
        </div>
      )}

      {(activeTab === 'directory' || selectedPlayer) && !selectedPlayer && (
        <PlayerListTab 
          players={players} 
          onSelectPlayer={(player) => setSelectedPlayer(player)} 
        />
      )}

      {/* --- SCHEDA DETTAGLIO SINGOLO GIOCATORE --- */}
      {selectedPlayer && (
        <PlayerDetailView 
          player={selectedPlayer} 
          onBack={() => setSelectedPlayer(null)} 
        />
      )}
    </div>
  );
}
