const $ = (id) => document.getElementById(id);
const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
async function api(url, options={}) { const response = await fetch(url, options); const body = await response.json().catch(() => ({})); if (!response.ok) throw new Error(body.detail || `HTTP ${response.status}`); return body; }
async function loadHealth() {
  try { const h = await api('/api/health'); $('api-status').textContent = 'API online · local'; $('tshark-status').textContent = h.tshark_available ? 'Available' : 'Not installed'; $('repo-status').textContent = h.saylo_repo_configured ? 'Configured' : 'Not configured'; $('repo-detail').textContent = h.saylo_repo_configured ? 'Source checkout path found' : 'Set SAYLO_REPO_PATH to inspect source'; }
  catch (e) { $('api-status').textContent = 'API unavailable'; $('repo-detail').textContent = e.message; }
}
async function loadAgents() {
  try { const data = await api('/api/agents'); $('agent-count').textContent = data.count; $('agent-list').innerHTML = data.agents.map(a => `<div class="agent-card"><strong>${escapeHtml(a.name)}</strong><p>${escapeHtml(a.focus)}</p></div>`).join(''); }
  catch (e) { $('agent-list').textContent = e.message; }
}
async function loadInventory() {
  $('cartography-summary').textContent = 'Scanning configured source checkout…';
  try { const [i,c] = await Promise.all([api('/api/project/inventory'), api('/api/project/cartography')]); $('cartography-summary').textContent = i.exists ? `${i.scanned_file_count} files scanned · ${i.indicators.length} heuristic indicators${i.truncated ? ' · scan limit reached' : ''}` : 'No local source checkout available. No code-specific architecture is assumed.'; $('mermaid-map').textContent = c.mermaid; const sample = (i.files || []).slice(0,10); $('inventory-files').innerHTML = sample.length ? sample.map(f => `<div class="file-row"><code>${escapeHtml(f.path)}</code><span>${f.size_bytes} B</span></div>`).join('') : '<p class="muted">No files to display yet.</p>'; }
  catch (e) { $('cartography-summary').textContent = `Inventory failed: ${e.message}`; }
}
$('refresh-inventory').addEventListener('click', loadInventory);
$('investigation-form').addEventListener('submit', async (event) => {
  event.preventDefault(); const status = $('form-status'), target = $('investigation-result'); status.textContent = 'Creating plan…'; target.classList.add('hidden');
  try { const record = await api('/api/investigations', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({title:$('task-title').value, kind:$('task-kind').value, description:$('task-description').value})}); status.textContent = `Plan created · ${record.id.slice(0,8)}`; target.innerHTML = `<div class="task-title">${escapeHtml(record.title)}</div><p class="muted">Status: ${escapeHtml(record.status)} · ${escapeHtml(record.execution_mode)}</p><p style="margin:12px 0 6px;font-size:11px;font-weight:700">Suggested specialists</p>${record.selected_agents.map(a=>`<span class="task-agent">${escapeHtml(a)}</span>`).join('')}<div style="margin-top:14px">${record.tasks.map(t=>`<div class="task-step"><strong>${t.step}. ${escapeHtml(t.name)}</strong><small>Owner: ${escapeHtml(t.owner)} · ${t.checks.map(escapeHtml).join(' · ')}</small></div>`).join('')}</div><p class="muted">${record.limitations.map(escapeHtml).join(' ')}</p>`; target.classList.remove('hidden'); }
  catch (e) { status.textContent = e.message; }
});
$('parse-sip').addEventListener('click', async () => { $('sip-result').textContent = 'Parsing…'; try { const result = await api('/api/voip/sip/parse', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:$('sip-message').value})}); $('sip-result').textContent = JSON.stringify(result, null, 2); } catch(e) { $('sip-result').textContent = e.message; } });
$('analyze-pcap').addEventListener('click', async () => { const file = $('pcap-file').files[0]; if (!file) { $('pcap-result').textContent = 'Choose a PCAP/PCAPNG file first.'; $('pcap-result').classList.remove('hidden'); return; } $('pcap-result').textContent = 'Analyzing locally…'; $('pcap-result').classList.remove('hidden'); try { const result = await api('/api/voip/pcap/analyze', {method:'POST', headers:{'Content-Type':'application/octet-stream','X-Filename':file.name}, body:file}); $('pcap-result').textContent = JSON.stringify(result, null, 2); } catch(e) { $('pcap-result').textContent = e.message; } });
loadHealth(); loadAgents(); loadInventory();
