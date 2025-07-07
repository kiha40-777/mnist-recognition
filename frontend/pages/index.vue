<template>
  <div class="h-screen flex flex-col justify-between">
    <div class="flex flex-col items-center justify-center bg-gray-900 text-white">
      <h1 class="text-4xl font-bold mb-4 mt-8">AI手書き数字認識</h1>
      <p class="text-lg mb-8">自分が何の数字を書いたかAIに当ててもらおう！</p>
    </div>
    <div class="flex items-center justify-center w-full h-full">
      <div class="p-4 flex">
        <div class="text-center items-center mt-4 p-4">
          <p class="text-lg mb-4 text-left">↓数字を書いてみよう！</p>
          <CanvasDrawer />
        </div>
        <div class="text-center items-center mt-4 p-4 flex-none w-[400px]">
          <p class="text-lg mb-4 text-left">　</p>
          <h1 class="text-2xl font-bold mt-2">AIが考えた結果</h1>
        </div>
      </div>
    </div>

    <div class="flex flex-col items-center justify-center bg-gray-900 text-white">
      <h2 class="text-lg mb-4 mt-4">公認サークル iGEM - Waseda</h2>
    </div>
  </div>

</template>

<script setup>
import CanvasDrawer from '../components/CanvasDrawer.vue'
</script>
