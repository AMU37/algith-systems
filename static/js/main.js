document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navGroups = document.querySelectorAll('.nav-group');

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });
    }

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            sidebar.classList.toggle('mobile-open');
        });
    }

    navGroups.forEach(function(group) {
        const toggle = group.querySelector('.nav-group-toggle');
        if (toggle) {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                group.classList.toggle('open');
            });
        }
    });

    document.addEventListener('click', function(e) {
        if (sidebar && sidebar.classList.contains('mobile-open')) {
            if (!sidebar.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                sidebar.classList.remove('mobile-open');
            }
        }
    });

    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(function(flash) {
        setTimeout(function() {
            flash.style.opacity = '0';
            flash.style.transform = 'translateY(-10px)';
            setTimeout(function() {
                flash.remove();
            }, 300);
        }, 5000);
    });

    let deferredPrompt;
    const installBtn = document.getElementById('installApp');
    window.addEventListener('beforeinstallprompt', function(e) {
        e.preventDefault();
        deferredPrompt = e;
        if (installBtn) installBtn.style.display = 'block';
    });
    if (installBtn) {
        installBtn.addEventListener('click', function() {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then(function(result) {
                    deferredPrompt = null;
                    installBtn.style.display = 'none';
                });
            }
        });
    }
});

function openModal(id) {
    document.getElementById(id).classList.add('active');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}

function confirmDelete(message, formId) {
    if (confirm(message || 'هل أنت متأكد من الحذف؟')) {
        document.getElementById(formId).submit();
    }
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('ar-YE', {
        style: 'currency',
        currency: 'YER',
        minimumFractionDigits: 0
    }).format(amount);
}

function formatDate(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleDateString('ar-YE', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function addSaleItem() {
    const container = document.getElementById('saleItems');
    if (!container) return;
    const products = JSON.parse(document.getElementById('productsData')?.textContent || '[]');
    const index = container.children.length;

    const item = document.createElement('div');
    item.className = 'sale-item';
    item.innerHTML = `
        <div class="form-row">
            <div class="form-group">
                <label>المنتج/الخدمة</label>
                <select class="form-control product-select" onchange="updateSalePrice(this, ${index})">
                    <option value="">اختر...</option>
                    ${products.map(p => `<option value="${p.id}" data-price="${p.sale_price}">${p.name}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>الكمية</label>
                <input type="number" class="form-control item-quantity" value="1" min="1" onchange="updateSaleTotal(${index})">
            </div>
            <div class="form-group">
                <label>السعر</label>
                <input type="number" class="form-control item-price" value="0" step="0.01" onchange="updateSaleTotal(${index})">
            </div>
            <div class="form-group">
                <label>الإجمالي</label>
                <input type="number" class="form-control item-total" value="0" readonly>
            </div>
            <div class="form-group">
                <label>&nbsp;</label>
                <button type="button" class="btn btn-danger btn-icon" onclick="this.closest('.sale-item').remove(); updateSaleInvoiceTotal();">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
    container.appendChild(item);
}

function updateSalePrice(select, index) {
    const price = select.options[select.selectedIndex].dataset.price || 0;
    const item = select.closest('.sale-item');
    item.querySelector('.item-price').value = price;
    updateSaleTotal(index);
}

function updateSaleTotal(index) {
    const items = document.querySelectorAll('.sale-item');
    const item = items[index];
    if (!item) return;
    const qty = parseFloat(item.querySelector('.item-quantity').value) || 0;
    const price = parseFloat(item.querySelector('.item-price').value) || 0;
    item.querySelector('.item-total').value = (qty * price).toFixed(2);
    updateSaleInvoiceTotal();
}

function updateSaleInvoiceTotal() {
    let total = 0;
    document.querySelectorAll('.item-total').forEach(function(input) {
        total += parseFloat(input.value) || 0;
    });
    const totalInput = document.getElementById('saleTotal');
    if (totalInput) totalInput.value = total.toFixed(2);
}

function collectSaleItems() {
    const items = [];
    document.querySelectorAll('.sale-item').forEach(function(item) {
        const select = item.querySelector('.product-select');
        items.push({
            product_id: select?.value || '',
            product_name: select?.options[select.selectedIndex]?.text || '',
            quantity: item.querySelector('.item-quantity')?.value || 0,
            price: item.querySelector('.item-price')?.value || 0,
            total: item.querySelector('.item-total')?.value || 0
        });
    });
    return JSON.stringify(items);
}

function addPurchaseItem() {
    const container = document.getElementById('purchaseItems');
    if (!container) return;
    const products = JSON.parse(document.getElementById('productsData')?.textContent || '[]');
    const index = container.children.length;

    const item = document.createElement('div');
    item.className = 'purchase-item';
    item.innerHTML = `
        <div class="form-row">
            <div class="form-group">
                <label>المنتج/الخدمة</label>
                <select class="form-control product-select" onchange="updatePurchasePrice(this, ${index})">
                    <option value="">اختر...</option>
                    ${products.map(p => `<option value="${p.id}" data-price="${p.purchase_price}">${p.name}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>الكمية</label>
                <input type="number" class="form-control item-quantity" value="1" min="1" onchange="updatePurchaseTotal(${index})">
            </div>
            <div class="form-group">
                <label>السعر</label>
                <input type="number" class="form-control item-price" value="0" step="0.01" onchange="updatePurchaseTotal(${index})">
            </div>
            <div class="form-group">
                <label>الإجمالي</label>
                <input type="number" class="form-control item-total" value="0" readonly>
            </div>
            <div class="form-group">
                <label>&nbsp;</label>
                <button type="button" class="btn btn-danger btn-icon" onclick="this.closest('.purchase-item').remove(); updatePurchaseInvoiceTotal();">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
    container.appendChild(item);
}

function updatePurchasePrice(select, index) {
    const price = select.options[select.selectedIndex].dataset.price || 0;
    const item = select.closest('.purchase-item');
    item.querySelector('.item-price').value = price;
    updatePurchaseTotal(index);
}

function updatePurchaseTotal(index) {
    const items = document.querySelectorAll('.purchase-item');
    const item = items[index];
    if (!item) return;
    const qty = parseFloat(item.querySelector('.item-quantity').value) || 0;
    const price = parseFloat(item.querySelector('.item-price').value) || 0;
    item.querySelector('.item-total').value = (qty * price).toFixed(2);
    updatePurchaseInvoiceTotal();
}

function updatePurchaseInvoiceTotal() {
    let total = 0;
    document.querySelectorAll('.item-total').forEach(function(input) {
        total += parseFloat(input.value) || 0;
    });
    const totalInput = document.getElementById('purchaseTotal');
    if (totalInput) totalInput.value = total.toFixed(2);
}

function collectPurchaseItems() {
    const items = [];
    document.querySelectorAll('.purchase-item').forEach(function(item) {
        const select = item.querySelector('.product-select');
        items.push({
            product_id: select?.value || '',
            product_name: select?.options[select.selectedIndex]?.text || '',
            quantity: item.querySelector('.item-quantity')?.value || 0,
            price: item.querySelector('.item-price')?.value || 0,
            total: item.querySelector('.item-total')?.value || 0
        });
    });
    return JSON.stringify(items);
}

function addJournalLine() {
    const container = document.getElementById('journalLines');
    if (!container) return;
    const line = document.createElement('div');
    line.className = 'journal-line';
    line.innerHTML = `
        <div class="form-row">
            <div class="form-group">
                <label>الحساب</label>
                <input type="text" class="form-control line-account" placeholder="اسم الحساب">
            </div>
            <div class="form-group">
                <label>البيان</label>
                <input type="text" class="form-control line-description" placeholder="الوصف">
            </div>
            <div class="form-group">
                <label>مدين</label>
                <input type="number" class="form-control line-debit" value="0" step="0.01" onchange="updateJournalBalance()">
            </div>
            <div class="form-group">
                <label>دائن</label>
                <input type="number" class="form-control line-credit" value="0" step="0.01" onchange="updateJournalBalance()">
            </div>
            <div class="form-group">
                <label>&nbsp;</label>
                <button type="button" class="btn btn-danger btn-icon" onclick="this.closest('.journal-line').remove(); updateJournalBalance();">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
    container.appendChild(line);
}

function updateJournalBalance() {
    let debit = 0, credit = 0;
    document.querySelectorAll('.line-debit').forEach(function(input) { debit += parseFloat(input.value) || 0; });
    document.querySelectorAll('.line-credit').forEach(function(input) { credit += parseFloat(input.value) || 0; });
    const balance = document.getElementById('journalBalance');
    if (balance) {
        const diff = debit - credit;
        balance.textContent = diff === 0 ? 'متوازن' : `غير متوازن (${diff.toFixed(2)})`;
        balance.style.color = diff === 0 ? 'var(--secondary)' : 'var(--danger)';
    }
}

function collectJournalLines() {
    const lines = [];
    document.querySelectorAll('.journal-line').forEach(function(line) {
        lines.push({
            account: line.querySelector('.line-account')?.value || '',
            description: line.querySelector('.line-description')?.value || '',
            debit: line.querySelector('.line-debit')?.value || 0,
            credit: line.querySelector('.line-credit')?.value || 0
        });
    });
    return JSON.stringify(lines);
}

function printPage(url) {
    window.open(url, '_blank', 'width=800,height=600');
}

function exportTable(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;
    let csv = [];
    const rows = table.querySelectorAll('tr');
    rows.forEach(function(row) {
        const cols = row.querySelectorAll('td, th');
        const rowData = [];
        cols.forEach(function(col) {
            rowData.push('"' + col.textContent.trim().replace(/"/g, '""') + '"');
        });
        csv.push(rowData.join(','));
    });
    const blob = new Blob(['\ufeff' + csv.join('\n')], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'export.csv';
    link.click();
}
