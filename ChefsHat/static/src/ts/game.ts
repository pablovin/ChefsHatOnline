document.addEventListener("DOMContentLoaded", () => {
    const overlayElem = document.getElementById("overlay") as HTMLElement;
    const playerContainers = Array.from(document.getElementsByClassName("player__container--clickable"));
    const allModals = document.getElementsByClassName("modal") as HTMLCollection;
    const modalPlayer = document.getElementById("modalPlayer") as HTMLElement;
    const cardsContainer = modalPlayer.getElementsByClassName("modal__player--cards")[0] as HTMLElement;
    const modalPlayerBtn = document.getElementById("modal--player__button") as HTMLElement;

    const animationDuration = window.getComputedStyle(document.documentElement).getPropertyValue('--animation-global-duration') as string;
    const animationDurationSeconds = parseFloat(animationDuration.replace(/\D+$/g, '')); //=== Remove s from duration
    const modalOpeningAnimationClass = "modal--opening";
    const modalClosingAnimationClass = "modal--closing";
    const modalAnimationTime:number = animationDurationSeconds * 1000;
    const modalFormTime:number = modalAnimationTime * 3;
    
    const SHARED_DATA = {
        is_pizza: ((window as any)._sharedData.IS_PIZZA as string === 'True') ? true : false,
        simulate_next_actions: ((window as any)._sharedData.SIMULATE_NEXT_ACTIONS as string === 'True') ? true : false,
        opponents_action: ((window as any)._sharedData.OPPONENTS_ACTION as string === 'True') ? true : false,
        has_error_message: ((window as any)._sharedData.HAS_ERROR_MESSAGE as string === 'True') ? true : false,
        action_done: ((window as any)._sharedData.ACTION_DONE as string === 'True') ? true : false,
        player_turn: parseInt((window as any)._sharedData.PLAYER_TURN),
    };

    const playersPortraitContainer = document.getElementById("playersPortrait") as HTMLElement;
    const playersLandscapeContainer = document.getElementById("playersLandscape") as HTMLElement;

    const screeData = {
        orientation: (screen.orientation || {}).type,
        width: window.innerWidth as number
    }

    let xTouchDown: number | null = null;
    let yTouchDown: number | null = null;

    //=== Handle touch start
    const handleTouchStart = (evt: any) => {
        xTouchDown = evt.touches[0].clientX;
        yTouchDown = evt.touches[0].clientY;
    };

    //=== Handle touch swipe
    const handleTouchMove = (evt: any) => {
        if (!xTouchDown || !yTouchDown)
            return;

        const xTouchUp = evt.touches[0].clientX;
        const yTouchUp = evt.touches[0].clientY;

        let xDiff = xTouchDown - xTouchUp;
        let yDiff = yTouchDown - yTouchUp;

        if (Math.abs(xDiff) > Math.abs(yDiff)) {
            if (xDiff > 0) {
                /* left swipe */
            } else {
                /* right swipe */
            }
        } else {
            if (yDiff > 0) {
                /* up swipe */
            } else {
                /* down swipe */
                handleModalClosing(modalPlayer);
            }
        }
        
        xTouchDown = null;
        yTouchDown = null;
    };

    const handlePlayersPosition = (): void => {
        screeData.orientation = (screen.orientation || {}).type;
        screeData.width = window.innerWidth;
        
        if (screeData.orientation.includes('portrait') && screeData.width <= 600) {
            console.info('Portrait mode')
            playersLandscapeContainer.classList.remove('active');            
            playersPortraitContainer.classList.add('active');
        } else {
            console.info('Landscape mode')
            playersPortraitContainer.classList.remove('active');
            playersLandscapeContainer.classList.add('active');
        }
    }

    handlePlayersPosition();

    //=== Close modal on outer click
    const handleClick = (event: Event): void => {
        const target = event.target as HTMLElement
        const modalPlayer = allModals.namedItem('modalPlayer') as HTMLElement;
        const modalError = allModals.namedItem('modalError') as HTMLElement;

        // Close player modal
        if (modalPlayer.classList.contains('active') && !isTargetModal(target)) {
            handleModalClosing(modalPlayer);
        } 
        
        // Close error modal
        if (modalError.classList.contains('active') && !isTargetModal(target)) {
            handleModalClosing(modalError);
        }
    }

    //=== Check if event came from modal
    const isTargetModal = (target: HTMLElement): boolean => {
        let isFromModal = false;
        let elements: HTMLElement[] = [];

        while (!isFromModal && target.classList.length > 0) {
            if (target.classList.contains('modal')) {
                isFromModal = true;
            }

            elements.unshift(target);
            target = target.parentNode as HTMLElement;
        }
        return isFromModal;
    }

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

        // Cleanup
        setTimeout(() => {
            modalElem.classList.remove(modalOpeningAnimationClass);
        }, modalAnimationTime);
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
            overlayElem.classList.remove('active')
        }, modalAnimationTime);
    }

    const handleFormWithDelay = (form: HTMLFormElement, delay = 1000): void => {
        setTimeout(() => {
            form.submit();
        }, delay);
    };

    const isChecked = (element: HTMLInputElement): boolean => {
        return element.getElementsByTagName('input')[0].checked;
    }

    const handleCardsSelection = (): void => {
        const cardsArray = Array.from(modalPlayer.getElementsByClassName('card'));

        if (cardsArray.some(isChecked)){
            modalPlayerBtn.removeAttribute('disabled')
            modalPlayerBtn.classList.remove('disabled');
        } else {
            modalPlayerBtn.setAttribute('disabled', 'disabled');
            modalPlayerBtn.classList.add('disabled');
        }
    }

    const handlePlayerModal = (event: Event): void => {
        event.stopPropagation();

        if (SHARED_DATA.player_turn === 0) {
            handleModalOpening(modalPlayer);
        }
    }

    //=== Show last action
    const showActionDoneModal = () => {
        return new Promise(resolve => {
            const modalActionDone = allModals.namedItem('modalActionDone') as HTMLElement;
            const closingTime: number = modalAnimationTime * 2;
            // Value too low don't show overlayElem on pizza ready
            const totalTime: number = modalAnimationTime * 4;   
            
            handleModalOpening(modalActionDone);

            setTimeout(() => {
                handleModalClosing(modalActionDone);
            }, closingTime);

            setTimeout(resolve, totalTime);
        });
    }

    //=== Handle action
    const handleActions = async () => {
        if (typeof SHARED_DATA === 'undefined') {
            return console.error('Shared data is undefined');
        }

        //=== Await for last action to be shown
        if (SHARED_DATA.action_done) {
            console.info('Show last action'); 
            await showActionDoneModal();
        }

        switch (true) {
            //=== error
            case (SHARED_DATA.has_error_message):
                console.info('Invalid move');
                const modalError = allModals.namedItem('modalError') as HTMLElement
                handleModalOpening(modalError);

                break;
            //=== Action simulation
            case (SHARED_DATA.opponents_action && SHARED_DATA.simulate_next_actions):
                console.info('Action simulation');
                const modalAction = allModals.namedItem("modalAction") as HTMLElement;
                const nextActionForm = document.getElementById("formNextAction") as HTMLFormElement;
                
                handleModalOpening(modalAction);
                handleFormWithDelay(nextActionForm, modalFormTime);
                break;
            //=== Pizza ready
            case (SHARED_DATA.is_pizza):
                console.info('Pizza ready');
                const modalPizza = allModals.namedItem("modalPizza") as HTMLElement;
                const formPizza = document.getElementById("formPizza") as HTMLFormElement;

                handleModalOpening(modalPizza);
                handleFormWithDelay(formPizza, modalFormTime);
                break;
            //=== Opponents turn
            case (SHARED_DATA.player_turn !== 0 && SHARED_DATA.opponents_action):
                console.info('Adversaries turn');
                const opponentForm = document.getElementById('opponentForm') as HTMLFormElement;
                handleFormWithDelay(opponentForm, modalFormTime);
                break;
                // Automatically show player modal
                //=== Player turn
                // case (SHARED_DATA.player_turn === 0 && !SHARED_DATA.has_error_message):
                //     console.info('Player turn');
                //     handleModalOpening(modalPlayer);
                //     break;
        }
    }

    handleActions();

    //=== Event binding
    window.addEventListener("click", handleClick);
    window.addEventListener("resize", handlePlayersPosition);
    cardsContainer.addEventListener("click", handleCardsSelection);
    modalPlayer.addEventListener('touchstart', handleTouchStart, false);
    modalPlayer.addEventListener('touchmove', handleTouchMove, false);
    // containers for landscape and portrait layouts
    for (const playerContainer of playerContainers) {
        playerContainer.addEventListener("click", handlePlayerModal);   
    }
});