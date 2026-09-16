<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Stile Playtomic</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#f0fdf4',
                            500: '#10b981', // Verde sportivo principale (stile Playtomic)
                            600: '#059669',
                            700: '#047857',
                        }
                    }
                }
            }
        }
    </script>
    <!-- Google Fonts: Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-gray-50 text-gray-900 antialiased min-h-screen flex">

    <!-- SIDEBAR DI NAVIGAZIONE -->
    <aside class="w-64 bg-white border-r border-gray-100 hidden md:flex flex-col justify-between p-6">
        <div>
            <!-- Logo -->
            <div class="flex items-center gap-3 mb-10">
                <div class="w-10 h-10 rounded-2xl bg-brand-500 flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-brand-500/30">
                    P
                </div>
                <span class="text-xl font-bold tracking-tight">SportApp</span>
            </div>

            <!-- Menu Links -->
            <nav class="space-y-1">
                <a href="#" class="flex items-center gap-3 px-4 py-3 text-sm font-semibold text-brand-600 bg-brand-50 rounded-2xl transition-all">
                    📊 Dashboard
                </a>
                <a href="#" class="flex items-center gap-3 px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-2xl transition-all">
                    📅 Prenotazioni
                </a>
                <a href="#" class="flex items-center gap-3 px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-2xl transition-all">
                    👥 Community & Match
                </a>
                <a href="#" class="flex items-center gap-3 px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-2xl transition-all">
                    📈 Analytics & Storico
                </a>
            </nav>
        </div>

        <!-- Profilo utente in basso -->
        <div class="pt-4 border-t border-gray-100 flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-gray-200 overflow-hidden">
                <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100" alt="Avatar" class="w-full h-full object-cover">
            </div>
            <div>
                <h4 class="text-sm font-semibold">Andrea</h4>
                <p class="text-xs text-gray-500">Pro Member</p>
            </div>
        </div>
    </aside>

    <!-- CONTENUTO PRINCIPALE -->
    <main class="flex-1 flex flex-col min-w-0 overflow-y-auto">
        
        <!-- Header superiore -->
        <header class="bg-white border-b border-gray-100 px-8 py-4 flex items-center justify-between sticky top-0 z-10">
            <div>
                <h1 class="text-xl font-bold tracking-tight">Bentornato, Andrea! 👋</h1>
                <p class="text-xs text-gray-500">Ecco una panoramica delle attività e delle metriche di oggi.</p>
            </div>
            <div class="flex items-center gap-4">
                <button class="px-4 py-2 bg-brand-500 hover:bg-brand-600 text-white text-sm font-semibold rounded-2xl shadow-md shadow-brand-500/20 transition-all">
                    + Nuova Prenotazione
                </button>
            </div>
        </header>

        <!-- Area dei contenuti -->
        <div class="p-8 max-w-7xl w-full mx-auto space-y-8">

            <!-- SEZIONE KPI CARDS (Stile Playtomic / Dashboard moderna) -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <!-- Card 1 -->
                <div class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm hover:shadow-md transition-all">
                    <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Match Totali</p>
                    <div class="flex items-baseline justify-between mt-2">
                        <h3 class="text-3xl font-bold">128</h3>
                        <span class="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-full">+12%</span>
                    </div>
                </div>
                <!-- Card 2 -->
                <div class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm hover:shadow-md transition-all">
                    <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Ore di Gioco</p>
                    <div class="flex items-baseline justify-between mt-2">
                        <h3 class="text-3xl font-bold">96.5</h3>
                        <span class="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-full">+8%</span>
                    </div>
                </div>
                <!-- Card 3 -->
                <div class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm hover:shadow-md transition-all">
                    <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Tasso Vittorie</p>
                    <div class="flex items-baseline justify-between mt-2">
                        <h3 class="text-3xl font-bold">64%</h3>
                        <span class="text-xs font-semibold text-rose-600 bg-rose-50 px-2.5 py-1 rounded-full">-2%</span>
                    </div>
                </div>
                <!-- Card 4 -->
                <div class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm hover:shadow-md transition-all">
                    <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Credito Disponibile</p>
                    <div class="flex items-baseline justify-between mt-2">
                        <h3 class="text-3xl font-bold">€ 45.00</h3>
                        <span class="text-xs font-semibold text-brand-600 bg-brand-50 px-2.5 py-1 rounded-full">Attivo</span>
                    </div>
                </div>
            </div>

            <!-- SEZIONE CENTRALE: Tabella Attività / Match Recenti -->
            <div class="bg-white rounded-3xl border border-gray-100 shadow-sm p-6">
                <div class="flex items-center justify-between mb-6">
                    <h3 class="text-lg font-bold">Prossimi Match & Prenotazioni</h3>
                    <a href="#" class="text-sm font-semibold text-brand-600 hover:underline">Vedi tutti</a>
                </div>
                
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-gray-100 text-xs font-semibold text-gray-400 uppercase">
                                <th class="pb-4">Campo / Attività</th>
                                <th class="pb-4">Data & Ora</th>
                                <th class="pb-4">Partecipanti</th>
                                <th class="pb-4">Stato</th>
                                <th class="pb-4 text-right">Azione</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-50 text-sm">
                            <tr class="hover:bg-gray-50/50 transition-all">
                                <td class="py-4 font-semibold">Campo Padel 01 (Indoor)</td>
                                <td class="py-4 text-gray-500">Oggi, 18:00 - 19:30</td>
                                <td class="py-4 text-gray-500">4 / 4 giocatori</td>
                                <td class="py-4">
                                    <span class="px-3 py-1 bg-emerald-50 text-emerald-600 rounded-full text-xs font-semibold">Confermato</span>
                                </td>
                                <td class="py-4 text-right">
                                    <button class="text-gray-400 hover:text-gray-900 font-medium">Dettagli</button>
                                </td>
                            </tr>
                            <tr class="hover:bg-gray-50/50 transition-all">
                                <td class="py-4 font-semibold">Campo Padel 03 (Panoramic)</td>
                                <td class="py-4 text-gray-500">Dom, 10:00 - 11:30</td>
                                <td class="py-4 text-gray-500">2 / 4 giocatori</td>
                                <td class="py-4">
                                    <span class="px-3 py-1 bg-amber-50 text-amber-600 rounded-full text-xs font-semibold">In attesa</span>
                                </td>
                                <td class="py-4 text-right">
                                    <button class="text-gray-400 hover:text-gray-900 font-medium">Invita</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

        </div>
    </main>

</body>
</html>
