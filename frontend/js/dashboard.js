// ダッシュボードのロジック

document.addEventListener('DOMContentLoaded', () => {
    loadTodayReviews();
    setupNewItemForm();
});

/**
 * 今日の復習タスクを読み込んで表示
 */
async function loadTodayReviews() {
    const container = document.getElementById('today-reviews');
    const countElement = document.getElementById('review-count');

    try {
        const tasks = await api.getTodayReviews();

        countElement.textContent = tasks.length;

        if (tasks.length === 0) {
            container.innerHTML = `
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
                    <p class="text-blue-700">今日の復習タスクはありません</p>
                    <p class="text-sm text-blue-600 mt-2">新しい学習項目を追加しましょう！</p>
                </div>
            `;
            return;
        }

        container.innerHTML = tasks.map(task => `
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div class="flex items-start justify-between">
                    <div class="flex-1">
                        <h3 class="text-lg font-semibold text-gray-900 mb-1">
                            学習項目 #${task.learning_item_id}
                        </h3>
                        <p class="text-sm text-gray-600 mb-2">
                            <span class="font-medium">${task.stage_name}</span>
                            <span class="mx-2">•</span>
                            予定日: ${formatDate(task.due_date)}
                        </p>
                        ${isPastDue(task.due_date) ?
                            '<span class="inline-block px-2 py-1 bg-red-100 text-red-700 text-xs rounded">期限超過</span>'
                            : ''
                        }
                    </div>
                    <button
                        onclick="completeTask(${task.id})"
                        class="ml-4 px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors"
                    >
                        完了
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load today reviews:', error);
        container.innerHTML = `
            <div class="bg-red-50 border border-red-200 rounded-lg p-4 text-center text-red-700">
                エラー: ${error.message}
            </div>
        `;
    }
}

/**
 * 復習タスクを完了
 */
async function completeTask(taskId) {
    try {
        await api.completeReviewTask(taskId);
        showNotification('復習タスクを完了しました！', 'success');
        loadTodayReviews();
    } catch (error) {
        console.error('Failed to complete task:', error);
        showNotification('エラー: ' + error.message, 'error');
    }
}

/**
 * 新規学習項目フォームのセットアップ
 */
function setupNewItemForm() {
    const form = document.getElementById('new-item-form');
    const modal = document.getElementById('new-item-modal');
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
        const content = document.getElementById('content').value;
        const startDate = document.getElementById('start_date').value;

        try {
            const data = { title, content };
            if (startDate) {
                data.start_date = startDate;
            }

            await api.createLearningItem(data);
            showNotification('学習項目を作成しました！', 'success');
            form.reset();
            modal.classList.add('hidden');
            loadTodayReviews();
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
function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ja-JP', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * 期限超過かチェック
 */
function isPastDue(dateStr) {
    const dueDate = new Date(dateStr);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return dueDate < today;
}
