// 学習項目一覧のロジック

document.addEventListener('DOMContentLoaded', () => {
    loadItems();
});

/**
 * 学習項目一覧を読み込んで表示
 */
async function loadItems() {
    const container = document.getElementById('items-container');
    const countElement = document.getElementById('items-count');

    try {
        const data = await api.getLearningItems();
        const items = data.items;

        countElement.textContent = data.total;

        if (items.length === 0) {
            container.innerHTML = `
                <tr>
                    <td colspan="4" class="px-6 py-8 text-center text-gray-500">
                        学習項目がありません。
                        <a href="index.html" class="text-blue-500 hover:underline ml-2">新しく追加する</a>
                    </td>
                </tr>
            `;
            return;
        }

        container.innerHTML = items.map(item => `
            <tr class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4 border-b border-gray-200">
                    <span class="text-gray-700 font-medium">${item.id}</span>
                </td>
                <td class="px-6 py-4 border-b border-gray-200">
                    <a href="item-detail.html?id=${item.id}" class="text-blue-600 hover:text-blue-800 font-semibold">
                        ${escapeHtml(item.title)}
                    </a>
                    ${item.content ? `
                        <p class="text-sm text-gray-600 mt-1 line-clamp-2">${escapeHtml(item.content)}</p>
                    ` : ''}
                </td>
                <td class="px-6 py-4 border-b border-gray-200">
                    <span class="text-sm text-gray-600">${formatDateTime(item.created_at)}</span>
                </td>
                <td class="px-6 py-4 border-b border-gray-200 text-right">
                    <button
                        onclick="deleteItem(${item.id}, '${escapeHtml(item.title)}')"
                        class="px-3 py-1 bg-red-500 hover:bg-red-600 text-white text-sm rounded transition-colors"
                    >
                        削除
                    </button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load items:', error);
        container.innerHTML = `
            <tr>
                <td colspan="4" class="px-6 py-4 text-center text-red-600">
                    エラー: ${error.message}
                </td>
            </tr>
        `;
    }
}

/**
 * 学習項目を削除
 */
async function deleteItem(itemId, title) {
    if (!confirm(`「${title}」を削除しますか？\n関連する復習タスクもすべて削除されます。`)) {
        return;
    }

    try {
        await api.deleteLearningItem(itemId);
        showNotification('学習項目を削除しました', 'success');
        loadItems();
    } catch (error) {
        console.error('Failed to delete item:', error);
        showNotification('エラー: ' + error.message, 'error');
    }
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
 * 日時をフォーマット
 */
function formatDateTime(dateTimeStr) {
    const date = new Date(dateTimeStr);
    return date.toLocaleString('ja-JP', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
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
