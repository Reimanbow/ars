// 媒体詳細のロジック

let currentSourceId = null;

document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const sourceId = params.get('id');

    if (!sourceId) {
        window.location.href = 'sources.html';
        return;
    }

    currentSourceId = sourceId;
    loadSourceDetail(sourceId);
    setupNewItemForm();
});

/**
 * 媒体の詳細を読み込んで表示
 */
async function loadSourceDetail(sourceId) {
    const titleElement = document.getElementById('source-title');
    const categoryElement = document.getElementById('source-category');
    const descriptionElement = document.getElementById('source-description');
    const itemsContainer = document.getElementById('items-container');
    const itemsCountElement = document.getElementById('items-count');

    try {
        const source = await api.getSource(sourceId);

        titleElement.textContent = source.title;

        if (source.category) {
            categoryElement.innerHTML = `
                <span class="px-3 py-1 bg-blue-100 text-blue-700 text-sm rounded">${escapeHtml(source.category)}</span>
            `;
        } else {
            categoryElement.innerHTML = '';
        }

        descriptionElement.textContent = source.description || '(説明なし)';

        const items = source.learning_items || [];
        itemsCountElement.textContent = items.length;

        if (items.length === 0) {
            itemsContainer.innerHTML = `
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
                    <p class="text-blue-700">学習項目がまだありません</p>
                    <p class="text-sm text-blue-600 mt-2">「+ 学習項目を追加」ボタンから追加しましょう！</p>
                </div>
            `;
            return;
        }

        itemsContainer.innerHTML = `
            <div class="space-y-3">
                ${items.map(item => `
                    <div class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                        <div class="flex items-center justify-between">
                            <a href="item-detail.html?id=${item.id}" class="flex-1">
                                <h4 class="font-semibold text-gray-900 hover:text-blue-600">${escapeHtml(item.title)}</h4>
                                ${item.content ? `
                                    <p class="text-sm text-gray-600 mt-1 line-clamp-1">${escapeHtml(item.content)}</p>
                                ` : ''}
                                <p class="text-xs text-gray-500 mt-1">作成日: ${formatDate(item.created_at)}</p>
                            </a>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

    } catch (error) {
        console.error('Failed to load source detail:', error);
        titleElement.textContent = 'エラー';
        descriptionElement.textContent = error.message;
        itemsContainer.innerHTML = '';
    }
}

/**
 * 新規学習項目フォームのセットアップ
 */
function setupNewItemForm() {
    const form = document.getElementById('new-item-form');
    const modal = document.getElementById('new-item-modal');
    const openBtn = document.getElementById('add-item-btn');
    const closeBtn = document.getElementById('close-modal-btn');

    openBtn.addEventListener('click', () => {
        document.getElementById('source_id').value = currentSourceId;
        modal.classList.remove('hidden');
    });

    closeBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
        form.reset();
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const sourceId = parseInt(document.getElementById('source_id').value);
        const title = document.getElementById('title').value;
        const content = document.getElementById('content').value;
        const startDate = document.getElementById('start_date').value;

        try {
            const data = { source_id: sourceId, title };
            if (content) data.content = content;
            if (startDate) data.start_date = startDate;

            await api.createLearningItem(data);
            showNotification('学習項目を作成しました！', 'success');
            form.reset();
            modal.classList.add('hidden');
            loadSourceDetail(currentSourceId);
        } catch (error) {
            console.error('Failed to create item:', error);
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
 * 日付をフォーマット
 */
function formatDate(dateTimeStr) {
    const date = new Date(dateTimeStr);
    return date.toLocaleDateString('ja-JP', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * HTMLエスケープ
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
