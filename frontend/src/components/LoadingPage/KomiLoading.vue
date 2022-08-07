<template>
  <div v-if="showloading" ref="textdiv" class="tw-fixed tw-w-screen tw-h-screen tw-flex tw-justify-center tw-items-center tw-tracking-widest tw-flex-col tw-text-xl blinking tw-pointer-events-none animate__animated animate__fadeIn" style="z-index:6001;font-weight:200;opacity:1;transition:.5s ease-in-out">
    <div style="height:400px"></div>
    <div>服务准备中...</div>
  </div>
  <div v-if="showloading" ref="komidiv" class="div-body animate__animated animate__fadeIn" style="position: fixed; width:100vw;height:100vh;opacity:1;transition:.5s ease-in-out">
    <div class="komi">
      <div class="komi-head">
        <div class="komi-hair-back">
          <div class="komi-hair-back-1"></div>
        </div>
        <div class="komi-ear komi-ear-left"></div>
        <div class="komi-ear komi-ear-right"></div>
        <div class="komi-cat-ear komi-cat-ear-left">
          <div class="komi-cat-ear-fur"></div>
        </div>
        <div class="komi-cat-ear komi-cat-ear-right">
          <div class="komi-cat-ear-fur"></div>
        </div>
        <div class="komi-hair-strand"></div>
        <div class="komi-face"></div>
        <div class="komi-hair-bangs">
          <div class="komi-hair-bangs-1"></div>
          <div class="komi-hair-bangs-2"></div>
          <div class="komi-hair-bangs-3"></div>
        </div>
        <div class="komi-face-inner">
          <div class="komi-eye komi-eye-left">
            <div class="komi-eye-pupil">
              <div class="komi-eye-sparkle"></div>
            </div>
          </div>
          <div class="komi-eye komi-eye-right">
            <div class="komi-eye-pupil">
              <div class="komi-eye-sparkle"></div>
            </div>
          </div>
          <div class="komi-blush komi-blush-left"></div>
          <div class="komi-blush komi-blush-right"></div>
        </div>
      </div>
      <div class="komi-panel">
        <div class="komi-hair-extension"></div>
        <div class="komi-body">
          <div class="komi-neck">
            <div class="komi-neck-shadow"></div>
            <div class="komi-collar komi-collar-left"></div>
            <div class="komi-collar komi-collar-right"></div>
            <div class="komi-bow">
              <div class="komi-bow-top">
                <div class="komi-bow-top-shadow"></div>
              </div>
              <div class="komi-bow-bottom"></div>
            </div>
          </div>
          <div class="komi-shirt">
            <div class="komi-shirt-sleeves"></div>
            <div class="komi-shirt-sleeves-shadow"></div>
          </div>
        </div>
      </div>
      <div class="komi-zigzag komi-zigzag-1"></div>
      <div class="komi-zigzag komi-zigzag-2"></div>
      <div class="komi-zigzag komi-zigzag-3"></div>
      <div class="komi-zigzag komi-zigzag-4"></div>
      <div class="komi-zigzag komi-zigzag-5"></div>
      <div class="komi-zigzag komi-zigzag-6"></div>
      <div class="komi-zigzag komi-zigzag-7"></div>
      <div class="komi-zigzag komi-zigzag-8"></div>
      <div class="komi-zigzag komi-zigzag-9"></div>
      <div class="komi-zigzag komi-zigzag-10"></div>
      <div lang="ja" class="komi-buruburu">
        <span class="komi-buruburu-character komi-buruburu-character-1">
          ブ
        </span>
        <span class="komi-buruburu-character komi-buruburu-character-2">
          ル
        </span>
        <span class="komi-buruburu-character komi-buruburu-character-3">
          ル
        </span>
        <span class="komi-buruburu-character komi-buruburu-character-4">
          ル
        </span>
        <span class="komi-buruburu-character komi-buruburu-character-5">
          ル
        </span>
        <span class="komi-buruburu-character komi-buruburu-character-6">
          ル
        </span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect, nextTick } from 'vue'
import { useMainStore } from '@/stores' 
const mainStore = useMainStore();

let komidiv = ref()
let textdiv = ref()

let showloading = ref(false)
let show_loading_page_instantly = async () => {
  showloading.value = true
  await nextTick()
}

let lock = false
let hide_loading_page_slowly = () => {
  if (showloading.value) {
    if (!lock) {
      lock = true
      komidiv.value.classList.remove('animate__fadeIn')
      komidiv.value.classList.add('animate__fadeOut')
      textdiv.value.classList.remove('animate__fadeIn')
      textdiv.value.classList.add('animate__fadeOut')
      window.setTimeout(()=> {
        komidiv.value.classList.remove('animate__fadeOut')
        komidiv.value.classList.add('animate__fadeIn')
        textdiv.value.classList.remove('animate__fadeOut')
        textdiv.value.classList.add('animate__fadeIn')
        showloading.value = false
        lock = false
      }, 900)
    }
  }
}

watchEffect(() => {
  if (mainStore.ready === null) {
  } else if (!mainStore.ready) {
    show_loading_page_instantly()
  } else {
    hide_loading_page_slowly()
  }
})



</script>

<style scoped lang="scss">

  .blinking {
    animation: 3s wordsLoopAnimation linear infinite normal;
  }

  @keyframes wordsLoopAnimation {
    0% {
      opacity: 1;
    }

    60% {
      opacity: 0
    }

    90% {
      opacity: 1
    }

    100% {
      opacity: 1
    }
  }
    
  @keyframes blinky {
    0%, 9%, 11%, 19%, 21%, 69%, 71%, 100% {
      transform: scaleY(1);
    }
    10%, 20%, 70% {
      transform: scaleY(0);
    }
  }

  .testblock {
    box-sizing: border-box;
  }

  .div-body {
    display: grid;
    place-items: center;
    height: 100vh;
    background-color: var(--komi-background);
    font-size: 16px;
    line-height: 1;
    font-family: "Kiwi Maru", serif;
    overflow: hidden;
    z-index: 6000;
  }

  .komi {
    position: relative;
  }
  .komi *,
  .komi *::before,
  .komi *::after {
    position: absolute;
  }
  .komi-head, .komi-body, .komi-hair-extension {
    animation: var(--komi-hover-animation, none);
  }
  .komi-eye {
    top: 4.5rem;
    right: var(--komi-eye-right);
    bottom: auto;
    left: var(--komi-eye-left);
    --komi-flip: 1;
    --komi-eye-offset: 1.25rem;
    --komi-pupil-offset: 0.5rem;
    --komi-eye-line-top-offset: -13%;
    --komi-eye-line-bottom-offset: 16%;
    z-index: 2;
    height: 3.75rem;
    width: 4rem;
    transform-origin: center 70%;
    border-radius: 100%;
    background-color: var(--komi-white);
    animation: blinky 7s infinite;
  }
  .komi-eye::before, .komi-eye::after {
    content: "";
  }
  .komi-eye::before {
    top: -0.0625rem;
    right: var(--komi-eye-line-top-right);
    bottom: auto;
    left: var(--komi-eye-line-top-left);
    height: 120%;
    width: 120%;
    transform: rotate(calc(-12deg * var(--komi-flip)));
    border-radius: 100%;
    border: var(--komi-line-width-2) solid transparent;
    border-top: var(--komi-line-width-2) solid var(--komi-black);
  }
  .komi-eye::after {
    top: auto;
    right: var(--komi-eye-line-bottom-right);
    bottom: 0;
    left: var(--komi-eye-line-bottom-left);
    height: 15%;
    width: 50%;
    transform: rotate(calc(8deg * var(--komi-flip)));
    border-radius: 100%;
    border: var(--komi-line-width-1) solid transparent;
    border-bottom: var(--komi-line-width-1) solid var(--komi-black);
  }
  .komi-eye-sparkle {
    inset: 15% 20%;
    transform: scale(var(--komi-eye-sparkle-scale, 0));
    transition: 0.4s ease-in-out;
  }
  .komi-eye-sparkle::before, .komi-eye-sparkle::after {
    content: "";
    border-radius: 100%;
    background-color: var(--komi-sparkle-color);
  }
  .komi-eye-sparkle::before {
    left: 50%;
    height: 100%;
    width: 0.5rem;
    transform: translateX(-50%);
    animation: twinkleY 0.3s infinite;
  }
  .komi-eye-sparkle::after {
    top: 50%;
    width: 100%;
    height: 0.5rem;
    transform: translateY(-50%);
    animation: twinkleX 0.3s 0.3s infinite;
  }
  .komi-eye-pupil {
    top: 0.75rem;
    right: var(--komi-pupil-right);
    bottom: auto;
    left: var(--komi-pupil-left);
    height: 2.5rem;
    width: 2.5rem;
    transform: scale(var(--komi-eye-pupil-scale, 1));
    border-radius: 100%;
    background-color: var(--komi-black);
    transition: 0.4s ease-in-out;
    overflow: hidden;
  }
  .komi-eye-pupil::before {
    content: "";
    top: 60%;
    left: 50%;
    height: 100%;
    width: 130%;
    transform: translateX(-50%);
    border-radius: 100%;
    background-color: var(--komi-primary-color-tint);
  }
  .komi-eye-left {
    --komi-eye-left: var(--komi-eye-offset);
    --komi-pupil-right: var(--komi-pupil-offset);
    --komi-eye-line-top-left: var(--komi-eye-line-top-offset);
    --komi-eye-line-bottom-left: var(--komi-eye-line-bottom-offset);
  }
  .komi-eye-right {
    --komi-flip: -1;
    --komi-eye-right: var(--komi-eye-offset);
    --komi-pupil-left: var(--komi-pupil-offset);
    --komi-eye-line-top-right: var(--komi-eye-line-top-offset);
    --komi-eye-line-bottom-right: var(--komi-eye-line-bottom-offset);
  }
  .komi-blush {
    top: 7.5rem;
    right: var(--komi-blush-right);
    bottom: auto;
    left: var(--komi-blush-left);
    --komi-blush-offset: 0.75rem;
    height: 2rem;
    width: 2.5rem;
    border-radius: 100%;
    background-color: var(--komi-accent-color);
    opacity: var(--komi-blush-opacity, 0.1);
    transition: 0.8s;
  }
  .komi-blush-left {
    --komi-blush-left: var(--komi-blush-offset);
  }
  .komi-blush-right {
    --komi-blush-right: var(--komi-blush-offset);
  }
  .komi-ear {
    top: 5.75rem;
    right: var(--komi-ear-right);
    bottom: auto;
    left: var(--komi-ear-left);
    --komi-flip: 1;
    --komi-ear-offset: -1.25rem;
    height: 3rem;
    width: 2rem;
    transform: rotate(calc(40deg * var(--komi-flip)));
    border-radius: 100%;
    background-color: var(--komi-secondary-color);
  }
  .komi-ear-left {
    --komi-flip: -1;
    --komi-ear-left: var(--komi-ear-offset);
    z-index: -1;
  }
  .komi-ear-right {
    --komi-ear-right: var(--komi-ear-offset);
  }
  .komi-cat-ear {
    top: var(--komi-cat-ear-translate, 4rem);
    right: var(--komi-cat-ear-right);
    bottom: auto;
    left: var(--komi-cat-ear-left);
    --komi-flip: 1;
    --komi-cat-ear-offset: -3rem;
    --komi-cat-ear-fur-offset: 20%;
    --komi-cat-ear-fur-1-offset: 1.75rem;
    --komi-cat-ear-fur-2-offset: 1.5rem;
    z-index: -1;
    height: 6rem;
    width: 5rem;
    transition: 0.5s ease-in-out;
  }
  .komi-cat-ear::before {
    content: "";
    inset: 0;
    transform-origin: var(--komi-cat-ear-transform-origin);
    transform: rotate(calc(30deg * var(--komi-flip)));
    border-radius: inherit;
    background-color: var(--komi-primary-color);
  }
  .komi-cat-ear-fur {
    top: 10%;
    right: var(--komi-cat-ear-fur-right);
    bottom: auto;
    left: var(--komi-cat-ear-fur-left);
    height: 70%;
    width: 70%;
    transform-origin: var(--komi-cat-ear-transform-origin);
    transform: rotate(calc(30deg * var(--komi-flip)));
    border-radius: inherit;
    background-color: var(--komi-primary-color-tint);
  }
  .komi-cat-ear-fur::before, .komi-cat-ear-fur::after {
    content: "";
    border-radius: var(--komi-cat-ear-fur-border-radius);
    background-color: var(--komi-primary-color);
  }
  .komi-cat-ear-fur::before {
    top: -0.625rem;
    right: var(--komi-cat-ear-fur-1-right);
    bottom: auto;
    left: var(--komi-cat-ear-fur-1-left);
    height: 2rem;
    width: 2rem;
    transform: rotate(calc(-70deg * var(--komi-flip)));
  }
  .komi-cat-ear-fur::after {
    top: -0.25rem;
    right: var(--komi-cat-ear-fur-2-right);
    bottom: auto;
    left: var(--komi-cat-ear-fur-2-left);
    height: 1rem;
    width: 1rem;
    transform: rotate(calc(-50deg * var(--komi-flip)));
  }
  .komi-cat-ear-left {
    --komi-cat-ear-left: var(--komi-cat-ear-offset);
    --komi-cat-ear-transform-origin: right bottom;
    --komi-cat-ear-fur-left: var(--komi-cat-ear-fur-offset);
    --komi-cat-ear-fur-1-left: var(--komi-cat-ear-fur-1-offset);
    --komi-cat-ear-fur-2-left: var(--komi-cat-ear-fur-2-offset);
    --komi-cat-ear-fur-border-radius: 0 100% 0 100%;
    border-radius: 0.5rem 0 0 100%;
  }
  .komi-cat-ear-right {
    --komi-flip: -1;
    --komi-cat-ear-right: var(--komi-cat-ear-offset);
    --komi-cat-ear-transform-origin: left bottom;
    --komi-cat-ear-fur-right: var(--komi-cat-ear-fur-offset);
    --komi-cat-ear-fur-1-right: var(--komi-cat-ear-fur-1-offset);
    --komi-cat-ear-fur-2-right: var(--komi-cat-ear-fur-2-offset);
    --komi-cat-ear-fur-border-radius: 100% 0 100% 0;
    border-radius: 0 0.5rem 100% 0;
    animation: var(--komi-cat-ear-animation);
  }
  .komi-face {
    border-top-left-radius: 50% 50%;
    border-top-right-radius: 50% 50%;
    border-bottom-right-radius: 50% 40%;
    border-bottom-left-radius: 50% 40%;
    inset: 0;
    background-color: var(--komi-secondary-color);
  }
  .komi-face-inner {
    inset: 0;
  }
  .komi-hair-back {
    top: -2.75rem;
    left: -2rem;
    width: 120%;
  }
  .komi-hair-back-1 {
    width: 100%;
    height: 9.5rem;
    transform: rotate(-10deg);
    border-radius: 100%;
    background-color: var(--komi-primary-color);
  }
  .komi-hair-back-1::before, .komi-hair-back-1::after {
    content: "";
  }
  .komi-hair-back-1::before {
    top: 5.5rem;
    right: -1rem;
    width: 50%;
    height: 60%;
    background-color: inherit;
    border-radius: 100%;
  }
  .komi-hair-back-1::after {
    inset: 0;
    border-radius: inherit;
    border-left: 1rem solid var(--komi-primary-color-tint);
  }
  .komi-hair-bangs {
    top: -0.5rem;
    left: 25%;
    width: 65%;
  }
  .komi-hair-bangs::before, .komi-hair-bangs::after {
    content: "";
    z-index: 2;
    background-color: var(--komi-primary-color-tint);
  }
  .komi-hair-bangs::before {
    top: 2.5rem;
    left: -3.75rem;
    height: 1rem;
    width: 1rem;
    transform: rotate(-2deg) skewY(20deg);
    border-radius: 0.25rem;
  }
  .komi-hair-bangs::after {
    top: 2.25rem;
    left: 0.5rem;
    height: 1rem;
    width: 90%;
    transform: rotate(-2deg) skewY(10deg);
    border-radius: 0.25rem;
  }
  .komi-hair-bangs-1, .komi-hair-bangs-2 {
    transform-origin: center top;
    background-color: var(--komi-primary-color);
  }
  .komi-hair-bangs-1 {
    top: 0;
    left: 0;
    width: 55%;
    height: 6rem;
    transform: rotate(-8deg);
    border-bottom-left-radius: 100% 50%;
  }
  .komi-hair-bangs-1::before {
    content: "";
    left: -1.5rem;
    height: 80%;
    width: 3rem;
    border-bottom-left-radius: 100%;
    transform: rotate(50deg);
    border-left: 1.5rem solid var(--komi-primary-color);
  }
  .komi-hair-bangs-2 {
    top: 0;
    left: 50%;
    width: 45%;
    height: 6.5rem;
    transform: rotate(-12deg);
    border-bottom-left-radius: 100% 70%;
  }
  .komi-hair-bangs-3 {
    top: 1.5rem;
    left: -1.75rem;
    height: 6rem;
    width: 4.5rem;
    border-bottom-left-radius: 100%;
    transform-origin: center top;
    transform: rotate(45deg);
    border-left: 1.75rem solid var(--komi-primary-color);
  }
  .komi-hair-strand {
    z-index: -1;
    top: 4rem;
    left: -0.75rem;
    height: 13rem;
    width: 1.5rem;
    background-color: var(--komi-primary-color);
  }
  .komi-head {
    position: relative;
    z-index: 3;
    height: 12rem;
    width: 13rem;
    margin-bottom: 5rem;
  }
  .komi-hair-extension {
    top: 3rem;
    left: calc(50% - 7rem);
    width: 14rem;
    height: 14rem;
    background-color: var(--komi-primary-color);
  }
  .komi-hair-extension::after {
    content: "";
    left: 1rem;
    height: 100%;
    width: 5rem;
    background-color: var(--komi-primary-color-dark);
  }
  .komi-neck {
    z-index: 2;
    bottom: calc(100% - 0.25rem);
    left: 50%;
    height: 5rem;
    width: 2rem;
    transform: translateX(-50%);
    background-color: var(--komi-secondary-color);
  }
  .komi-neck::after {
    content: "";
    z-index: -1;
    top: calc(100% - 0.125rem);
    left: 50%;
    border: 1.125rem solid transparent;
    border-top-color: var(--komi-secondary-color);
    transform: translateX(-50%);
  }
  .komi-neck-shadow {
    inset: 0;
    overflow: hidden;
  }
  .komi-neck-shadow::before {
    content: "";
    top: 0.25rem;
    left: 50%;
    width: 250%;
    height: 3rem;
    border-radius: 100%;
    background-color: var(--komi-black);
    transform: translateX(-50%);
    opacity: 0.1;
  }
  .komi-collar {
    --komi-flip: 1;
    --komi-collar-offset: -4.4375rem;
    bottom: -0.5rem;
    left: 50%;
    height: 3rem;
    width: 100%;
    transform: translateX(-50%) skewY(calc(-15deg * var(--komi-flip))) scaleY(0.6);
  }
  .komi-collar::before {
    top: 0.5rem;
    right: var(--komi-collar-right);
    bottom: auto;
    left: var(--komi-collar-left);
    content: "";
    height: 0;
    width: 0;
    border: 2.5rem solid transparent;
    border-top-color: var(--komi-shirt-color);
    transform: rotate(calc(78deg * var(--komi-flip)));
  }
  .komi-collar-left {
    --komi-collar-left: var(--komi-collar-offset);
  }
  .komi-collar-right {
    --komi-flip: -1;
    --komi-collar-right: var(--komi-collar-offset);
  }
  .komi-bow {
    bottom: -1.875rem;
    left: 50%;
    height: 0.75rem;
    width: 1.25rem;
    transform: translateX(-50%);
  }
  .komi-bow::after {
    content: "";
    z-index: 3;
    inset: 0;
    border-radius: 0.75rem;
    background-color: var(--komi-bow-color-1);
    background-image: var(--komi-bow-gradient);
  }
  .komi-bow-top {
    --komi-flip: 1;
    --komi-bow-top-offset: 0.75rem;
    z-index: 2;
    inset: 0;
  }
  .komi-bow-top::before, .komi-bow-top::after {
    top: -0.25rem;
    right: var(--komi-bow-top-right);
    bottom: auto;
    left: var(--komi-bow-top-left);
    content: "";
    height: 1.75rem;
    width: 1.75rem;
    transform: rotate(calc(-15deg * var(--komi-flip))) perspective(1rem) rotateY(calc(22deg * var(--komi-flip)));
    background-color: var(--komi-bow-color-1);
    background-image: var(--komi-bow-gradient);
    border-radius: 0.25rem;
  }
  .komi-bow-top::before {
    --komi-bow-top-right: var(--komi-bow-top-offset);
  }
  .komi-bow-top::after {
    --komi-bow-top-left: var(--komi-bow-top-offset);
    --komi-flip: -1;
  }
  .komi-bow-top-shadow {
    --komi-bow-top-shadow-offset: 0.75rem;
    inset: 0;
  }
  .komi-bow-top-shadow::before, .komi-bow-top-shadow::after {
    top: 0.125rem;
    right: var(--komi-bow-top-shadow-right);
    bottom: auto;
    left: var(--komi-bow-top-shadow-left);
    content: "";
    z-index: 1;
    height: 0.75rem;
    width: 1.25rem;
    transform: rotate(calc(-15deg * var(--komi-flip)));
    border-radius: 100%;
    background-color: var(--komi-bow-color-2);
    mix-blend-mode: multiply;
    opacity: 0.4;
  }
  .komi-bow-top-shadow::before {
    --komi-bow-top-shadow-right: var(--komi-bow-top-shadow-offset);
  }
  .komi-bow-top-shadow::after {
    --komi-bow-top-shadow-left: var(--komi-bow-top-shadow-offset);
    --komi-flip: -1;
  }
  .komi-bow-bottom {
    --komi-flip: 1;
    --komi-bow-bottom-offset: -1.5rem;
    z-index: 1;
    inset: 0;
  }
  .komi-bow-bottom::before, .komi-bow-bottom::after {
    top: 0.325rem;
    right: var(--komi-bow-bottom-right);
    bottom: auto;
    left: var(--komi-bow-bottom-left);
    content: "";
    height: 1.75rem;
    width: 2rem;
    transform: rotate(calc(15deg * var(--komi-flip)));
    border-radius: 0.125rem;
    background-color: var(--komi-bow-color-1);
    background-image: var(--komi-bow-gradient);
  }
  .komi-bow-bottom::before {
    --komi-bow-bottom-left: var(--komi-bow-bottom-offset);
  }
  .komi-bow-bottom::after {
    --komi-bow-bottom-right: var(--komi-bow-bottom-offset);
    --komi-flip: -1;
  }
  .komi-shirt {
    --komi-flip: 1;
    z-index: 1;
    top: -0.5rem;
    left: 50%;
    width: 9rem;
    height: 8rem;
    transform: translateX(-50%);
  }
  .komi-shirt::before, .komi-shirt::after {
    top: 0;
    right: var(--komi-shirt-right);
    bottom: auto;
    left: var(--komi-shirt-left);
    content: "";
    z-index: 2;
    height: 100%;
    width: 70%;
    border-radius: 0.5rem;
    background-color: var(--komi-shirt-color-dark);
    transform: rotate(calc(8deg * var(--komi-flip)));
  }
  .komi-shirt::before {
    --komi-shirt-left: 0;
    --komi-flip: -1;
  }
  .komi-shirt::after {
    --komi-shirt-right: 0;
  }
  .komi-shirt-sleeves::before, .komi-shirt-sleeves::after {
    top: 1rem;
    right: var(--komi-shirt-sleeve-right);
    bottom: auto;
    left: var(--komi-shirt-sleeve-left);
    content: "";
    z-index: -1;
    height: 4rem;
    width: 4rem;
    border-radius: 0.25rem;
    background-color: var(--komi-shirt-color-dark);
    transform: rotate(calc(20deg * var(--komi-flip)));
  }
  .komi-shirt-sleeves::before {
    --komi-shirt-sleeve-left: -1.25rem;
  }
  .komi-shirt-sleeves::after {
    --komi-shirt-sleeve-right: -1.25rem;
    --komi-flip: -1;
  }
  .komi-shirt-sleeves, .komi-shirt-sleeves-shadow {
    inset: 0;
  }
  .komi-shirt-sleeves-shadow {
    z-index: 1;
  }
  .komi-shirt-sleeves-shadow::before, .komi-shirt-sleeves-shadow::after {
    top: 2.5rem;
    right: var(--komi-shirt-sleeve-sh-right);
    bottom: auto;
    left: var(--komi-shirt-sleeve-sh-left);
    content: "";
    height: 50%;
    width: 1.5rem;
    transform: rotate(calc(20deg * var(--komi-flip)));
    background-color: var(--komi-shirt-color-dark-2);
  }
  .komi-shirt-sleeves-shadow::before {
    --komi-shirt-sleeve-sh-left: -1rem;
  }
  .komi-shirt-sleeves-shadow::after {
    --komi-shirt-sleeve-sh-right: -1rem;
    --komi-flip: -1;
  }
  .komi-body {
    z-index: 1;
    top: 12rem;
    left: calc(50% - 6rem);
    height: 6rem;
    width: 12rem;
  }
  .komi-panel {
    top: 2rem;
    left: 50%;
    width: clamp(20rem, 50vw, 30rem);
    height: 15rem;
    transform: translateX(-50%);
    background-color: var(--komi-white);
    overflow: hidden;
  }
  .komi-zigzag {
    background-image: repeating-linear-gradient(45deg, var(--komi-primary-color-tint) 0 0.125rem, transparent 0.125rem 0.25rem);
    opacity: var(--komi-zigzag-opacity, 0);
    transition: 0.3s;
  }
  .komi-zigzag, .komi-zigzag::after {
    height: 0.125rem;
    width: 1.125rem;
  }
  .komi-zigzag::after {
    content: "";
    background-image: repeating-linear-gradient(-45deg, transparent 0 0.125rem, var(--komi-primary-color-tint) 0.125rem 0.25rem);
  }
  .komi-zigzag-1 {
    left: -2rem;
    bottom: 2rem;
    transform: rotate(85deg);
  }
  .komi-zigzag-2 {
    left: -2rem;
    bottom: 6rem;
    width: 0.875rem;
    transform: rotate(90deg);
  }
  .komi-zigzag-3 {
    left: -3rem;
    top: 5rem;
    transform: rotate(60deg);
  }
  .komi-zigzag-4 {
    left: -2rem;
    top: -1rem;
    transform: rotate(-40deg);
  }
  .komi-zigzag-5 {
    left: 5rem;
    top: -4rem;
    transform: rotate(-10deg);
  }
  .komi-zigzag-6 {
    right: -1rem;
    top: -2rem;
    transform: rotate(50deg);
  }
  .komi-zigzag-7 {
    right: -3.5rem;
    top: 4rem;
    transform: rotate(80deg);
  }
  .komi-zigzag-8 {
    right: -2.5rem;
    top: 8rem;
    width: 0.875rem;
    transform: rotate(-60deg);
  }
  .komi-zigzag-9 {
    right: -2rem;
    bottom: 5rem;
    transform: rotate(90deg);
  }
  .komi-zigzag-10 {
    right: -2rem;
    bottom: 1rem;
    transform: rotate(95deg);
  }
  .komi-zigzags {
    inset: 0;
  }
  .komi-buruburu {
    right: -3rem;
    top: 0;
    height: 100%;
    transform-origin: center bottom;
    transform: rotate(5deg) skewX(-10deg) scale(var(--komi-buruburu-scale, 0.7));
    font-size: 3rem;
    color: var(--komi-primary-color);
    opacity: var(--komi-buruburu-opacity, 0);
    transition: opacity 0.3s, transform 0.4s ease-in-out;
  }
  .komi-buruburu-character-1 {
    left: -0.25em;
    font-size: 1.2em;
  }
  .komi-buruburu-character-2 {
    top: 1.0625em;
    left: -0.125em;
  }
  .komi-buruburu-character-3 {
    top: 2em;
    left: -0.5em;
  }
  .komi-buruburu-character-4 {
    top: 3.25em;
    left: -0.625em;
    font-size: 0.9em;
  }
  .komi-buruburu-character-5 {
    top: 4.75em;
    left: -0.75em;
    font-size: 0.8em;
  }
  .komi-buruburu-character-6 {
    top: 6.5em;
    left: 0;
    left: -0.5em;
    font-size: 0.7em;
  }
  .komi:hover {
    --komi-hover-animation: tremble 0.3s infinite;
    --komi-eye-pupil-scale: 0.85;
    --komi-zigzag-opacity: 1;
    --komi-buruburu-opacity: 1;
    --komi-buruburu-scale: 1;
  }
  .komi-head:hover {
    --komi-eye-pupil-scale: 1.1;
    --komi-eye-sparkle-scale: 1;
    --komi-blush-opacity: 0.3;
    --komi-cat-ear-scale: 1;
    --komi-cat-ear-translate: -3rem;
    --komi-cat-ear-animation: catEarTwitch 3s 0.5s infinite;
  }
  .komi-head:hover,
  .komi-head:hover + .komi-panel {
    --komi-hover-animation: none;
  }
  .komi-head:hover ~ .komi-zigzag {
    --komi-zigzag-opacity: 0;
  }
  .komi-head:hover ~ .komi-buruburu {
    --komi-buruburu-opacity: 0;
  }

  @keyframes twinkleY {
    0%, 100% {
      transform: translateX(-50%) scaleY(1);
    }
    50% {
      transform: translateX(-50%) scaleY(0.5);
    }
  }
  @keyframes twinkleX {
    0%, 100% {
      transform: translateY(-50%) scaleX(1);
    }
    50% {
      transform: translateY(-50%) scaleX(0.5);
    }
  }
  @keyframes catEarTwitch {
    0%, 70%, 90% {
      transform: rotate(0deg);
    }
    80%, 95% {
      transform: rotate(5deg) scaleX(0.9);
    }
  }
  @keyframes tremble {
    0%, 24%, 50%, 74%, 100% {
      transform: translate(0, 0);
    }
    25%, 49% {
      transform: translate(0.0625rem, 0.1875rem);
    }
    75%, 99% {
      transform: translate(-0.0625rem, 0.1875rem);
    }
  }
</style>


<style lang="scss">
    :root {
      --komi-black: #413564;
      --komi-white: #fff;
      --komi-primary-color: #554684;
      --komi-primary-color-dark: #413564;
      --komi-primary-color-tint: #8979b9;
      --komi-secondary-color: #fff5f0;
      --komi-accent-color: #ff4dde;
      --komi-sparkle-color: #ffe085;
      --komi-shirt-color: #fff;
      --komi-shirt-color-dark: #eaeaea;
      --komi-shirt-color-dark-2: #ddd;
      --komi-bow-color-1: #961E60;
      --komi-bow-color-2: #411854;
      --komi-bow-gradient: repeating-linear-gradient(-45deg, var(--komi-bow-color-1) 0 0.25rem, var(--komi-bow-color-2) 0.25rem 0.375rem);
      --komi-background: #c4bcdc;
      --komi-line-width-1: 0.125rem;
      --komi-line-width-2: 0.375rem;
    }

</style>