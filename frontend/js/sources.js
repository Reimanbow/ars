// 媒体一覧のロジック

document.addEventListener('DOMContentLoaded', () => {
    loadSources();
    setupNewSourceForm();
});

/**
 * 媒体一覧を読み込んで表示
 */
async function loadSources() {
    const container = document.getElementById('sources-container');
    const countElement = document.getElementById('sources-count');

    try {
        const data = await api.getSources();
        const sources = data.items;

        countElement.textContent = data.total;

        if (sources.length === 0) {
            container.innerHTML = `
                <div class="col-span-full bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
                    <p class="text-blue-700">媒体がありません</p>
                    <p class="text-sm text-blue-600 mt-2">新しく追加しましょう！</p>
                </div>
            `;
            return;
        }

        container.innerHTML = sources.map(source => `
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div class="flex items-start justify-between mb-2">
                    <h3 class="text-lg font-semibold text-gray-900">${escapeHtml(source.title)}</h3>
                    ${source.category ? `
                        <span class="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded">${escapeHtml(source.category)}</span>
                    ` : ''}
                </div>
                ${source.description ? `
                    <p class="text-sm text-gray-600 mb-3 line-clamp-2">${escapeHtml(source.description)}</p>
                ` : ''}
                <div class="flex items-center justify-between mt-4">
                    <a href="source-detail.html?id=${source.id}" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
                        詳細を見る →
                    </a>
                    <button
                        onclick="deleteSource(${source.id}, '${escapeHtml(source.title)}')"
                        class="px-3 py-1 bg-red-500 hover:bg-red-600 text-white text-xs rounded transition-colors"
                    >
                        削除
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load sources:', error);
        container.innerHTML = `
            <div class="col-span-full bg-red-50 border border-red-200 rounded-lg p-4 text-center text-red-700">
                エラー: ${error.message}
            </div>
        `;
    }
}

/**
 * 媒体を削除
 */
async function deleteSource(sourceId, title) {
    if (!confirm(`「${title}」を削除しますか？\n関連する学習項目と復習タスクもすべて削除されます。`)) {
        return;
    }

    try {
        await api.deleteSource(sourceId);
        showNotification('媒体を削除しました', 'success');
        loadSources();
    } catch (error) {
        console.error('Failed to delete source:', error);
        showNotification('エラー: ' + error.message, 'error');
    }
}

/**
 * 新規媒体フォームのセットアップ
 */
function setupNewSourceForm() {
    const form = document.getElementById('new-source-form');
    const modal = document.getElementById('new-source-modal');
    const openBtn = document.getElementById('open-modal-btn');
    const closeBtn = document.getElementById('close-modal-btn');

    openBtn.addEventListener('click', () => {
        modal.classList.remove('hidden');
    });

    closeBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
        form.reset();
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const title = document.getElementById('title').value;
        const category = document.getElementById('category').value || null;
        const description = document.getElementById('description').value || null;

        try {
            const data = { title };
            if (category) data.category = category;
            if (description) data.description = description;

            await api.createSource(data);
            showNotification('媒体を作成しました！', 'success');
            form.reset();
            modal.classList.add('hidden');
            loadSources();
        } catch (error) {
            console.error('Failed to create source:', error);
            showNotification('エラー: ' + error.message, 'error');
        }
    });
}

/**
 * 通知を表示
 */
function showNotification(message, type = 'success') {
    const container = document.getElementById('notification-container');
    const bgColor = type === 'success' ? 'bg-green-500' : 'bg-red-500';

    const notification = document.createElement('div');
    notification.className = `${bgColor} text-white px-6 py-3 rounded-lg shadow-lg`;
    notification.textContent = message;

    container.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

/**
 * HTMLエスケープ
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
