<template>
  <div class="h-[650px] flex flex-col justify-between">
    <div class="flex flex-col items-center justify-center bg-gray-900 text-white">
      <h1 class="text-4xl font-bold mb-4 mt-8">AI手書き数字認識</h1>
      <p class="text-lg mb-8">自分が何の数字を書いたかAIに当ててもらおう！</p>
    </div>
    <div class="flex items-center justify-center w-full h-full">
      <div class="p-4 flex">
        <div class="text-center items-center mt-4 p-4">
          <p class="text-lg mb-4 text-left">↓数字を書いてみよう！</p>
          <CanvasDrawer @thinking="thinking = $event" @result="handleResult" @clear="clearPrediction" />
        </div>
        <div class="text-center items-center mt-4 p-4 flex-none w-[400px]">
          <h1 class="text-2xl font-bold mt-2 mb-4">AIが考えた結果</h1>
          <div v-if="prediction !==null && !thinking">
            <h2 v-if="prediction !== null" class="text-xl font-bold mb-2" >あなたの書いた数字は{{ prediction }}です！</h2>
            <h2 v-if="probability !== null" class="text-xl font-bold mb-2" >確信度：{{ ((probability) * 100).toFixed(1) }}%</h2>
            <div v-for="(digit, index) in pred_array" :key="index" class="text-lg mb-1">
              <span class="font-bold">{{ digit }}:</span> {{ ((prob_array[index]) * 100).toFixed(1) }}%
            </div>
          </div>
        </div>
        <transition name="fade">
          <div v-if="thinking" class="fixed inset-0 bg-black/80 flex flex-col items-center justify-center z-50">
            <div class="m-8">
              <p class="text-9xl font-italic">🤔</p>
            </div>
            <div class="m-8">
              <p class="text-white text-4xl font-bold">
                考え中<span class="dots"></span>
              </p>
            </div>
          </div>
      </transition>
      </div>
    </div>

    <!-- <div class="flex flex-col items-center justify-center bg-gray-900 text-white">
      <h2 class="text-lg mb-4 mt-4">公認サークル iGEM - Waseda</h2>
    </div> -->
  </div>

</template>

<script setup>
import CanvasDrawer from '../components/CanvasDrawer.vue'
import { ref } from 'vue'

const prediction = ref(null)
const probability = ref(null)
const thinking = ref(false)
let pred_array = []
let prob_array = []

function handleResult({ digits , probs }) {
  prediction.value = digits[0]
  pred_array = digits.slice(1)
  probability.value = probs[0]
  prob_array = probs.slice(1)
}

function clearPrediction() {
  prediction.value = null
  probability.value = null
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active { transition: opacity .5s ease; }
.fade-enter-from,
.fade-leave-to { opacity: 0; }

@keyframes dot-bounce {
  0%   { content: '\00a0\00a0\00a0';   }   /* 0 個 */
  25%  { content: '.\00a0\00a0';  }   /* 1 個 */
  50%  { content: '..\00a0'; }   /* 2 個 */
  75%  { content: '...';}   /* 3 個 */
  100% { content: '\00a0\00a0\00a0';   }   /* 戻る */
}

.dots::after {
  content: '';
  animation: dot-bounce 1.5s steps(4) infinite;
}
</style>
