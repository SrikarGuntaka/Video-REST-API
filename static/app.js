(function () {
  const $ = (sel) => document.querySelector(sel);
  const outputEl = $('#output');
  const apiBase = window.API_BASE || '';

  function writeOutput(title, data) {
    const text = `${title}:\n${JSON.stringify(data, null, 2)}`;
    outputEl.textContent = text;
  }

  async function apiNoId(method, path) {
    const url = `${apiBase}${path}`;
    const res = await fetch(url, { method });
    if (!res.ok) {
      let errText = await res.text().catch(() => '');
      throw new Error(`${res.status} ${res.statusText}: ${errText}`);
    }
    return res.status === 204 ? null : res.json();
  }

  async function api(method, id, body) {
    const url = `${apiBase}/video/${id}`;
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
    });
    if (!res.ok && res.status !== 204) {
      let errText = await res.text().catch(() => '');
      throw new Error(`${res.status} ${res.statusText}: ${errText}`);
    }
    if (res.status === 204) return null;
    return res.json();
  }

  function getFormValues() {
    const id = Number($('#video-id').value);
    const name = $('#video-name').value.trim();
    const viewsRaw = $('#video-views').value;
    const likesRaw = $('#video-likes').value;
    const views = viewsRaw === '' ? undefined : Number(viewsRaw);
    const likes = likesRaw === '' ? undefined : Number(likesRaw);
    return { id, name, views, likes };
  }

  $('#btn-create').addEventListener('click', async () => {
    try {
      const { id, name, views, likes } = getFormValues();
      const body = { name, views, likes };
      const data = await api('PUT', id, body);
      writeOutput('Created', data);
    } catch (e) { writeOutput('Error', e.message); }
  });

  $('#btn-update').addEventListener('click', async () => {
    try {
      const { id, name, views, likes } = getFormValues();
      const body = {};
      if (name) body.name = name;
      if (views !== undefined) body.views = views;
      if (likes !== undefined) body.likes = likes;
      const data = await api('PATCH', id, body);
      writeOutput('Updated', data);
    } catch (e) { writeOutput('Error', e.message); }
  });

  $('#btn-get').addEventListener('click', async () => {
    try {
      const { id } = getFormValues();
      const data = await api('GET', id);
      writeOutput('Fetched', data);
    } catch (e) { writeOutput('Error', e.message); }
  });

  $('#btn-delete').addEventListener('click', async () => {
    try {
      const { id } = getFormValues();
      await api('DELETE', id);
      writeOutput('Deleted', { id });
    } catch (e) { writeOutput('Error', e.message); }
  });

  const clearBtn = document.querySelector('#btn-clear');
  if (clearBtn) {
    clearBtn.addEventListener('click', async () => {
      try {
        const data = await apiNoId('DELETE', '/videos');
        writeOutput('Cleared DB', data);
      } catch (e) { writeOutput('Error', e.message); }
    });
  }
})();
