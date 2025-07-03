// 主JavaScript文件 - VCD管理系统

$(document).ready(function() {
    // 初始化
    initializeApp();
    
    // 设置CSRF令牌（如果需要）
    setupCSRF();
    
    // 设置全局AJAX错误处理
    setupGlobalErrorHandling();
    
    // 初始化工具提示
    initializeTooltips();
    
    // 设置导航高亮
    highlightActiveNavigation();
});

/**
 * 初始化应用
 */
function initializeApp() {
    console.log('VCD管理系统初始化完成');
    
    // 检查浏览器兼容性
    checkBrowserCompatibility();
    
    // 设置自动保存表单数据
    setupAutoSave();
    
    // 初始化键盘快捷键
    setupKeyboardShortcuts();
}

/**
 * 设置CSRF保护
 */
function setupCSRF() {
    // 在实际生产环境中，这里应该设置CSRF令牌
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                // xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
}

/**
 * 设置全局AJAX错误处理
 */
function setupGlobalErrorHandling() {
    $(document).ajaxError(function(event, xhr, settings, thrownError) {
        console.error('AJAX错误:', thrownError, xhr.responseText);
        
        if (xhr.status === 500) {
            showErrorMessage('服务器内部错误，请稍后再试');
        } else if (xhr.status === 404) {
            showErrorMessage('请求的资源不存在');
        } else if (xhr.status === 403) {
            showErrorMessage('没有权限执行此操作');
        } else if (xhr.status === 0) {
            showErrorMessage('网络连接失败，请检查网络连接');
        }
    });
    
    // 设置AJAX加载指示器 - 使用新的通知系统
    $(document).ajaxStart(function() {
        notifications.showLoading();
    }).ajaxStop(function() {
        notifications.hideLoading();
    });
}

/**
 * 初始化工具提示
 */
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * 高亮当前页面导航
 */
function highlightActiveNavigation() {
    var currentPath = window.location.pathname;
    $('.navbar-nav .nav-link').each(function() {
        var href = $(this).attr('href');
        if (href === currentPath) {
            $(this).addClass('active');
        } else {
            $(this).removeClass('active');
        }
    });
}

/**
 * 检查浏览器兼容性
 */
function checkBrowserCompatibility() {
    // 检查是否支持必要的API
    if (!window.fetch) {
        showErrorMessage('您的浏览器版本过低，可能无法正常使用所有功能，建议升级浏览器');
    }
    
    if (!window.localStorage) {
        console.warn('浏览器不支持localStorage');
    }
}

/**
 * 设置自动保存表单数据
 */
function setupAutoSave() {
    // 为表单字段添加自动保存功能
    $('form input, form select, form textarea').on('blur', function() {
        var formId = $(this).closest('form').attr('id');
        var fieldName = $(this).attr('name');
        var fieldValue = $(this).val();
        
        if (formId && fieldName && window.localStorage) {
            var key = `autosave_${formId}_${fieldName}`;
            localStorage.setItem(key, fieldValue);
        }
    });
    
    // 恢复自动保存的表单数据
    $('form').each(function() {
        var formId = $(this).attr('id');
        if (formId && window.localStorage) {
            $(this).find('input, select, textarea').each(function() {
                var fieldName = $(this).attr('name');
                if (fieldName) {
                    var key = `autosave_${formId}_${fieldName}`;
                    var savedValue = localStorage.getItem(key);
                    if (savedValue) {
                        $(this).val(savedValue);
                    }
                }
            });
        }
    });
}

/**
 * 设置键盘快捷键
 */
function setupKeyboardShortcuts() {
    $(document).keydown(function(e) {
        // Ctrl + S: 快速保存
        if (e.ctrlKey && e.keyCode === 83) {
            e.preventDefault();
            var activeModal = $('.modal.show');
            if (activeModal.length > 0) {
                activeModal.find('.btn-primary').first().click();
            }
        }
        
        // ESC: 关闭模态框
        if (e.keyCode === 27) {
            $('.modal.show').modal('hide');
        }
        
        // F5: 刷新当前页面数据
        if (e.keyCode === 116) {
            e.preventDefault();
            refreshCurrentPageData();
        }
    });
}

/**
 * 刷新当前页面数据
 */
function refreshCurrentPageData() {
    var currentPath = window.location.pathname;
    
    if (currentPath.includes('/vcds')) {
        if (typeof loadVcds === 'function') loadVcds();
    } else if (currentPath.includes('/inventory')) {
        if (typeof loadInventory === 'function') loadInventory();
    } else if (currentPath.includes('/sales')) {
        if (typeof loadSales === 'function') loadSales();
    } else if (currentPath.includes('/rentals')) {
        if (typeof loadRentals === 'function') loadRentals();
    } else if (currentPath.includes('/statistics')) {
        if (typeof loadStatistics === 'function') loadStatistics();
    } else if (currentPath === '/') {
        if (typeof loadDashboardStats === 'function') loadDashboardStats();
    }
}

/**
 * 显示错误消息
 */
function showErrorMessage(message) {
    showToast('错误', message, 'danger');
}

/**
 * 显示成功消息
 */
function showSuccessMessage(message) {
    showToast('成功', message, 'success');
}

/**
 * 显示警告消息
 */
function showWarningMessage(message) {
    showToast('警告', message, 'warning');
}

/**
 * 显示信息消息
 */
function showInfoMessage(message) {
    showToast('信息', message, 'info');
}

/**
 * 显示Toast消息
 */
function showToast(title, message, type = 'info') {
    var toastId = 'toast_' + Date.now();
    var typeClass = type === 'danger' ? 'text-bg-danger' : 
                   type === 'success' ? 'text-bg-success' :
                   type === 'warning' ? 'text-bg-warning' : 'text-bg-info';
    
    var toastHtml = `
        <div id="${toastId}" class="toast ${typeClass}" role="alert">
            <div class="toast-header">
                <strong class="me-auto">${title}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    // 如果没有toast容器，创建一个
    if ($('#toastContainer').length === 0) {
        $('body').append('<div id="toastContainer" class="toast-container position-fixed top-0 end-0 p-3"></div>');
    }
    
    $('#toastContainer').append(toastHtml);
    
    var toastElement = document.getElementById(toastId);
    var toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // 自动移除已隐藏的toast
    toastElement.addEventListener('hidden.bs.toast', function() {
        $(this).remove();
    });
}

// 旧的加载指示器函数已被新的通知系统替代

/**
 * 格式化日期
 */
function formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
    if (!(date instanceof Date)) {
        date = new Date(date);
    }
    
    var year = date.getFullYear();
    var month = String(date.getMonth() + 1).padStart(2, '0');
    var day = String(date.getDate()).padStart(2, '0');
    var hours = String(date.getHours()).padStart(2, '0');
    var minutes = String(date.getMinutes()).padStart(2, '0');
    var seconds = String(date.getSeconds()).padStart(2, '0');
    
    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds);
}

/**
 * 格式化货币
 */
function formatCurrency(amount, currency = '¥') {
    if (isNaN(amount)) return currency + '0.00';
    return currency + parseFloat(amount).toFixed(2);
}

/**
 * 验证表单
 */
function validateForm(formId) {
    var form = document.getElementById(formId);
    if (!form) return false;
    
    var isValid = true;
    var firstInvalidField = null;
    
    $(form).find('[required]').each(function() {
        var field = $(this);
        var value = field.val().trim();
        
        if (!value) {
            field.addClass('is-invalid');
            if (!firstInvalidField) {
                firstInvalidField = field;
            }
            isValid = false;
        } else {
            field.removeClass('is-invalid');
        }
    });
    
    // 特殊验证规则
    $(form).find('input[type="email"]').each(function() {
        var field = $(this);
        var email = field.val().trim();
        if (email && !isValidEmail(email)) {
            field.addClass('is-invalid');
            if (!firstInvalidField) {
                firstInvalidField = field;
            }
            isValid = false;
        }
    });
    
    $(form).find('input[type="tel"]').each(function() {
        var field = $(this);
        var phone = field.val().trim();
        if (phone && !isValidPhone(phone)) {
            field.addClass('is-invalid');
            if (!firstInvalidField) {
                firstInvalidField = field;
            }
            isValid = false;
        }
    });
    
    if (!isValid && firstInvalidField) {
        firstInvalidField.focus();
    }
    
    return isValid;
}

/**
 * 验证邮箱格式
 */
function isValidEmail(email) {
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * 验证手机号格式
 */
function isValidPhone(phone) {
    var re = /^1[3-9]\d{9}$/;
    return re.test(phone);
}

/**
 * 清除表单自动保存数据
 */
function clearFormAutoSave(formId) {
    if (!window.localStorage) return;
    
    var keysToRemove = [];
    for (var i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        if (key && key.startsWith(`autosave_${formId}_`)) {
            keysToRemove.push(key);
        }
    }
    
    keysToRemove.forEach(function(key) {
        localStorage.removeItem(key);
    });
}

/**
 * 导出数据为Excel
 */
function exportToExcel(data, filename) {
    // 这里使用简单的CSV导出，在实际项目中可以使用SheetJS等库
    var csvContent = '';
    
    // 添加表头
    if (data.length > 0) {
        csvContent += Object.keys(data[0]).join(',') + '\n';
    }
    
    // 添加数据行
    data.forEach(function(row) {
        csvContent += Object.values(row).map(function(value) {
            return '"' + String(value).replace(/"/g, '""') + '"';
        }).join(',') + '\n';
    });
    
    // 下载文件
    var blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    var link = document.createElement('a');
    var url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename + '.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

/**
 * 获取Cookie值
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 现代化通知系统

// Toast通知系统
class NotificationSystem {
    constructor() {
        this.createToastContainer();
        this.createLoadingOverlay();
    }

    // 创建Toast容器
    createToastContainer() {
        if (!document.querySelector('.toast-container')) {
            const container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
    }

    // 创建加载遮罩
    createLoadingOverlay() {
        if (!document.querySelector('.loading-overlay')) {
            const overlay = document.createElement('div');
            overlay.className = 'loading-overlay';
            overlay.innerHTML = `
                <div class="text-center">
                    <div class="loading-spinner"></div>
                    <div class="loading-text">处理中...</div>
                </div>
            `;
            document.body.appendChild(overlay);
        }
    }

    // 显示Toast通知
    showToast(message, type = 'info', duration = 4000) {
        const container = document.querySelector('.toast-container');
        const toastId = 'toast-' + Date.now();
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };

        const toast = document.createElement('div');
        toast.id = toastId;
        toast.className = `custom-toast ${type}`;
        toast.innerHTML = `
            <div class="toast-body d-flex align-items-center p-3">
                <i class="${icons[type]} me-3" style="font-size: 20px;"></i>
                <div class="flex-grow-1">${message}</div>
                <button type="button" class="btn-close btn-close-white ms-3" onclick="notifications.hideToast('${toastId}')"></button>
            </div>
        `;

        container.appendChild(toast);

        // 自动隐藏
        setTimeout(() => {
            this.hideToast(toastId);
        }, duration);

        return toastId;
    }

    // 隐藏Toast
    hideToast(toastId) {
        const toast = document.getElementById(toastId);
        if (toast) {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }
    }

    // 显示成功通知
    success(message, duration = 4000) {
        return this.showToast(message, 'success', duration);
    }

    // 显示错误通知
    error(message, duration = 6000) {
        return this.showToast(message, 'error', duration);
    }

    // 显示警告通知
    warning(message, duration = 5000) {
        return this.showToast(message, 'warning', duration);
    }

    // 显示信息通知
    info(message, duration = 4000) {
        return this.showToast(message, 'info', duration);
    }

    // 显示加载遮罩
    showLoading(text = '处理中...') {
        const overlay = document.querySelector('.loading-overlay');
        const textElement = overlay.querySelector('.loading-text');
        textElement.textContent = text;
        overlay.style.display = 'flex';
    }

    // 隐藏加载遮罩
    hideLoading() {
        const overlay = document.querySelector('.loading-overlay');
        overlay.style.display = 'none';
    }

    // 确认对话框
    confirm(title, message, confirmText = '确认', cancelText = '取消') {
        return new Promise((resolve) => {
            const modalId = 'confirm-modal-' + Date.now();
            const modal = document.createElement('div');
            modal.id = modalId;
            modal.className = 'modal fade confirm-modal';
            modal.innerHTML = `
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-question-circle text-warning me-2"></i>
                                ${title}
                            </h5>
                        </div>
                        <div class="modal-body">
                            <p class="mb-0">${message}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">${cancelText}</button>
                            <button type="button" class="btn btn-primary confirm-btn">${confirmText}</button>
                        </div>
                    </div>
                </div>
            `;

            document.body.appendChild(modal);

            const bootstrapModal = new bootstrap.Modal(modal);
            
            // 绑定事件
            modal.querySelector('.confirm-btn').addEventListener('click', () => {
                bootstrapModal.hide();
                resolve(true);
            });

            modal.addEventListener('hidden.bs.modal', () => {
                document.body.removeChild(modal);
                resolve(false);
            });

            bootstrapModal.show();
        });
    }

    // 进度提示
    showProgress(message, progress = 0) {
        const overlay = document.querySelector('.loading-overlay');
        overlay.innerHTML = `
            <div class="text-center">
                <div class="loading-spinner"></div>
                <div class="loading-text">${message}</div>
                <div class="progress mt-3" style="width: 200px;">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" 
                         style="width: ${progress}%"></div>
                </div>
            </div>
        `;
        overlay.style.display = 'flex';
    }

    // 更新进度
    updateProgress(progress) {
        const progressBar = document.querySelector('.loading-overlay .progress-bar');
        if (progressBar) {
            progressBar.style.width = progress + '%';
        }
    }
}

// 创建全局通知实例
const notifications = new NotificationSystem();

// 按钮加载状态管理
class ButtonLoader {
    static setLoading(button, loadingText = '处理中...') {
        if (typeof button === 'string') {
            button = document.querySelector(button);
        }
        
        if (button) {
            button.disabled = true;
            button.classList.add('btn-loading');
            button.setAttribute('data-original-text', button.innerHTML);
            button.innerHTML = loadingText;
        }
    }

    static removeLoading(button) {
        if (typeof button === 'string') {
            button = document.querySelector(button);
        }
        
        if (button) {
            button.disabled = false;
            button.classList.remove('btn-loading');
            const originalText = button.getAttribute('data-original-text');
            if (originalText) {
                button.innerHTML = originalText;
                button.removeAttribute('data-original-text');
            }
        }
    }
}

// AJAX请求包装器
class ApiClient {
    static async request(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
            ...options
        };

        try {
            const response = await fetch(url, defaultOptions);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || '请求失败');
            }
            
            return data;
        } catch (error) {
            throw error;
        }
    }

    static async get(url) {
        return this.request(`${url}?t=${new Date().getTime()}`);
    }

    static async post(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async put(url, data) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async delete(url) {
        return this.request(url, {
            method: 'DELETE'
        });
    }
}

// 页面消息条
function showMessageBar(message, type = 'info', containerId = null) {
    const container = containerId ? document.getElementById(containerId) : document.querySelector('.container-fluid');
    
    // 移除现有消息条
    const existingBar = container.querySelector('.message-bar');
    if (existingBar) {
        existingBar.remove();
    }

    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };

    const messageBar = document.createElement('div');
    messageBar.className = `message-bar ${type}`;
    messageBar.innerHTML = `
        <i class="${icons[type]}"></i>
        <span>${message}</span>
        <button type="button" class="btn-close ms-auto" onclick="this.parentElement.remove()"></button>
    `;

    container.insertBefore(messageBar, container.firstChild);
    messageBar.style.display = 'flex';

    // 5秒后自动隐藏
    setTimeout(() => {
        if (messageBar.parentNode) {
            messageBar.remove();
        }
    }, 5000);
}

// 添加CSS动画样式
const style = document.createElement('style');
style.textContent = `
@keyframes slideOutRight {
    from {
        transform: translateX(0);
        opacity: 1;
    }
    to {
        transform: translateX(100%);
        opacity: 0;
    }
}
`;
document.head.appendChild(style);

// 导出全局对象
window.notifications = notifications;
window.ButtonLoader = ButtonLoader;
window.ApiClient = ApiClient;
window.showMessageBar = showMessageBar; 