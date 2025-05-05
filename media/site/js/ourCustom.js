// $(document).ready(function () {
//     if ($("#moshakhasat").on("click")) {
//         if ($("#tozihat").hasClass("active-btn")){
//             $("#moshakhasat").addClass("active-btn");
//             $("#tozihat").removeClass("active-btn");
//             $("#Specifications").removeClass("d-none").addClass("d-block");
//             $("#description").toggleClass("d-none");
//         }
//     }
// });
  // custom coursor
  if ($(".custom-cursor").length) {
    var cursor = document.querySelector(".custom-cursor__cursor");
    var cursorinner = document.querySelector(".custom-cursor__cursor-two");
    var a = document.querySelectorAll("a");

    document.addEventListener("mousemove", function (e) {
        var x = e.clientX;
        var y = e.clientY;
        cursor.style.transform = `translate3d(calc(${e.clientX}px - 50%), calc(${e.clientY}px - 50%), 0)`;
    });

    document.addEventListener("mousemove", function (e) {
        var x = e.clientX;
        var y = e.clientY;
        cursorinner.style.left = x + "px";
        cursorinner.style.top = y + "px";
    });

    document.addEventListener("mousedown", function () {
        cursor.classList.add("click");
        cursorinner.classList.add("custom-cursor__innerhover");
    });

    document.addEventListener("mouseup", function () {
        cursor.classList.remove("click");
        cursorinner.classList.remove("custom-cursor__innerhover");
    });

    a.forEach((item) => {
        item.addEventListener("mouseover", () => {
            cursor.classList.add("custom-cursor__hover");
        });
        item.addEventListener("mouseleave", () => {
            cursor.classList.remove("custom-cursor__hover");
        });
    });
}

if ($(".listing-details__contact-info-phone").length) {
    $(".listing-details__contact-info-phone").on("click", function (e) {
        e.preventDefault();
        var textElement = $(this).find(".text h5");
        var mainText = textElement.data("number");
        var toggleText = textElement.data("toggle-number");
        if (textElement.text() == mainText) {
            textElement.text(toggleText);
        } else {
            textElement.text(mainText);
        }
    });
}

if ($(".listing-top__map-show-hide").length) {
    $(".listing-top__map-show-hide").on("click", function () {
        $(this).toggleClass("hidden");
        var textElement = $(this).find(".listing-top__map-show-hide-text span");
        if (textElement.text() == textElement.data("text")) {
            textElement.text(textElement.data("toggle-text"));
        } else {
            textElement.text(textElement.data("text"));
        }
        $(".listing__map").toggleClass("hidden");
        $(".listing__content").toggleClass("hidden");
    });
}

if ($("#datepicker").length) {
    $("#datepicker").datepicker();
}

if ($("#datepicker2").length) {
    $("#datepicker2").datepicker();
}

if ($("#datepicker-inline").length) {
    $("#datepicker-inline").datepicker();
}

$('input[name="time"]').ptTimeSelect();

if ($(".banner-bg-slide").length) {
    $(".banner-bg-slide").each(function () {
        var Self = $(this);
        var bgSlideOptions = Self.data("options");
        var bannerTwoSlides = Self.vegas(bgSlideOptions);
    });
}