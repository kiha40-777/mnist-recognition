<template>
  <div class="h-screen flex flex-col justify-between">
    <div class="flex flex-col items-center justify-center bg-gray-900 text-white">
      <h1 class="text-4xl font-bold mb-4 mt-8">AI手書き数字認識</h1>
      <p class="text-lg mb-8">自分が何の数字を書いたかAIに当ててもらおう！</p>
    </div>
    <div class="flex items-center justify-center">
      <div class="p-4 flex">
        <div class="text-center items-center mt-4 w-1/2 p-4">
          <p class="text-lg mb-4 text-left">↓数字を書いてみよう！</p>
          <CanvasDrawer />
        </div>
        <div class="text-center items-center mt-4 w-1/2 p-4">
          <p class="text-lg mb-4 text-left">　</p>
          <p>手書きの数字をキャンバスに描いて、予測ボタンを押してください。</p>
          <p>予測結果と確信度が表示されます。</p>
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
