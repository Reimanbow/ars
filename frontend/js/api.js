// APIクライアント

const api = {
    // ============================================================================
    // 学習項目API
    // ============================================================================

    /**
     * 新規学習項目を作成
     */
    async createLearningItem(data) {
        const response = await fetch(`${API_BASE_URL}/learning-items/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create learning item');
        }
        return response.json();
    },

    /**
     * 学習項目の一覧を取得
     */
    async getLearningItems(limit = 100, offset = 0) {
        const response = await fetch(
            `${API_BASE_URL}/learning-items/?limit=${limit}&skip=${offset}`
        );
        if (!response.ok) {
            throw new Error('Failed to fetch learning items');
        }
        return response.json();
    },

    /**
     * 学習項目の詳細を取得
     */
    async getLearningItem(id) {
        const response = await fetch(`${API_BASE_URL}/learning-items/${id}`);
        if (!response.ok) {
            throw new Error('Failed to fetch learning item');
        }
        return response.json();
    },

    /**
     * 学習項目を更新
     */
    async updateLearningItem(id, data) {
        const response = await fetch(`${API_BASE_URL}/learning-items/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to update learning item');
        }
        return response.json();
    },

    /**
     * 学習項目を削除
     */
    async deleteLearningItem(id) {
        const response = await fetch(`${API_BASE_URL}/learning-items/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to delete learning item');
        }
        return true;
    },

    // ============================================================================
    // 復習タスクAPI
    // ============================================================================

    /**
     * 今日の復習タスクを取得
     */
    async getTodayReviews() {
        const response = await fetch(`${API_BASE_URL}/review-tasks/today`);
        if (!response.ok) {
            throw new Error('Failed to fetch today reviews');
        }
        return response.json();
    },

    /**
     * 復習タスクを完了
     */
    async completeReviewTask(id) {
        const response = await fetch(`${API_BASE_URL}/review-tasks/${id}/complete`, {
            method: 'POST'
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to complete review task');
        }
        return response.json();
    },

    /**
     * 復習タスクの完了を取り消し
     */
    async uncompleteReviewTask(id) {
        const response = await fetch(`${API_BASE_URL}/review-tasks/${id}/uncomplete`, {
            method: 'POST'
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to uncomplete review task');
        }
        return response.json();
    }
};
