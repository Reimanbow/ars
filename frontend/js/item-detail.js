// 学習項目詳細のロジック

document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const itemId = params.get('id');

    if (!itemId) {
        window.location.href = 'items.html';
        return;
    }

    loadItemDetail(itemId);
});

/**
 * 学習項目の詳細を読み込んで表示
 */
async function loadItemDetail(itemId) {
    const titleElement = document.getElementById('item-title');
    const contentElement = document.getElementById('item-content');
    const progressContainer = document.getElementById('progress-container');

    try {
        const item = await api.getLearningItem(itemId);

        titleElement.textContent = item.title;
        contentElement.textContent = item.content || '(内容なし)';

        // 復習タスクをステージオフセット順にソート
        const tasks = [...item.review_tasks].sort((a, b) => a.stage_offset_days - b.stage_offset_days);

        progressContainer.innerHTML = tasks.map((task, index) => {
            const isCompleted = task.status === 'Completed';
            const isReady = task.status === 'Ready';
            const isPending = task.status === 'Pending';

            return `
                <div class="flex items-start mb-6 last:mb-0">
                    <!-- ステップインジケーター -->
                    <div class="flex flex-col items-center mr-4">
                        <div class="w-10 h-10 rounded-full flex items-center justify-center ${
                            isCompleted ? 'bg-green-500 text-white' :
                            isReady ? 'bg-blue-500 text-white' :
                            'bg-gray-300 text-gray-600'
                        }">
                            ${isCompleted ? '✓' : index + 1}
                        </div>
                        ${index < tasks.length - 1 ? `
                            <div class="w-0.5 h-12 ${isCompleted ? 'bg-green-500' : 'bg-gray-300'}"></div>
                        ` : ''}
                    </div>

                    <!-- タスク情報 -->
                    <div class="flex-1 bg-white border rounded-lg p-4 ${
                        isReady ? 'border-blue-400 shadow-md' : 'border-gray-200'
                    }">
                        <div class="flex items-center justify-between mb-2">
                            <h3 class="text-lg font-semibold text-gray-900">${task.stage_name}</h3>
                            <span class="px-3 py-1 rounded-full text-sm ${
                                isCompleted ? 'bg-green-100 text-green-700' :
                                isReady ? 'bg-blue-100 text-blue-700' :
                                'bg-gray-100 text-gray-600'
                            }">
                                ${
                                    isCompleted ? '完了' :
                                    isReady ? '実施可能' :
                                    '未到達'
                                }
                            </span>
                        </div>

                        <div class="text-sm text-gray-600 space-y-1">
                            <p>予定日: ${formatDate(task.due_date)}</p>
                            ${task.completed_at ? `
                                <p class="text-green-600">完了日時: ${formatDateTime(task.completed_at)}</p>
                            ` : ''}
                        </div>

                        ${isReady && !isCompleted ? `
                            <button
                                onclick="completeTask(${task.id})"
                                class="mt-3 px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors"
                            >
                                完了にする
                            </button>
                        ` : ''}

                        ${isCompleted ? `
                            <button
                                onclick="uncompleteTask(${task.id})"
                                class="mt-3 px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white text-sm rounded transition-colors"
                            >
                                完了を取り消す
                            </button>
                        ` : ''}
                    </div>
                </div>
            `;
        }).join('');

    } catch (error) {
        console.error('Failed to load item detail:', error);
        titleElement.textContent = 'エラー';
        contentElement.textContent = error.message;
        progressContainer.innerHTML = '';
    }
}

/**
 * 復習タスクを完了
 */
async function completeTask(taskId) {
    try {
        await api.completeReviewTask(taskId);
        showNotification('復習タスクを完了しました！', 'success');

        // ページをリロード
        const params = new URLSearchParams(window.location.search);
        const itemId = params.get('id');
        loadItemDetail(itemId);
    } catch (error) {
        console.error('Failed to complete task:', error);
        showNotification('エラー: ' + error.message, 'error');
    }
}

/**
 * 復習タスクの完了を取り消し
 */
async function uncompleteTask(taskId) {
    if (!confirm('完了を取り消しますか？')) {
        return;
    }

    try {
        await api.uncompleteReviewTask(taskId);
        showNotification('完了を取り消しました', 'success');

        // ページをリロード
        const params = new URLSearchParams(window.location.search);
        const itemId = params.get('id');
        loadItemDetail(itemId);
    } catch (error) {
        console.error('Failed to uncomplete task:', error);
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
 * 日付をフォーマット
 */
function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ja-JP', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
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
