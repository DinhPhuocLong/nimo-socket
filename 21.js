function collectEgg() {
    const button = document.querySelector('.pl-icon_danmu_open');
    if (button) button.click();
    let flag = true;
    collectInterval = setInterval(function () {
            const collectBtn = document.querySelector('.nimo-box-gift__box__btn');
            const redEgg = document.querySelector('.interactive-gift-entry-box-wrap');
            if (redEgg) redEgg.click();
            let isBoxGift = document.querySelector('.nimo-room__chatroom__box-gift');
            if (collectBtn) collectBtn.click();
            const modal = document.querySelector('.act-interactive-gift-modal');
            const container = document.querySelector('.gift-entries-swiper');
            if (container) {
                const nodeList = container.querySelectorAll('.nimo-room__chatroom__box-gift-item');
                const nodeListToArray = [...nodeList];
                const ifHasBoxgift = nodeListToArray.some(item => {
                    const el = item.querySelector('.nimo-box-gift') || item.querySelector('.interactive-gift-entry-box-wrap');
                    if (el) {
                        return window.getComputedStyle(el).display == 'block' || window.getComputedStyle(el).display == 'flex'
                    }
                })
                if (!ifHasBoxgift) window.close();
            }
            if (modal) {
                const iframe = modal.querySelector('iframe');
                if (iframe) {
                    let innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc && flag == true) {
                        let joinButton = innerDoc.querySelector('.btn');
                        if (joinButton) {
                            joinButton.click();
                            flag = false;
                        }
                        let result = innerDoc.querySelector('.ig-result');
                        console.log('closeing');
                            if (result) {
                                flag = true;
                                let close = innerDoc.querySelector('.act-interactive-gift-modal-close');
                                if (close) {
                                    close.click();
                                }
                            }
                        }
                    }
                }

            }, 1);
    }
    collectEgg();