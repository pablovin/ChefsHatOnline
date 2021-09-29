document.addEventListener("DOMContentLoaded", () => {
  const overlayElem = document.getElementById("overlay") as HTMLElement;
  const imageLinks = document.getElementsByClassName('img__link') as HTMLCollection;
  const modalLightbox = document.getElementById("lightbox") as HTMLElement;
  const modalLightboxImages = modalLightbox.getElementsByClassName("lightbox--img") as HTMLCollection;
  const modalLightboxControls = modalLightbox.getElementsByClassName("lightbox--control") as HTMLCollection;
  const modalLightboxCloseBtn = document.getElementsByClassName("modal--lightbox--close")[0] as HTMLElement;
  
  const handleModalOpen = () => {
    overlayElem.classList.add('active');
    modalLightbox.classList.add('active');
  
    for (let lightboxControl of Array.from(modalLightboxControls)) {
      (lightboxControl as Element).addEventListener('click', handleModalControl);
    }
  };
  
  const handleModalClose = (event: Event) => {
    event.preventDefault();
    overlayElem.classList.remove('active');
    modalLightbox.classList.remove('active');
  
    for (const imgElem of Array.from(modalLightboxImages)) {
      imgElem.parentElement.classList.remove('active');
    }
  };
  
  let slideIndex = 1;
  const handleModalControl = (event: Event) => {
    const elem = event.target as HTMLElement;
  
    if (elem.classList.contains('next')) {
      if ((slideIndex + 1) <= modalLightboxImages.length) {
        slideIndex++;
      }
    }
    
    if (elem.classList.contains('prev')) {
      if ((slideIndex - 1) !== 0) {
        slideIndex--;
      }
    }
  
    handleSlideShow(slideIndex);
  }
  
  const handelImgClick = (event: Event) => {
    const elem = event.target as HTMLElement;
    if (elem.tagName.toLowerCase() === 'a') {
      event.preventDefault();
    }
  
    slideIndex = parseInt(elem.getAttribute('data-target')) || 1;
    
    handleModalOpen();
    handleSlideShow(slideIndex);
  }
  
  const handleSlideShow = (slideNumber: number) => {
    if (slideNumber === 0) {
      return;
    }
    
    for (const imgElem of Array.from(modalLightboxImages)) {
      if (slideNumber === parseInt(imgElem.getAttribute('data-img'))) {
        imgElem.parentElement.classList.add('active');
      } else {
        imgElem.parentElement.classList.remove('active');
      }
    }
  }
  
  modalLightboxCloseBtn.addEventListener('click', (event) => handleModalClose(event));

  // Handle click on rules images and rule book link
  for (const imageLink of Array.from(imageLinks)) {
    imageLink.addEventListener('click', (event) => handelImgClick(event));
  }
});