const API_URL = "http://localhost:8000/api";
let apiToken = localStorage.getItem('django_auth_token');
let mySongs = []; // cache array

window.onload = () => { if (apiToken) showApp(); };

window.handleGoogleLogin = function(response) {
    fetch(`${API_URL}/auth/google/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ access_token: response.credential, id_token: response.credential })
    })
    .then(res => res.json())
    .then(data => {
        if (data.key) {
            apiToken = data.key;
            localStorage.setItem('django_auth_token', apiToken);
            showApp();
        } else alert("Login failed! " + JSON.stringify(data));
    }).catch(err => alert("Could not connect to backend."));
};

window.showApp = function() {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('app-section').classList.remove('hidden');
    document.getElementById('user-controls').classList.remove('hidden');
    document.getElementById('nav-playlists').classList.remove('hidden');
    fetchSongs().then(() => fetchPlaylists());
};

window.logout = function() {
    apiToken = null;
    mySongs = [];
    localStorage.removeItem('django_auth_token');

    // Hide everything
    document.getElementById('app-section').classList.add('hidden');
    document.getElementById('user-controls').classList.add('hidden');
    document.getElementById('nav-playlists').classList.add('hidden');
    document.getElementById('playlists-section').classList.add('hidden');

    // Show login
    document.getElementById('auth-section').classList.remove('hidden');

    // Clear content
    document.getElementById('songs-list').innerHTML = "<p style='color: var(--text-secondary)'>Loading songs...</p>";
    document.getElementById('playlists-list').innerHTML = "<p style='color: var(--text-secondary)'>Loading playlists...</p>";
    document.getElementById('generate-status').innerHTML = "";
    document.getElementById('story-input').value = "";
    document.getElementById('mood-input').value = "";
    document.getElementById('occasion-input').value = "";
    document.getElementById('lyrics-input').value = "";
    document.getElementById('language-input').value = "English";
};

async function fetchAPI(path, options={}) {
    const headers = { "Authorization": `Token ${apiToken}` };
    if (!(options.body instanceof FormData)) headers["Content-Type"] = "application/json";
    
    const res = await fetch(`${API_URL}${path}`, { ...options, headers: {...options.headers, ...headers} });
    if (res.status === 401) { logout(); throw new Error("Unauthorized"); }
    if (res.status === 204) return null;
    if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Backend error");
    }
    return await res.json();
}

window.generateSong = async function() {
    const story    = document.getElementById('story-input').value.trim();
    const genre    = document.getElementById('genre-input').value;
    const mood     = document.getElementById('mood-input').value.trim();
    const occasion = document.getElementById('occasion-input').value.trim();
    const language = document.getElementById('language-input').value.trim() || "English";
    const lyrics   = document.getElementById('lyrics-input').value.trim();
    const statusEl = document.getElementById('generate-status');
    
    if (!story) return alert("Please enter a story/prompt!");

    const payload = { story, genre, title: story.substring(0, 20) + "...", language };
    if (mood)     payload.mood     = mood;
    if (occasion) payload.occasion = occasion;
    if (lyrics)   payload.lyrics   = lyrics;

    statusEl.innerHTML = "✨ Generating... please wait.";
    try {
        await fetchAPI('/songs/', { method: 'POST', body: JSON.stringify(payload) });
        statusEl.innerHTML = "✅ Song generation started!";
        document.getElementById('story-input').value   = "";
        document.getElementById('mood-input').value    = "";
        document.getElementById('occasion-input').value = "";
        document.getElementById('lyrics-input').value  = "";
        document.getElementById('language-input').value = "English";
        fetchSongs();
    } catch(e) { statusEl.innerText = "Error: " + e.message; }
};

window.fetchSongs = async function() {
    try {
        let data = await fetchAPI('/songs/');
        if (data.results) data = data.results;
        
        mySongs = data;
        const list = document.getElementById('songs-list');
        list.innerHTML = data.length ? "" : "<p style='color: var(--text-secondary)'>No songs found.</p>";

        data.forEach(song => {
            const statusClass = song.status.toLowerCase();
            const shareLink = `http://localhost:3000/public.html?id=${song.id}`;
            
            list.innerHTML += `
                <div class="item">
                    <h4>${song.title || "Generating..."}</h4>
                    <p style="margin: 2px 0; font-size:14px; color: var(--text-secondary);"><strong>Genre:</strong> ${song.genre}</p>
                    
                    <div class="badges-row">
                        <span class="status-badge status-${statusClass}">${song.status}</span>
                        <span class="visibility-badge">Visibility: <strong style="color: #fff;">${song.visibility.toUpperCase()}</strong></span>
                    </div>
                    
                    <div class="controls">
                        <button class="secondary" onclick="toggleVisibility(${song.id}, '${song.visibility}')">
                            Make ${song.visibility === 'public' ? 'Private' : 'Public'}
                        </button>
                    </div>

                    ${song.visibility === 'public' && song.status === 'complete' ? 
                        `<div class="share-box">Share Link: <a href="${shareLink}" target="_blank">${shareLink}</a></div>` 
                        : `<div class="share-box" style="color: var(--text-secondary);">Private. Change to public to get a shareable link.</div>`
                    }

                    ${song.audio_url ? `<div class="audio-player"><audio controls src="${song.audio_url}"></audio></div>` : ''}
                </div>
            `;
        });
    } catch(e) { console.error(e); }
};

window.toggleVisibility = async function(id, currentVisibility) {
    const newVis = currentVisibility === 'public' ? 'private' : 'public';
    try {
        await fetchAPI(`/songs/${id}/`, { method: 'PATCH', body: JSON.stringify({ visibility: newVis }) });
        fetchSongs();
    } catch(e) { alert(e.message); }
};

window.createPlaylist = async function() {
    const name = document.getElementById('new-playlist-name').value;
    if(!name) return;
    try {
        await fetchAPI('/playlists/', { method: 'POST', body: JSON.stringify({ name }) });
        document.getElementById('new-playlist-name').value = '';
        fetchPlaylists();
    } catch(e) { alert(e.message); }
};

window.fetchPlaylists = async function() {
    try {
        let data = await fetchAPI('/playlists/');
        if (data.results) data = data.results;

        const list = document.getElementById('playlists-list');
        list.innerHTML = data.length ? "" : "<p style='color: var(--text-secondary)'>No playlists found.</p>";

        data.forEach(pl => {
            let songOptions = mySongs.filter(s => s.status === 'complete').map(s => `<option value="${s.id}">${s.title || s.id}</option>`).join('');
            
            list.innerHTML += `
                <div class="item">
                    <div class="flex-row">
                        <div>
                            <h4>${pl.name}</h4>
                            <p style="font-size:13px; color: var(--text-secondary);">Total Songs: ${pl.song_count}</p>
                        </div>
                        ${pl.cover_image ? `<img src="${pl.cover_image}" class="cover">` : ''}
                    </div>
                    
                    <div class="playlist-songs">
                        <strong style="color:#fff;">Songs in Playlist</strong>
                        <div style="margin-top: 10px;">
                        ${pl.songs.length === 0 ? '<i style="color: var(--text-secondary);">Empty</i>' : 
                            pl.songs.map(s => `
                                <div class="playlist-song-row">
                                    <span>${s.title || s.id}</span>
                                    <button class="danger" style="padding: 4px 10px; font-size: 11px;" onclick="removeSong(${pl.id}, ${s.id})">Remove</button>
                                </div>
                            `).join('')
                        }
                        </div>
                    </div>

                    <div class="controls flex-row" style="gap: 15px;">
                        <select id="add-song-pl-${pl.id}" style="margin:0;">
                            <option value="">-- Select Song to Add --</option>
                            ${songOptions}
                        </select>
                        <button class="success" onclick="addSong(${pl.id})">Add Song</button>
                    </div>

                    <div class="controls" style="margin-top: 20px; border-top: 1px solid var(--border); padding-top: 15px;">
                        <input type="file" id="cover-pl-${pl.id}" accept="image/*" style="padding: 8px;">
                        <button class="secondary" onclick="uploadPlaylistCover(${pl.id})">Upload Cover</button>
                    </div>
                </div>
            `;
        });
    } catch(e) { console.error(e); }
};

window.addSong = async function(playlistId) {
    const songId = document.getElementById(`add-song-pl-${playlistId}`).value;
    if(!songId) return alert("Select a song first!");
    try {
        await fetchAPI(`/playlists/${playlistId}/songs/add/`, { method: 'POST', body: JSON.stringify({ song_id: parseInt(songId) }) });
        fetchPlaylists();
    } catch(e) { alert(e.message); }
};

window.removeSong = async function(playlistId, songId) {
    try {
        await fetchAPI(`/playlists/${playlistId}/songs/remove/`, { method: 'POST', body: JSON.stringify({ song_id: parseInt(songId) }) });
        fetchPlaylists();
    } catch(e) { alert(e.message); }
};

window.uploadPlaylistCover = async function(playlistId) {
    const fileInput = document.getElementById(`cover-pl-${playlistId}`);
    if(!fileInput.files.length) return alert("Please select an image file first!");
    
    const formData = new FormData();
    formData.append("cover_image", fileInput.files[0]);

    try {
        const res = await fetch(`${API_URL}/playlists/${playlistId}/`, {
            method: 'PATCH',
            headers: { "Authorization": `Token ${apiToken}` },
            body: formData
        });
        
        if(!res.ok) throw new Error(await res.text());
        fetchPlaylists();
    } catch(e) { alert(e.message); }
};