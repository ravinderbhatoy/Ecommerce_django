(function ($) {
  "use strict";

  // Spinner
  var spinner = function () {
      setTimeout(function () {
          if ($('#spinner').length > 0) {
              $('#spinner').removeClass('show');
          }
      }, 1);
  };
  spinner(0);

  // Fixed Navbar
  $(window).scroll(function () {
      if ($(window).width() < 992) {
          if ($(this).scrollTop() > 55) {
              $('.fixed-top').addClass('shadow');
          } else {
              $('.fixed-top').removeClass('shadow');
          }
      } else {
          if ($(this).scrollTop() > 55) {
              $('.fixed-top').addClass('shadow').css('top', -55);
          } else {
              $('.fixed-top').removeClass('shadow').css('top', 0);
          }
      } 
  });
  
 // Back to top button
 $(window).scroll(function () {
  if ($(this).scrollTop() > 300) {
      $('.back-to-top').fadeIn('slow');
  } else {
      $('.back-to-top').fadeOut('slow');
  }
  });
  $('.back-to-top').click(function () {
      $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
      return false;
  });

  // Testimonial carousel
  $(".testimonial-carousel").owlCarousel({
      autoplay: true,
      smartSpeed: 2000,
      center: false,
      dots: true,
      loop: true,
      margin: 25,
      nav : true,
      navText : [
          '<i class="bi bi-arrow-left"></i>',
          '<i class="bi bi-arrow-right"></i>'
      ],
      responsiveClass: true,
      responsive: {
          0:{
              items:1
          },
          576:{
              items:1
          },
          768:{
              items:1
          },
          992:{
              items:2
          },
          1200:{
              items:2
          }
      }
  });

  // vegetable carousel
  $(".vegetable-carousel").owlCarousel({
      autoplay: true,
      smartSpeed: 1500,
      center: false,
      dots: true,
      loop: true,
      margin: 25,
      nav : true,
      navText : [
          '<i class="bi bi-arrow-left"></i>',
          '<i class="bi bi-arrow-right"></i>'
      ],
      responsiveClass: true,
      responsive: {
          0:{
              items:1
          },
          576:{
              items:1
          },
          768:{
              items:2
          },
          992:{
              items:3
          },
          1200:{
              items:4
          }
      }
  });


  // Modal Video
  $(document).ready(function () {
      var $videoSrc;
      $('.btn-play').click(function () {
          $videoSrc = $(this).data("src");
      });

      $('#videoModal').on('shown.bs.modal', function (e) {
          $("#video").attr('src', $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
      })

      $('#videoModal').on('hide.bs.modal', function (e) {
          $("#video").attr('src', $videoSrc);
      })
  });

})(jQuery);

// tracking price changes
  
$(".quantity button").on("click", function () {
  var button = $(this);
  var input = button.closest(".quantity").find("input");
  var oldValue = parseFloat(input.val());
  var newVal;

  if (button.hasClass("btn-plus")) {
      newVal = oldValue + 1;
  }else {
      newVal = oldValue > 1 ? oldValue - 1 : 1;
  }
  // updating the input value
  input.val(newVal);

  var cartProductPriceElement = button.closest("tr").find(".cart-product-price");
  var productTotalPriceElement = button.closest("tr").find(".product-total-price");

  var currentPrice = parseFloat(cartProductPriceElement.text().replace("$", ""));
  var newTotalPrice = (currentPrice * newVal).toFixed(2);

  productTotalPriceElement.text(newTotalPrice + " $");
  // Custom function to update the total cart value
  fetchTotal();
//   updateCart()
});

function getCsrfToken() {
  const tokenElement = document.getElementById('csrf-token');
    if (tokenElement) {
        console.log(tokenElement)
        return tokenElement.value;
    } else {
        console.error('CSRF token hidden input field not found');
        return '';
    }
}


async function updateCart(productId, productQuantity) {
    console.log('updating cart')
    // const productId = productQuantity.getAttribute('data')
    const response = await fetch(`update-cart/${productId}`, {
            method: 'POST',
            body: JSON.stringify({quantity: productQuantity}),
            headers: {
                "X-CSRFToken":csrftoken,
                "content-Type": "application/json"
            }
        })
    if (!response.ok){
        throw new Error('Network response was not ok')
    }else{
        const data =response.json()
        console.log(data)
        console.log(data['success'])
    }
}

function fetchTotal() {
  const cartTotalElement = document.getElementById("cart-total");
  const finalCartTotalElement = document.getElementById("final-total");
  const productTotal = document.getElementsByClassName("product-total-price");

  let sum = 0
  for(let i=0; i<productTotal.length; i++){
     const value = parseFloat(productTotal[i].innerText.replace("$", ""));
     sum = sum+value
  }
  finalCartTotalElement.innerText = (sum+3.00).toFixed(2)+ " $";
  cartTotalElement.innerText = sum.toFixed(2) + " $";
  // Your custom logic to update the total cart value
}   

document.addEventListener('DOMContentLoaded', ()=>{
    fetchTotal()
})



