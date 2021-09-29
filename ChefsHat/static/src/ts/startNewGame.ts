document.addEventListener("DOMContentLoaded", () => {
    const overlayElem = document.getElementById("overlay") as HTMLElement;
    const modalCardExchange = document.getElementById("modalCardExchange") as HTMLElement;
    const noCardsExchangeBtn = document.getElementById("noCardsExchangeBtn") as HTMLElement ?? null;
    const cardsContainer = document.getElementById("clickableCards") as HTMLElement;
    const cardExchangeBtn = document.getElementById("cardExchangeSubmit") as HTMLElement;

    const animationDuration = window.getComputedStyle(document.documentElement).getPropertyValue('--animation-global-duration');
    const animationDurationSeconds = parseFloat(animationDuration.replace(/\D+$/g, '')); //=== Remove s from duration
    const modalOpeningAnimationClass = "modal--opening";
    const modalClosingAnimationClass = "modal--closing";
    const modalAnimationTime: number = animationDurationSeconds * 1000;

    const SHARED_DATA = {
        player_has_role: ((window as any)._sharedData.PLAYER_HAS_ROLE as string === 'True') ? true : false,
        game_over: ((window as any)._sharedData.GAME_OVER as string === 'True') ? true : false,
    };

    const handleModalOpening = (modalElem: HTMLElement): void => {
        console.info('Opening modal');

        if (!overlayElem.classList.contains('active')) {
            overlayElem.classList.add('active')
        }

        if (modalElem.classList.contains(modalClosingAnimationClass)) {
            modalElem.classList.remove(modalClosingAnimationClass)
        }

        if (!modalElem.classList.contains(modalOpeningAnimationClass)) {
            modalElem.classList.add(modalOpeningAnimationClass);
        }
        
        modalElem.classList.add('active');
    }

    const handleModalClosing = (modalElem: HTMLElement): void => {
        console.info('Closing modal');

        if (modalElem.classList.contains(modalOpeningAnimationClass)) {
            modalElem.classList.remove(modalOpeningAnimationClass);
        }
        
        if (!modalElem.classList.contains(modalClosingAnimationClass)) {
            modalElem.classList.add(modalClosingAnimationClass)
        }

        // Cleanup
        setTimeout(() => {
            modalElem.classList.remove(modalClosingAnimationClass);
            modalElem.classList.remove('active');
            overlayElem.classList.remove('active');
        }, modalAnimationTime);
    }

    const isChecked = (element: HTMLInputElement): boolean => {
        return element.getElementsByTagName('input')[0].checked;
    }

    const handleCardsSelection = (): void => {
        const cardsArray = Array.from(cardsContainer.getElementsByClassName('card'));

        /* Check if almost two ar checked */
        let cardsCount = 0;
        for(let card of cardsArray) {
            if (isChecked(card as HTMLInputElement)) {
                ++cardsCount;
            }
        }
//         if (cardsCount <= 2) {
//             cardExchangeBtn.removeAttribute('disabled');
//             cardExchangeBtn.classList.remove('disabled');
//         } else {
//             cardExchangeBtn.setAttribute('disabled', 'disabled');
//             cardExchangeBtn.classList.add('disabled')
//         }
    }


    function handlePlayerModal(event: any): void {
        event.stopPropagation();
        handleModalClosing(modalCardExchange);
    }

    //=== Event binding
    if (!SHARED_DATA.game_over && SHARED_DATA.player_has_role) {
        console.info('It should open the modal');

        handleModalOpening(modalCardExchange);

        if (cardsContainer) {
            cardsContainer.addEventListener("click", handleCardsSelection);
        }

        if (! cardExchangeBtn == null) {
             cardExchangeBtn.addEventListener("click", handlePlayerModal);
        }
    }

//     else {
//         cardExchangeBtn.classList.remove('disabled');
//
//     }

    if (noCardsExchangeBtn) {
        noCardsExchangeBtn.addEventListener('click', () => handleModalClosing(modalCardExchange))
    }
});