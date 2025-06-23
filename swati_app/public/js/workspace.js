function generateWorkspaceCards() {
    // Remove previous cards
    $('#workspace-cards-container').remove();

    const $container = $(`
        <div id="workspace-cards-container" class="row" style="
            margin: 0 -10px;
            padding: 15px;
            width: 100%;
        "></div>
    `);

    // Add styles once
    if (!$('#workspace-cards-styles').length) {
        $('head').append(`
            <style id="workspace-cards-styles">
                #workspace-cards-container .workspace-card {
                    padding: 10px;
                }
                #workspace-cards-container .card {
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    overflow: hidden;
                    height: 100%;
                    transition: all 0.3s;
                    background: white;
                }
                #workspace-cards-container .card:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                }
                #workspace-cards-container .card-img-placeholder {
                    height: 120px;
                    background: #f5f7fa;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #8D99A6;
                    font-size: 32px;
                    font-weight: 500;
                }
                #workspace-cards-container .card-body {
                    padding: 15px;
                }
                #workspace-cards-container .card-title {
                    font-size: 15px;
                    font-weight: 600;
                    margin-bottom: 5px;
                    color: #36414C;
                }
                #workspace-cards-container .card-count {
                    color: #6c7680;
                    font-size: 13px;
                    margin-bottom: 10px;
                }
                #workspace-cards-container .btn-sm {
                    font-size: 12px;
                    padding: 3px 8px;
                }
            </style>
        `);
    }

    // Process widgets
    $('.shortcut-widget-box').each(function () {
        const $item = $(this);
        const $titleEl = $item.find('.widget-title');
        const title = $titleEl.length ? $titleEl.text().trim() : null;
        if (!title) return;

        const count = $item.find('.indicator-pill').text().trim() || '';
        const rawLink = $item.attr('aria-label') || '';
        const link = rawLink.trim();
        if (!link) return;

        const initials = title.split(' ').map(w => w[0]).join('').toUpperCase();

        $container.append(`
            <div class="col-md-3 workspace-card">
                <div class="card">
                    <div class="card-img-placeholder">${initials}</div>
                    <div class="card-body">
                        <h5 class="card-title">${title}</h5>
                        ${count ? `<p class="card-count">${count} items</p>` : ''}
                        <a href="/app/${link.replace(/\s+/g, '-').toLowerCase()}" 
                           class="btn btn-primary btn-sm">
                           Open
                        </a>
                    </div>
                </div>
            </div>
        `);
    });

    // Use safe wrapper (do not touch codex-editor!)
    if (!$('#workspace-cards-wrapper').length) {
        $('.layout-main-section').prepend('<div id="workspace-cards-wrapper"></div>');
    }
    $('#workspace-cards-wrapper').html($container);

    console.log('Generated cards for current workspace');
}

// Run on load
generateWorkspaceCards();

// Set up observer
const observer = new MutationObserver(() => {
    // Wait until widgets load
    if ($('.shortcut-widget-box .widget-title').length > 0) {
        observer.disconnect();
        setTimeout(() => {
            generateWorkspaceCards();
            observer.observe(document.querySelector('.layout-main-section'), {
                childList: true,
                subtree: true
            });
        }, 100); // allow rendering time
    }
});

// Start observing
observer.observe(document.querySelector('.layout-main-section'), {
    childList: true,
    subtree: true
});

